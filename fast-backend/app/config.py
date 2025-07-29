"""
Configuration settings for Rxplain Medical AI Assistant
"""

import os
from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Medical Assistant Settings
    MAX_RESPONSE_LENGTH: int = 2000
    SAFETY_WARNINGS_ENABLED: bool = True
    MEDICAL_DISCLAIMERS_ENABLED: bool = True
    
    # AI Model Settings
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GPT_MODEL: str = "gpt-4"
    GPT_MAX_TOKENS: int = 1000
    GPT_TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings

def validate_environment():
    """Validate required environment variables"""
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file.")
    
    # OpenAI API key is optional (only needed for GPT model)
    if not settings.OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY not set. GPT model will not be available.")
    
    return True 