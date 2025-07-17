from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import time

router = APIRouter()

class Notification(BaseModel):
    id: str
    title: str
    message: str
    type: str  # info, success, warning, error
    read: bool = False
    created_at: str
    action_url: Optional[str] = None
    icon: Optional[str] = None

# Mock notifications data
mock_notifications = [
    Notification(
        id="1",
        title="Bienvenido a VersaAI",
        message="Tu plataforma de IA está lista para usar. Comienza creando tu primer chatbot.",
        type="info",
        created_at="2024-01-01T10:00:00Z",
        action_url="/dashboard/chatbots",
        icon="🤖"
    ),
    Notification(
        id="2",
        title="Sistema actualizado",
        message="Se han aplicado las últimas mejoras de seguridad y rendimiento.",
        type="success",
        created_at="2024-01-01T09:30:00Z",
        icon="✅"
    ),
    Notification(
        id="3",
        title="Configuración recomendada",
        message="Te recomendamos configurar tu organización para una mejor experiencia.",
        type="warning",
        created_at="2024-01-01T09:00:00Z",
        action_url="/dashboard/organization",
        icon="⚙️"
    ),
    Notification(
        id="4",
        title="Base de conocimiento",
        message="Sube documentos para mejorar las respuestas de tus chatbots.",
        type="info",
        created_at="2024-01-01T08:30:00Z",
        action_url="/dashboard/knowledge-bases",
        icon="📚"
    ),
    Notification(
        id="5",
        title="Analíticas disponibles",
        message="Revisa el rendimiento de tus chatbots en la sección de analíticas.",
        type="info",
        created_at="2024-01-01T08:00:00Z",
        action_url="/dashboard/analytics",
        icon="📊"
    )
]

@router.get("/")
async def get_notifications(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    unread_only: bool = Query(False)
) -> Dict[str, Any]:
    """Get user notifications"""
    
    notifications = mock_notifications.copy()
    
    if unread_only:
        notifications = [n for n in notifications if not n.read]
    
    # Apply pagination
    total = len(notifications)
    notifications = notifications[offset:offset + limit]
    
    return {
        "notifications": [n.dict() for n in notifications],
        "total": total,
        "unread_count": len([n for n in mock_notifications if not n.read]),
        "has_more": offset + limit < total
    }

@router.get("/unread-count")
async def get_unread_count() -> Dict[str, int]:
    """Get count of unread notifications"""
    unread_count = len([n for n in mock_notifications if not n.read])
    return {"count": unread_count}

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: str) -> Dict[str, Any]:
    """Mark notification as read"""
    for notification in mock_notifications:
        if notification.id == notification_id:
            notification.read = True
            break
    
    return {"message": "Notification marked as read"}

@router.put("/mark-all-read")
async def mark_all_as_read() -> Dict[str, Any]:
    """Mark all notifications as read"""
    for notification in mock_notifications:
        notification.read = True
    
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
async def delete_notification(notification_id: str) -> Dict[str, Any]:
    """Delete a notification"""
    global mock_notifications
    mock_notifications = [n for n in mock_notifications if n.id != notification_id]
    
    return {"message": "Notification deleted"}

@router.post("/")
async def create_notification(notification: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new notification"""
    new_notification = Notification(
        id=str(len(mock_notifications) + 1),
        title=notification.get("title", ""),
        message=notification.get("message", ""),
        type=notification.get("type", "info"),
        created_at=datetime.now().isoformat() + "Z",
        action_url=notification.get("action_url"),
        icon=notification.get("icon")
    )
    
    mock_notifications.insert(0, new_notification)
    
    return {
        "message": "Notification created",
        "notification": new_notification.dict()
    }