from fastapi import APIRouter, Response, Request
from fastapi.responses import RedirectResponse
from app.db.session import db
from app.services.auth.auth_google_service import AuthGoogleService

router = APIRouter()

@router.get("/connect")
async def auth_google_connect():
    async with db.pool.acquire() as conn:
        service = AuthGoogleService(conn)
        url = await service.get_authorization_url()
        return RedirectResponse(url)

@router.get("/callback")
async def auth_google_callback(code: str):
    # TODO: In a real scenario, we should get user_id from session/token.
    # For now, hardcoding user_id=1 as per common MVP patterns or extracting from some auth middleware if present.
    # Assuming user_id=1 for testing this flow
    user_id = 1 
    
    async with db.pool.acquire() as conn:
        service = AuthGoogleService(conn)
        result = await service.auth_google_callback(code, user_id)
        return result