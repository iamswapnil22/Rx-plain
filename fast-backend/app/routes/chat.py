from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.services.gemini import query_gemini
from app.services.gpt import query_gpt

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gemini"

class ChatResponse(BaseModel):
    response: str
    model: str
    error: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    try:
        if not request.prompt.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )

        if request.model == "gemini":
            response = await query_gemini(request.prompt)
        elif request.model == "gpt":
            response = await query_gpt(request.prompt)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid model. Use 'gemini' or 'gpt'"
            )

        return ChatResponse(
            response=response,
            model=request.model,
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
