from fastapi import APIRouter, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()

class GlobalSettings(BaseModel):
    app_name: str = "VersaAI Platform"
    base_url: str = "http://localhost:3000"
    default_language: str = "es"
    timezone: str = "America/Mexico_City"
    description: str = "Plataforma empresarial de IA con capacidades RAG"
    maintenance_mode: bool = False
    allow_registration: bool = True
    
class AISettings(BaseModel):
    provider: str = "openai"
    default_model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    system_prompt: str = "Eres un asistente IA útil y profesional."
    enable_rag: bool = True
    enable_memory: bool = True

class SecuritySettings(BaseModel):
    session_duration: int = 480  # minutes
    max_login_attempts: int = 5
    min_password_length: int = 8
    lockout_duration: int = 15  # minutes
    require_two_factor: bool = False
    enable_audit_log: bool = True
    require_password_change: bool = False

class EmailSettings(BaseModel):
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = ""
    from_name: str = "VersaAI"
    enable_ssl: bool = True

class StorageSettings(BaseModel):
    provider: str = "local"
    max_file_size_mb: int = 10  # 10MB
    allowed_extensions: list = [".pdf", ".txt", ".docx", ".md"]
    storage_path: str = "uploads"

# Mock settings data
global_settings = GlobalSettings()
ai_settings = AISettings()
security_settings = SecuritySettings()
email_settings = EmailSettings()
storage_settings = StorageSettings()

@router.get("/global")
async def get_global_settings() -> Dict[str, Any]:
    """Get global application settings"""
    return {
        "general": global_settings.dict(),
        "ai": ai_settings.dict(),
        "security": security_settings.dict(),
        "email": email_settings.dict(),
        "storage": storage_settings.dict()
    }

@router.put("/global")
async def update_global_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Update global application settings"""
    # In a real implementation, you would save these to database
    return {
        "message": "Settings updated successfully",
        "updated_at": "2024-01-01T00:00:00Z"
    }

@router.get("/ai")
async def get_ai_settings() -> AISettings:
    """Get AI configuration settings"""
    return ai_settings

@router.put("/ai")
async def update_ai_settings(settings: AISettings) -> Dict[str, Any]:
    """Update AI configuration settings"""
    global ai_settings
    ai_settings = settings
    return {
        "message": "AI settings updated successfully",
        "updated_at": "2024-01-01T00:00:00Z"
    }

@router.get("/security")
async def get_security_settings() -> SecuritySettings:
    """Get security settings"""
    return security_settings

@router.put("/security")
async def update_security_settings(settings: SecuritySettings) -> Dict[str, Any]:
    """Update security settings"""
    global security_settings
    security_settings = settings
    return {
        "message": "Security settings updated successfully",
        "updated_at": "2024-01-01T00:00:00Z"
    }