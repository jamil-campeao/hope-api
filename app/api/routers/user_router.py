from fastapi import APIRouter
from app.schemas.user_schema import (UserCreateRequest, UserUpdateRequest, UserUpdatePasswordRequest, UserResponse)
from app.services.user_service import UserService
from app.db.session import db

router = APIRouter()

@router.post("", response_model=UserResponse)
async def create_user(user_data: UserCreateRequest) -> UserResponse:
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.create_user(user_data)

@router.put("/{id}", response_model=UserResponse)
async def update_user(user_data: UserUpdateRequest) -> UserResponse:
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.update_user(user_data)

@router.put("/{id}/password", response_model=UserResponse)
async def update_password(user_data: UserUpdatePasswordRequest) -> UserResponse:
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.update_password(user_data)

@router.post("/login")
async def login(login_data: LoginRequest):
    async with db.pool.acquire() as conn:
        user_service = UserService(conn)
        return await user_service.login(login_data)
    