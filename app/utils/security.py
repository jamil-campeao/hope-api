from fastapi import Depends
from app.schemas.user_schema import UserResponse
from app.api.deps import get_current_user

async def get_user_data(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user