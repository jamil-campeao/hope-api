import asyncpg
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreateRequest,
    UserUpdateRequest,
    UserUpdatePasswordRequest,
    UserResponse
)

class UserService:
    def __init__(self, db_connection: asyncpg.Connection):
        self.user_repository = UserRepository(db_connection)

    async def create_user(self, user_data: UserCreateRequest) -> UserResponse:
        return await self.user_repository.create_user(user_data)

    async def update_user(self, user_data: UserUpdateRequest) -> UserResponse:
        return await self.user_repository.update_user(user_data)

    async def update_password(self, user_data: UserUpdatePasswordRequest) -> UserResponse:
        return await self.user_repository.update_password(user_data)

    async def login(self, email: str, password: str):
        user_exists = await self.user_repository.user_exists(email, password)
        if not user_exists:
            raise HTTPException(status_code=400, detail="Usuário não existe")

        #Gero um token JWT
        token = jwt.encode({"email": email}, "secret", algorithm="HS256")