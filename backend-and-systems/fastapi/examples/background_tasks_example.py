"""
Background Tasks Example
Run: uvicorn background_tasks_example:app --reload
Docs: http://127.0.0.1:8000/docs

How to test:
1. POST /register — response comes back instantly, watch the terminal for background task logs
2. POST /order    — response instant, 3 tasks run in background (watch terminal)
3. POST /report   — long report generation runs in background, you get the job_id immediately
"""

import time
import uuid
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Background Tasks Example")


# ── Fake job store (in-memory) ────────────────────────────────────────────────

JOBS: dict = {}   # job_id → status


# ── Pydantic models ───────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: str

class OrderCreate(BaseModel):
    product: str
    quantity: int
    user_email: str


# ── Background task functions ─────────────────────────────────────────────────
# These are plain functions — they run after the response is sent.
# The print() output shows in your terminal, not in the API response.

def send_welcome_email(email: str, name: str):
    time.sleep(1)   # simulate email sending delay
    print(f"[BG] Welcome email sent to {name} at {email}")


def notify_admin_new_user(name: str, email: str):
    print(f"[BG] Admin notified: new user '{name}' ({email})")


def log_event(event: str, data: dict):
    print(f"[BG] Analytics event '{event}': {data}")


def process_order(product: str, quantity: int, user_email: str):
    time.sleep(2)   # simulate order processing
    print(f"[BG] Order processed: {quantity}x {product} for {user_email}")


def send_order_confirmation(email: str, product: str):
    time.sleep(1)
    print(f"[BG] Order confirmation sent to {email} for {product}")


def generate_report(job_id: str, report_type: str):
    print(f"[BG] Starting report generation: {report_type} (job_id={job_id})")
    JOBS[job_id] = "running"
    time.sleep(5)   # simulate heavy computation
    JOBS[job_id] = "done"
    print(f"[BG] Report done: {report_type} (job_id={job_id})")


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Background tasks example",
        "tip": "Watch the terminal when you hit POST endpoints — background tasks log there"
    }


# Single background task — response is instant, email sends after
@app.post("/register", tags=["Users"])
def register_user(user: UserRegister, background_tasks: BackgroundTasks):
    # critical work done first
    new_user = {"id": str(uuid.uuid4())[:8], "name": user.name, "email": user.email}

    # schedule background tasks — all run after this function returns
    background_tasks.add_task(send_welcome_email, user.email, user.name)

    # response sent immediately
    return {"message": f"Welcome {user.name}! Check your email (watch terminal).", "user": new_user}


# Multiple background tasks — all run in order after response
@app.post("/order", tags=["Orders"])
def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    order_id = str(uuid.uuid4())[:8]

    # 3 tasks scheduled — all run after response, in this order
    background_tasks.add_task(process_order, order.product, order.quantity, order.user_email)
    background_tasks.add_task(send_order_confirmation, order.user_email, order.product)
    background_tasks.add_task(log_event, "order_created", {"order_id": order_id, "product": order.product})

    return {
        "message": "Order placed! (Watch terminal for 3 background tasks running in sequence)",
        "order_id": order_id
    }


# Long-running task — client gets job_id immediately, checks status via polling
@app.post("/reports", tags=["Reports"])
def request_report(report_type: str, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())[:8]
    JOBS[job_id] = "queued"

    # 5-second report generation — runs entirely in background
    background_tasks.add_task(generate_report, job_id, report_type)

    return {
        "message": "Report generation started",
        "job_id": job_id,
        "check_status": f"/reports/{job_id}/status"
    }


@app.get("/reports/{job_id}/status", tags=["Reports"])
def get_report_status(job_id: str):
    status = JOBS.get(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
