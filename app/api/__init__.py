from fastapi import APIRouter
from app.api.endpoints import api_router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router)