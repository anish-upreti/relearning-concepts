"""
Tiny FastAPI app used to learn Docker.
Local run: uvicorn main:app --reload
"""

import os
import socket

from fastapi import FastAPI

app = FastAPI(title="Hello Docker")


@app.get("/")
def root():
    return {"message": "Hello from inside a container!"}


@app.get("/whoami")
def whoami():
    # Inside a container, the hostname is the container ID.
    return {"hostname": socket.gethostname(), "greeting": os.getenv("GREETING", "hi")}
