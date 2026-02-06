from fastapi import APIRouter, Depends
from app.schemas.user_schema import (UserCreateRequest, UserUpdateRequest, UserUpdatePasswordRequest, 
                                    UserResponse, LoginRequest, LoginResponse)
from app.services.user_service import UserService
from app.db.session import db
from app.api.deps import verify_api_token
from app.utils.security import get_user_data

router = APIRouter()

@router.post("/create", response_model=UserResponse)
async def create_user(user_data: UserCreateRequest) -> UserResponse:
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.create_user(user_data)

@router.put("/update", response_model=UserResponse, dependencies=[Depends(verify_api_token)])
async def update_user(user_data: UserUpdateRequest, current_user: UserResponse = Depends(get_user_data)) -> UserResponse:
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.update_user(user_data, current_user.id)

@router.put("/alter-password", response_model=UserResponse, dependencies=[Depends(verify_api_token)])
async def update_password(user_data: UserUpdatePasswordRequest, current_user: UserResponse = Depends(get_user_data)) -> UserResponse:
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.update_password(user_data, current_user.id)

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest) -> LoginResponse:
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.login(login_data)
    