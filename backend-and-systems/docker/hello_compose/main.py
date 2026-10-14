"""
FastAPI + Redis hit counter used to learn Docker Compose.
The app finds Redis by its SERVICE NAME ("redis"), not an IP address.
"""

import os
import socket

import redis
from fastapi import FastAPI

app = FastAPI(title="Hello Compose")

# Inside Compose, the hostname "redis" resolves to the redis container.
cache = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)


@app.get("/")
def root():
    return {"message": "Hello from the API container!"}


@app.get("/hits")
def hits():
    # INCR is atomic, so many API containers can share one counter safely.
    return {"hits": cache.incr("hits"), "served_by": socket.gethostname()}


@app.get("/health")
def health():
    cache.ping()
    return {"status": "ok"}
