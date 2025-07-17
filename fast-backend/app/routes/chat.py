from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.gpt import query_gpt
from app.services.gemini import query_gemini

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gemini"  # or gpt

@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    if request.model == "gemini":
        response = await query_gemini(request.prompt)
    elif request.model == "gpt":
        response = await query_gpt(request.prompt)
    else:
        raise HTTPException(status_code=400, detail="Invalid model")

    return {"response": response}
