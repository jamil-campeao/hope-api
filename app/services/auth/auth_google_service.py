import asyncpg
from app.core.config import settings
import urllib.parse
import httpx
from datetime import datetime, timedelta
from app.repositories.google_integration_repository import GoogleIntegrationRepository
from fastapi import HTTPException

class AuthGoogleService:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn
        self.repository = GoogleIntegrationRepository(conn)

    async def get_authorization_url(self) -> str:
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/calendar.events.readonly",
            "access_type": "offline",
            "prompt": "consent"
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        return url

    async def auth_google_callback(self, code: str, user_id: int):
        # 1. Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to retrieve tokens from Google: {response.text}")
            
        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        expires_in = tokens.get("expires_in")
        
        if not refresh_token:
             # If we didn't get a refresh token, it might be because the user already authorized the app previously.
             pass 

        # Calculate expiration
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        await self.repository.save_tokens(user_id, access_token, refresh_token, expires_at)
        
        return {"status": "success", "message": "Google Calendar connected successfully"}