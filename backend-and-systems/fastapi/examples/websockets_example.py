"""
WebSockets Example
Run: uvicorn websockets_example:app --reload
Test: open http://127.0.0.1:8000 in your browser (serves a chat UI)

Open the URL in multiple browser tabs to see real-time broadcast between clients.
Swagger (/docs) does NOT support WebSockets — use the HTML page at / instead.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import json

app = FastAPI(title="WebSockets Example")


# ── Connection Manager ────────────────────────────────────────────────────────
# Tracks all active WebSocket connections and handles broadcast.

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()                         # complete the WS handshake
        self.active_connections.append(websocket)        # track this connection

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)        # remove on disconnect

    async def send_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)               # send to one specific client

    async def broadcast(self, message: str):
        # send to every connected client
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, data: dict):
        # send structured JSON to every connected client
        for connection in self.active_connections:
            await connection.send_json(data)

    @property
    def count(self):
        return len(self.active_connections)


manager = ConnectionManager()


# ── HTML Chat Page ─────────────────────────────────────────────────────────────
# Served at / — open in multiple tabs to test real-time broadcast.

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        #messages { border: 1px solid #ddd; height: 300px; overflow-y: auto; padding: 10px; margin-bottom: 10px; border-radius: 4px; }
        .message { margin: 4px 0; }
        .system { color: #888; font-style: italic; }
        .own { color: #0066cc; }
        input { width: 70%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 8px 16px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; margin-left: 6px; }
        button:hover { background: #0052a3; }
        #status { margin-bottom: 10px; font-size: 13px; }
        .connected { color: green; }
        .disconnected { color: red; }
    </style>
</head>
<body>
    <h2>WebSocket Chat</h2>
    <div id="status" class="disconnected">Disconnected</div>

    <div>
        <input id="username" type="text" placeholder="Your name" value="User1" />
        <button onclick="connect()">Connect</button>
        <button onclick="disconnect()">Disconnect</button>
    </div>
    <br>

    <div id="messages"></div>

    <div>
        <input id="messageText" type="text" placeholder="Type a message..." onkeyup="if(event.key==='Enter') sendMessage()" />
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        let ws = null;

        function addMessage(text, type = "") {
            const div = document.createElement("div");
            div.className = "message " + type;
            div.textContent = text;
            document.getElementById("messages").appendChild(div);
            document.getElementById("messages").scrollTop = 9999;
        }

        function connect() {
            const username = document.getElementById("username").value.trim() || "Anonymous";
            ws = new WebSocket(`ws://localhost:8000/ws/chat/${username}`);

            ws.onopen = () => {
                document.getElementById("status").textContent = `Connected as ${username}`;
                document.getElementById("status").className = "connected";
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                const type = data.type === "system" ? "system" : (data.username === username ? "own" : "");
                const text = data.type === "system" ? data.message : `${data.username}: ${data.message}`;
                addMessage(text, type);
            };

            ws.onclose = () => {
                document.getElementById("status").textContent = "Disconnected";
                document.getElementById("status").className = "disconnected";
            };
        }

        function disconnect() {
            if (ws) ws.close();
        }

        function sendMessage() {
            const input = document.getElementById("messageText");
            const text = input.value.trim();
            if (ws && ws.readyState === WebSocket.OPEN && text) {
                ws.send(text);
                input.value = "";
            }
        }
    </script>
</body>
</html>
"""


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, tags=["Chat UI"])
def get_chat_page():
    # serves the HTML chat page — open in multiple tabs to test broadcast
    return HTML


@app.get("/stats", tags=["Info"])
def get_stats():
    return {"active_connections": manager.count}


# ── WebSocket: simple echo (one client) ───────────────────────────────────────

@app.websocket("/ws/echo")
async def echo_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass


# ── WebSocket: chat room (multiple clients, broadcast) ────────────────────────

@app.websocket("/ws/chat/{username}")
async def chat_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)

    # notify everyone this user joined
    await manager.broadcast_json({
        "type": "system",
        "message": f"{username} joined the chat ({manager.count} online)"
    })

    try:
        while True:
            message = await websocket.receive_text()

            # broadcast message to all connected clients as structured JSON
            await manager.broadcast_json({
                "type": "message",
                "username": username,
                "message": message
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)

        # notify remaining clients this user left
        await manager.broadcast_json({
            "type": "system",
            "message": f"{username} left the chat ({manager.count} online)"
        })
