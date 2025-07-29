from fastapi import APIRouter, HTTPException, status, Request, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.gemini import query_gemini, validate_medical_query
from app.services.conversation_memory import (
    get_conversation_memory, 
    create_context_prompt, 
    extract_medical_context
)
import uuid

router = APIRouter()

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None
    is_medical_query: bool = False
    conversation_id: str
    medical_context: Dict[str, Any] = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    prompt: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    try:
        # Validate input
        if not prompt.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )

        # Handle image upload
        image_data = None
        if image:
            # Validate image file
            if not image.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File must be an image"
                )
            
            # Read image data
            try:
                image_data = await image.read()
                # Limit image size (5MB)
                if len(image_data) > 5 * 1024 * 1024:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Image size must be less than 5MB"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error reading image: {str(e)}"
                )


        # Get conversation memory
        memory = get_conversation_memory()

        # Handle conversation ID and history
        if not conversation_id:
            conversation_id = memory.create_conversation(
                title=prompt[:50] + "..." if len(prompt) > 50 else prompt
            )

        # Check if this is a medical query
        is_medical_query = validate_medical_query(prompt)

        # Add user message to conversation
        user_message = prompt
        if image:
            user_message += f" [Image uploaded: {image.filename}]"

        # Get model for conversation (default to 'gemini')
        conversation = memory.get_conversation(conversation_id)
        model = conversation.model if conversation else "gemini"

        memory.add_message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
            model=model,
            is_medical_query=is_medical_query
        )

        # Create context-aware prompt
        conversation_history = memory.get_conversation_history(conversation_id, max_messages=6)
        context_prompt = create_context_prompt(conversation_history, prompt)

        # Generate response using Gemini
        response = await query_gemini(context_prompt, image_data)

        memory.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=response,
            model=model,
            is_medical_query=is_medical_query
        )

        # Extract and update medical context
        all_messages = memory.get_conversation_history(conversation_id, max_messages=50)
        medical_context = extract_medical_context(all_messages)
        memory.update_medical_context(conversation_id, medical_context)

        return ChatResponse(
            response=response,
            is_medical_query=is_medical_query,
            conversation_id=conversation_id,
            medical_context=medical_context
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        # Provide helpful error message for medical queries
        if validate_medical_query(prompt):
                            return ChatResponse(
                    response="""I apologize, but I'm experiencing technical difficulties. 

For medical questions, please:
1. **Contact your healthcare provider** for immediate medical advice
2. **Visit reliable medical websites** like Mayo Clinic, WebMD, or MedlinePlus
3. **Call emergency services** if you're experiencing a medical emergency

⚠️ **Important**: Never delay seeking professional medical help due to technical issues with AI assistants.

Your health and safety are the top priority.""",
                    error="Technical error occurred",
                    is_medical_query=True,
                    conversation_id=conversation_id or "error",
                    medical_context={}
                )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )



@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Rxplain Medical AI Assistant",
        "version": "1.0.0",
        "models": {
            "gemini": "Available",
            "gpt": "Available (requires API key)"
        }
    }

@router.get("/medical-keywords")
async def get_medical_keywords():
    """Get list of medical keywords for frontend validation"""
    return {
        "medication_keywords": [
            "medication", "medicine", "drug", "pill", "tablet", "capsule", "injection",
            "prescription", "dosage", "side effect", "interaction", "allergy",
            "metformin", "aspirin", "ibuprofen", "acetaminophen", "antibiotic",
            "blood pressure", "diabetes", "cholesterol", "pain", "fever"
        ],
        "general_health_keywords": [
            "health", "symptom", "treatment", "doctor", "nurse", "hospital",
            "pain", "fever", "allergy", "reaction", "blood", "heart", "diabetes",
            "blood pressure", "cholesterol", "antibiotic", "vitamin", "supplement"
        ]
    }

@router.get("/conversations")
async def get_conversations():
    """Get all conversations for the sidebar"""
    memory = get_conversation_memory()
    return memory.get_all_conversations()

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all messages"""
    memory = get_conversation_memory()
    conversation = memory.get_conversation(conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return {
        "id": conversation.id,
        "title": conversation.title,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "model": msg.model,
                "is_medical_query": msg.is_medical_query
            }
            for msg in conversation.messages
        ],
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "model": conversation.model,
        "medical_context": conversation.medical_context
    }

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    memory = get_conversation_memory()
    success = memory.delete_conversation(conversation_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return {"message": "Conversation deleted successfully"}
