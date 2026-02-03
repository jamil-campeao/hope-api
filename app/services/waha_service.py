import httpx
from fastapi import HTTPException
from app.core.config import settings
import base64


class WahaService:
    async def make_request(self, method: str, endpoint: str, payload: dict = None, params: dict = None, is_image: bool = False):
        url = f"{settings.WAHA_BASE_URL}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                headers = {
                    "X-Api-Key": settings.WAHA_API_KEY,
                    "Content-Type": "application/json"
                }
                response = await client.request(method, url, json=payload, params=params, headers=headers)
                response.raise_for_status()

                if is_image:
                    encoded_image = base64.b64encode(response.content).decode("utf-8")
                    return {"image": f"data:image/png;base64,{encoded_image}"}

                return response.json()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc))

    async def create_session(self, session_name: str):
        endpoint = "/api/sessions"
        payload = {"name": session_name}
        return await self.make_request("POST", endpoint, payload)

    async def get_screenshot(self, session_name: str):
        endpoint = f"/api/screenshot"
        params = {
            "session": session_name
        }
        return await self.make_request("GET", endpoint, params=params, is_image=True)
    

    async def send_message(self, session_name: str, chat_id: str, text: str):
        endpoint = "/api/sendText"
        payload = {
            "chatId": chat_id,
            "text": text,
            "session": session_name
        }

        return await self.make_request("POST", endpoint, payload)