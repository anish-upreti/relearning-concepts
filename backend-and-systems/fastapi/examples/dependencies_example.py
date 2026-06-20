"""
Dependencies & Injection Example
Run: uvicorn dependencies_example:app --reload
Docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI(title="Dependencies Example")

security = HTTPBearer()


# ── Pydantic models ──────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str


# ── Fake database ────────────────────────────────────────────────────────────

FAKE_USERS_DB = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com",   "role": "user"},
}

VALID_TOKENS = {
    "admin-token": 1,   # maps token → user_id
    "user-token":  2,
}


# ── Dependency: shared pagination params ─────────────────────────────────────
# Write once, reuse in any endpoint that needs pagination

def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# ── Dependency: database session (yield pattern) ─────────────────────────────
# Code before yield = setup (open connection)
# Code after yield  = cleanup (close connection)

def get_db():
    db = FAKE_USERS_DB.copy()   # simulate opening a DB session
    try:
        yield db
    finally:
        pass   # simulate closing the DB session


# ── Dependency: auth — extracts and validates the token ──────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    token = credentials.credentials
    user_id = VALID_TOKENS.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ── Dependency: chained — requires admin role ────────────────────────────────
# Depends on get_current_user, which depends on security + get_db

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"message": "Dependencies example running", "docs": "/docs"}


# Pagination dependency injected — try /users?skip=0&limit=5
@app.get("/users", tags=["Users"])
def list_users(
    params: dict = Depends(pagination),
    db = Depends(get_db)
):
    users = list(db.values())
    start = params["skip"]
    end   = start + params["limit"]
    return {"users": users[start:end], "pagination": params}


# Auth dependency — use "Bearer admin-token" or "Bearer user-token" in Swagger
@app.get("/profile", tags=["Users"])
def get_profile(current_user: dict = Depends(get_current_user)):
    return {"profile": current_user}


# Chained dependency — only admin-token works here
@app.get("/admin/stats", tags=["Admin"])
def get_stats(admin = Depends(require_admin)):
    return {
        "total_users": len(FAKE_USERS_DB),
        "admin": admin["name"]
    }


@app.delete("/admin/users/{user_id}", tags=["Admin"])
def delete_user(user_id: int, admin = Depends(require_admin), db = Depends(get_db)):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"deleted": user_id, "by": admin["name"]}
