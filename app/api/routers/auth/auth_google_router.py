from fastapi import APIRouter, Response, Request
from fastapi.responses import RedirectResponse
from app.db.session import db
from app.services.auth.auth_google_service import AuthGoogleService
from app.api.deps import verify_api_token
from app.api.deps import get_current_user
from app.schemas.user_schema import UserResponse
from fastapi import Depends

router = APIRouter()

@router.get("/connect")
async def auth_google_connect():
    async with db.pool.acquire() as conn:
        service = AuthGoogleService(conn)
        url = await service.get_authorization_url()
        return RedirectResponse(url)

@router.get("/callback")
async def auth_google_callback(code: str):
    user_id = 9
    
    async with db.pool.acquire() as conn:
        service = AuthGoogleService(conn)
        result = await service.auth_google_callback(code, user_id)
        return result