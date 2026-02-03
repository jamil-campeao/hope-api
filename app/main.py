from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router
from app.db.session import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Async API (Raw SQL)"}

@app.get("/health")
async def health_check():
    # Optional: check DB connection here
    return {"status": "ok"}
