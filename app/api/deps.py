from fastapi import Header, HTTPException
from app.core.config import settings


def verify_api_token(token: str = Header(...)):
    if token != settings.TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API key")