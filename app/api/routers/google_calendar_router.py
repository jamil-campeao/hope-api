from fastapi import APIRouter, Depends
from app.db.session import db
from app.api.deps import get_current_user

router = APIRouter()
        