from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def receive_prompt(data: PromptRequest):
    # For now, just return what was received
    return {"received_prompt": data.prompt}
