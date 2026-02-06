import asyncpg
from app.db.session import db
from datetime import datetime

class GoogleIntegrationRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def save_tokens(self, user_id: int, access_token: str, refresh_token: str, expires_at: datetime):
        sql = """
            INSERT INTO integrations_google (user_id, access_token, refresh_token, token_expires_at)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (id) DO UPDATE 
            SET access_token = EXCLUDED.access_token,
                refresh_token = EXCLUDED.refresh_token,
                token_expires_at = EXCLUDED.token_expires_at,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id
        """
        
        check_sql = "SELECT id FROM integrations_google WHERE user_id = $1"
        existing_id = await self.conn.fetchval(check_sql, user_id)
        
        if existing_id:
            update_sql = """
                UPDATE integrations_google 
                SET access_token = $1, refresh_token = $2, token_expires_at = $3, updated_at = CURRENT_TIMESTAMP
                WHERE id = $4
            """
            await self.conn.execute(update_sql, access_token, refresh_token, expires_at, existing_id)
            return existing_id
        else:
            return await self.conn.fetchval(sql, user_id, access_token, refresh_token, expires_at)
