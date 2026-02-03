from fastapi import APIRouter
from app.schemas.waha_schema import SessionCreate, MessageSend
from app.services.waha_service import WahaService

router = APIRouter()

@router.post("/sessions")
async def create_session(session: SessionCreate):
    """
    Inicia uma nova sessão no WAHA.
    """
    waha_service = WahaService()
    return await waha_service.create_session(session.session_name)

@router.get("/screenshot/{session_name}")
async def get_screenshot(session_name: str):
    """
    Pega o screenshot da sessão.
    """
    waha_service = WahaService()
    return await waha_service.get_screenshot(session_name)

@router.post("/send")
async def send_message(msg: MessageSend):
    """
    Envia uma mensagem de texto.
    """
    waha_service = WahaService()
    return await waha_service.send_message(msg.session, msg.chatId, msg.text)
