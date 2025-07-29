"""
Conversation Memory Service for Rxplain Medical AI Assistant
Maintains conversation history and context for medical discussions
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

class Message(BaseModel):
    """Individual message in a conversation"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    model: str  # "gemini" or "gpt"
    is_medical_query: bool = False

class Conversation(BaseModel):
    """Complete conversation with memory"""
    id: str
    title: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
    model: str
    medical_context: Dict[str, Any] = {}

class ConversationMemory:
    """Manages conversation memory and context"""
    
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.max_conversations = 100  # Limit stored conversations
        self.max_messages_per_conversation = 50  # Limit messages per conversation
    
    def create_conversation(self, title: str = "New Conversation", model: str = "gemini") -> str:
        """Create a new conversation"""
        conversation_id = f"conv_{int(time.time())}_{len(self.conversations)}"
        
        conversation = Conversation(
            id=conversation_id,
            title=title,
            messages=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            model=model
        )
        
        self.conversations[conversation_id] = conversation
        
        # Clean up old conversations if limit exceeded
        if len(self.conversations) > self.max_conversations:
            self._cleanup_old_conversations()
        
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str, model: str, is_medical_query: bool = False) -> bool:
        """Add a message to a conversation"""
        if conversation_id not in self.conversations:
            return False
        
        conversation = self.conversations[conversation_id]
        
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            model=model,
            is_medical_query=is_medical_query
        )
        
        conversation.messages.append(message)
        conversation.updated_at = datetime.now()
        
        # Update conversation title if it's the first user message
        if role == "user" and len(conversation.messages) == 1:
            conversation.title = content[:50] + "..." if len(content) > 50 else content
        
        # Limit messages per conversation
        if len(conversation.messages) > self.max_messages_per_conversation:
            conversation.messages = conversation.messages[-self.max_messages_per_conversation:]
        
        return True
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        return self.conversations.get(conversation_id)
    
    def get_conversation_history(self, conversation_id: str, max_messages: int = 10) -> List[Message]:
        """Get recent conversation history for context"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return []
        
        # Return the last N messages for context
        return conversation.messages[-max_messages:] if len(conversation.messages) > max_messages else conversation.messages
    
    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get a summary of the conversation"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return {}
        
        return {
            "id": conversation.id,
            "title": conversation.title,
            "message_count": len(conversation.messages),
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "model": conversation.model,
            "medical_context": conversation.medical_context
        }
    
    def update_medical_context(self, conversation_id: str, context: Dict[str, Any]) -> bool:
        """Update medical context for a conversation"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False
        
        conversation.medical_context.update(context)
        conversation.updated_at = datetime.now()
        return True
    
    def get_all_conversations(self) -> List[Dict[str, Any]]:
        """Get all conversations for the sidebar"""
        conversations = []
        for conv in self.conversations.values():
            conversations.append(self.get_conversation_summary(conv.id))
        
        # Sort by most recent first
        conversations.sort(key=lambda x: x["updated_at"], reverse=True)
        return conversations
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False
    
    def _cleanup_old_conversations(self):
        """Remove old conversations to maintain memory limits"""
        if len(self.conversations) <= self.max_conversations:
            return
        
        # Sort by updated_at and remove oldest
        sorted_conversations = sorted(
            self.conversations.items(),
            key=lambda x: x[1].updated_at
        )
        
        # Remove oldest conversations
        to_remove = len(self.conversations) - self.max_conversations
        for i in range(to_remove):
            del self.conversations[sorted_conversations[i][0]]

# Global conversation memory instance
conversation_memory = ConversationMemory()

def get_conversation_memory() -> ConversationMemory:
    """Get the global conversation memory instance"""
    return conversation_memory

def create_context_prompt(conversation_history: List[Message], current_query: str) -> str:
    """Create a context-aware prompt for the AI"""
    if not conversation_history:
        return current_query
    
    # Build conversation context
    context_parts = []
    context_parts.append("**Previous Conversation Context:**")
    
    for message in conversation_history[-6:]:  # Last 6 messages for context
        role_emoji = "👤" if message.role == "user" else "🤖"
        context_parts.append(f"{role_emoji} **{message.role.title()}**: {message.content}")
    
    context_parts.append(f"\n**Current Query**: {current_query}")
    context_parts.append("\n**Instructions**: Please provide a response that considers the conversation context above. If this is a follow-up question, reference previous information when appropriate.")
    
    return "\n\n".join(context_parts)

def extract_medical_context(messages: List[Message]) -> Dict[str, Any]:
    """Extract medical context from conversation history"""
    context = {
        "medications_mentioned": set(),
        "symptoms_discussed": set(),
        "conditions_referenced": set(),
        "safety_warnings_given": set(),
        "last_medical_topic": None
    }
    
    medical_keywords = {
        "medications": ["medication", "medicine", "drug", "pill", "tablet", "metformin", "aspirin", "ibuprofen"],
        "symptoms": ["symptom", "pain", "fever", "headache", "nausea", "dizziness"],
        "conditions": ["diabetes", "hypertension", "heart disease", "asthma", "arthritis"],
        "warnings": ["side effect", "allergy", "interaction", "warning", "precaution"]
    }
    
    for message in messages:
        content_lower = message.content.lower()
        
        # Extract medications
        for keyword in medical_keywords["medications"]:
            if keyword in content_lower:
                context["medications_mentioned"].add(keyword)
        
        # Extract symptoms
        for keyword in medical_keywords["symptoms"]:
            if keyword in content_lower:
                context["symptoms_discussed"].add(keyword)
        
        # Extract conditions
        for keyword in medical_keywords["conditions"]:
            if keyword in content_lower:
                context["conditions_referenced"].add(keyword)
        
        # Extract warnings
        for keyword in medical_keywords["warnings"]:
            if keyword in content_lower:
                context["safety_warnings_given"].add(keyword)
        
        # Track last medical topic
        if message.is_medical_query:
            context["last_medical_topic"] = message.content[:100]
    
    # Convert sets to lists for JSON serialization
    return {
        "medications_mentioned": list(context["medications_mentioned"]),
        "symptoms_discussed": list(context["symptoms_discussed"]),
        "conditions_referenced": list(context["conditions_referenced"]),
        "safety_warnings_given": list(context["safety_warnings_given"]),
        "last_medical_topic": context["last_medical_topic"]
    } 