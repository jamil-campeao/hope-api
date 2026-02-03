from pydantic import BaseModel

class SessionCreate(BaseModel):
    session_name: str

class MessageSend(BaseModel):
    session: str
    chatId: str
    text: str