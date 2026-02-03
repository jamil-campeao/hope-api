from fastapi import APIRouter

from app.api.routers import (waha_router, user_router)

api_router = APIRouter()

api_router.include_router(waha_router.router, prefix="/waha", tags=["waha"])
api_router.include_router(user_router.router, prefix="/users", tags=["users"])
