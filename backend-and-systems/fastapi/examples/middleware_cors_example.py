"""
Middleware & CORS Example
Run: uvicorn middleware_cors_example:app --reload
Docs: http://127.0.0.1:8000/docs

After running, check response headers in Swagger — you'll see X-Process-Time and X-Request-ID added by middleware.
"""

import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="Middleware & CORS Example")


# ── CORS Middleware ───────────────────────────────────────────────────────────
# Allows the browser to make requests from these origins to this API.
# Without this, a frontend on localhost:3000 calling this API gets blocked.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # React dev server
        "http://localhost:5173",    # Vite dev server
    ],
    allow_credentials=True,         # allow cookies and Authorization headers
    allow_methods=["*"],            # GET, POST, PUT, DELETE, OPTIONS etc.
    allow_headers=["*"],            # Content-Type, Authorization etc.
)


# ── Timing Middleware ─────────────────────────────────────────────────────────
# Wraps EVERY request — logs timing and adds X-Process-Time header to response.

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = round(time.time() - start, 4)
    response.headers["X-Process-Time"] = f"{duration}s"
    print(f"[TIMING] {request.method} {request.url.path} — {duration}s")

    return response


# ── Request ID Middleware ─────────────────────────────────────────────────────
# Attaches a unique ID to every request — useful for tracing logs in production.

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]          # short unique id, e.g. "a3f9b12c"
    request.state.request_id = request_id       # store on request for use in endpoints

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id  # send it back in response header
    return response


# ── Error Handling Middleware ─────────────────────────────────────────────────
# Catches unhandled exceptions and returns a consistent JSON error response.

@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"[ERROR] Unhandled exception: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "request_id": getattr(request.state, "request_id", None)}
        )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"message": "Middleware example running — check response headers in Swagger"}


@app.get("/fast", tags=["Demo"])
def fast_endpoint():
    # quick endpoint — X-Process-Time will be very small
    return {"speed": "fast"}


@app.get("/slow", tags=["Demo"])
def slow_endpoint():
    # simulates a slow operation — X-Process-Time will be ~1s
    time.sleep(1)
    return {"speed": "slow"}


@app.get("/headers", tags=["Demo"])
def show_request_headers(request: Request):
    # returns all headers the client sent — useful for debugging CORS
    return {
        "headers": dict(request.headers),
        "request_id": request.state.request_id
    }


@app.get("/error", tags=["Demo"])
def trigger_error():
    # triggers the error handling middleware
    raise ValueError("This is a test error caught by middleware")
