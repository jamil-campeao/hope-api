from fastapi import APIRouter

from app.api.routers import (waha_router, user_router)
from app.api.routers.auth import auth_google_router

api_router = APIRouter()

api_router.include_router(waha_router.router, prefix="/waha", tags=["waha"])
api_router.include_router(user_router.router, prefix="/users", tags=["users"])
api_router.include_router(auth_google_router.router, prefix="/auth/google", tags=["auth_google"])
