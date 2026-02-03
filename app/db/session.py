import asyncpg
from app.core.config import settings

class Database:
    pool: asyncpg.Pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                str(settings.POSTGRES_URI)
            )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

db = Database()

async def get_db_pool():
    if not db.pool:
        await db.connect()
    return db.pool
