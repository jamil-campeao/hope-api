

class GoogleCalendarService:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def get_calendar_list(self, user_id: int):
        pass