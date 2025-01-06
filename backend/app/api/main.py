from fastapi import APIRouter

from app.api.routes import (
    addresses,
    carts,
    login,
    orders,
    products,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(addresses.router, prefix="/addresses", tags=["addresses"])
api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.add_api_route("/webhook", utils.webhook, methods=["POST"], tags=["utils"])
