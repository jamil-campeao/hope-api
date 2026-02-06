import asyncpg
import jwt
from datetime import datetime, timedelta
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (UserCreateRequest, UserUpdateRequest, UserUpdatePasswordRequest, 
                                    UserResponse, LoginResponse)
from fastapi import HTTPException
from app.core.config import settings

class UserService:
    def __init__(self, db_connection: asyncpg.Connection):
        self.conn = db_connection
        self.user_repository = UserRepository(db_connection)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        # Using settings.TOKEN as secret for now as per codebase convention found in .env, ideally separate JWT_SECRET
        encoded_jwt = jwt.encode(to_encode, settings.TOKEN, algorithm="HS256") 
        return encoded_jwt

    async def login(self, login_data) -> LoginResponse: 
        user_exists = await self.user_repository.user_exists(login_data.email, login_data.password)
        if not user_exists:
            raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

        user_data = await self.user_repository.get_user_by_email(login_data.email)
        
        # Determine expiration: 30 days as requested (approx)
        access_token_expires = timedelta(days=30)
        access_token = self.create_access_token(
            data={"sub": login_data.email}, expires_delta=access_token_expires
        )
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_data
        )

    async def create_user(self, user_data: UserCreateRequest) -> UserResponse:
        return await self.user_repository.create_user(user_data)

    async def update_user(self, user_data: UserUpdateRequest, user_id: int) -> UserResponse:
        return await self.user_repository.update_user(user_data, user_id)

    async def update_password(self, user_data: UserUpdatePasswordRequest, user_id: int) -> UserResponse:
        return await self.user_repository.update_password(user_data, user_id)