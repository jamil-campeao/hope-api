import asyncpg
from app.schemas.user_schema import UserCreateRequest, UserUpdateRequest, UserUpdatePasswordRequest, UserResponse
from fastapi import HTTPException
from app.utils.security import get_password_hash, verify_password

class UserRepository:
    def __init__(self, db_connection: asyncpg.Connection):
        self.conn = db_connection

    async def create_user(self, user_data: UserCreateRequest) -> UserResponse:
        hashed_password = get_password_hash(user_data.password)
        sql = """
            INSERT INTO users (email, name, password, phone)
            VALUES ($1, $2, $3, $4)
            RETURNING id, email, name, phone, is_active, created_at, updated_at
        """
        try:
            result = await self.conn.fetchrow(sql, user_data.email, user_data.name, hashed_password, user_data.phone)
            return UserResponse(**result)
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Usuário já existe")
        except Exception as e:
            raise Exception(f"Erro ao criar usuário: {str(e)}")

    async def update_user(self, user_data: UserUpdateRequest, user_id: int) -> UserResponse:
        sql = """
            UPDATE users
            SET email = $1, name = $2, phone = $3, is_active = $4
            WHERE id = $5
            RETURNING id, email, name, phone, is_active, created_at, updated_at
        """
        try:
            result = await self.conn.fetchrow(sql, user_data.email, user_data.name, user_data.phone, user_data.active, user_id)
            return UserResponse(**result)
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Usuário já existe")
        except Exception as e:
            raise Exception(f"Erro ao atualizar usuário: {str(e)}")

    async def update_password(self, user_data: UserUpdatePasswordRequest, user_id: int) -> UserResponse:
        hashed_password = get_password_hash(user_data.new_password)
        sql = """
            UPDATE users
            SET password = $1
            WHERE id = $2
            RETURNING id, email, name, phone, is_active, created_at, updated_at
        """
        try:
            result = await self.conn.fetchrow(sql, hashed_password, user_id)
            return UserResponse(**result)
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Usuário já existe")
        except Exception as e:
            raise Exception(f"Erro ao atualizar senha do usuário: {str(e)}")

    async def user_exists(self, email: str, password: str) -> bool:
        sql = """
            SELECT password
            FROM users
            WHERE email = $1
        """
        try:
            result = await self.conn.fetchrow(sql, email)
            if not result:
                return False
            return verify_password(password, result['password'])
        except Exception as e:
            raise Exception(f"Erro ao verificar se o usuário existe: {str(e)}")

    async def get_user_by_email(self, email: str) -> UserResponse:
        sql = """
            SELECT email, name, phone, is_active, created_at, updated_at
            FROM users
            WHERE email = $1
        """
        try:
            result = await self.conn.fetchrow(sql, email)
            return UserResponse(**result)
        except Exception as e:
            raise Exception(f"Erro ao buscar usuário: {str(e)}")
        