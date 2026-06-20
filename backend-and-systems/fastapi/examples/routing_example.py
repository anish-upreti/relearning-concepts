"""
Advanced Routing with APIRouter
Run: uvicorn routing_example:app --reload
Docs: http://127.0.0.1:8000/docs

Notice in Swagger how routes are grouped under "Users", "Products", "Admin" tags.
v1 and v2 routes live side by side — old clients keep working.
"""

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional


# ── Pydantic models ───────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: str

class ProductCreate(BaseModel):
    name: str
    price: float
    category: Optional[str] = None


# ── Fake data ─────────────────────────────────────────────────────────────────

USERS    = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
PRODUCTS = [{"id": 1, "name": "Laptop", "price": 999.99}, {"id": 2, "name": "Phone", "price": 499.99}]


# ── Shared dependency ─────────────────────────────────────────────────────────

def get_api_key(api_key: str = ""):
    if api_key != "secret":
        raise HTTPException(status_code=403, detail="Invalid API key — use ?api_key=secret")
    return api_key


# ── Users Router ──────────────────────────────────────────────────────────────

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@users_router.get("/")
def list_users():
    return {"users": USERS}

@users_router.get("/{user_id}")
def get_user(user_id: int):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.post("/", status_code=201)
def create_user(user: UserCreate):
    new_user = {"id": len(USERS) + 1, "name": user.name, "email": user.email}
    USERS.append(new_user)
    return new_user


# ── Products Router ───────────────────────────────────────────────────────────

products_router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@products_router.get("/")
def list_products(category: Optional[str] = None):
    if category:
        return {"products": [p for p in PRODUCTS if p.get("category") == category]}
    return {"products": PRODUCTS}

@products_router.get("/{product_id}")
def get_product(product_id: int):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@products_router.post("/", status_code=201)
def create_product(product: ProductCreate):
    new_product = {"id": len(PRODUCTS) + 1, **product.model_dump()}
    PRODUCTS.append(new_product)
    return new_product


# ── Admin Router (router-level dependency) ────────────────────────────────────
# Every route here requires the API key — applied once, not per endpoint

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_api_key)],   # protects ALL routes in this router
)

@admin_router.get("/stats")
def get_stats():
    return {
        "total_users":    len(USERS),
        "total_products": len(PRODUCTS),
    }

@admin_router.delete("/users/{user_id}")
def delete_user(user_id: int):
    global USERS
    USERS = [u for u in USERS if u["id"] != user_id]
    return {"deleted": user_id}


# ── Versioned Routers ─────────────────────────────────────────────────────────
# v1 and v2 live at the same time — old clients use v1, new clients use v2

v1_router = APIRouter(prefix="/v1", tags=["v1"])
v2_router = APIRouter(prefix="/v2", tags=["v2"])

@v1_router.get("/status")
def status_v1():
    return {"version": "v1", "status": "ok"}

@v2_router.get("/status")
def status_v2():
    # v2 returns extra info — backwards compatible since v1 still works
    return {"version": "v2", "status": "ok", "uptime": "100%", "region": "us-east"}


# ── Main App — wires everything together ──────────────────────────────────────

app = FastAPI(title="Routing Example")

app.include_router(users_router)
app.include_router(products_router)
app.include_router(admin_router)
app.include_router(v1_router)
app.include_router(v2_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Routing example running",
        "routes": {
            "users":    "/users",
            "products": "/products",
            "admin":    "/admin (requires ?api_key=secret)",
            "v1":       "/v1/status",
            "v2":       "/v2/status",
            "docs":     "/docs",
        }
    }
