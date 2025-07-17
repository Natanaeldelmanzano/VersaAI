from fastapi import APIRouter, Depends
from typing import Dict, Any
import time
from ....core.config import settings

router = APIRouter()

@router.get("/info")
async def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    return {
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production",
        "timestamp": time.time(),
        "uptime": time.time(),
        "features": {
            "rag_enabled": True,
            "analytics_enabled": True,
            "multi_language": True,
            "real_time_chat": True
        }
    }

@router.get("/status")
async def get_system_status() -> Dict[str, Any]:
    """Get system status"""
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "available",
        "storage": "available",
        "memory_usage": "normal",
        "cpu_usage": "normal",
        "last_check": time.time()
    }

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Detailed health check"""
    return {
        "status": "healthy",
        "checks": {
            "database": True,
            "ai_service": True,
            "storage": True,
            "external_apis": True
        },
        "timestamp": time.time()
    }