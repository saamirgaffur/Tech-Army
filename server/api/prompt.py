import httpx
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def receive_prompt(data: PromptRequest):
    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
        # Convert Pydantic model to dict before sending
        response = await client.post(
            "http://127.0.0.1:8000/chatbot/",
            json={"user_query": data.prompt}  # Use data.prompt (string), or data.dict()
        )
        print(f"[Prompt Response]: {response.json()}")
        response.raise_for_status()
        return response.json()
