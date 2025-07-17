from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import time

router = APIRouter()

class ActivityItem(BaseModel):
    id: str
    type: str  # chatbot_created, conversation_started, document_uploaded, user_joined, etc.
    title: str
    description: str
    user_name: str
    user_avatar: Optional[str] = None
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None
    icon: Optional[str] = None
    color: Optional[str] = None

# Mock activity data
mock_activities = [
    ActivityItem(
        id="1",
        type="system_start",
        title="Sistema iniciado",
        description="VersaAI Platform se ha iniciado correctamente",
        user_name="Sistema",
        timestamp="2024-01-01T10:00:00Z",
        icon="🚀",
        color="green",
        metadata={"version": "1.0.0"}
    ),
    ActivityItem(
        id="2",
        type="user_login",
        title="Inicio de sesión",
        description="Usuario administrador ha iniciado sesión",
        user_name="Admin",
        user_avatar="https://ui-avatars.com/api/?name=Admin&background=6366f1&color=fff",
        timestamp="2024-01-01T09:45:00Z",
        icon="👤",
        color="blue"
    ),
    ActivityItem(
        id="3",
        type="dashboard_view",
        title="Dashboard accedido",
        description="Se ha accedido al panel principal",
        user_name="Admin",
        user_avatar="https://ui-avatars.com/api/?name=Admin&background=6366f1&color=fff",
        timestamp="2024-01-01T09:44:00Z",
        icon="📊",
        color="purple"
    ),
    ActivityItem(
        id="4",
        type="api_call",
        title="API consultada",
        description="Endpoint de configuración global consultado",
        user_name="Sistema",
        timestamp="2024-01-01T09:43:00Z",
        icon="🔗",
        color="gray",
        metadata={"endpoint": "/api/v1/settings/global"}
    ),
    ActivityItem(
        id="5",
        type="health_check",
        title="Verificación de salud",
        description="Sistema verificado - Estado: Saludable",
        user_name="Sistema",
        timestamp="2024-01-01T09:40:00Z",
        icon="💚",
        color="green"
    ),
    ActivityItem(
        id="6",
        type="database_connect",
        title="Base de datos conectada",
        description="Conexión a base de datos establecida correctamente",
        user_name="Sistema",
        timestamp="2024-01-01T09:35:00Z",
        icon="🗄️",
        color="blue"
    ),
    ActivityItem(
        id="7",
        type="server_ready",
        title="Servidor listo",
        description="Servidor backend iniciado en puerto 8000",
        user_name="Sistema",
        timestamp="2024-01-01T09:30:00Z",
        icon="⚡",
        color="yellow"
    ),
    ActivityItem(
        id="8",
        type="frontend_ready",
        title="Frontend listo",
        description="Aplicación frontend iniciada en puerto 3000",
        user_name="Sistema",
        timestamp="2024-01-01T09:25:00Z",
        icon="🌐",
        color="cyan"
    )
]

@router.get("/recent")
async def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    activity_type: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """Get recent activity"""
    
    activities = mock_activities.copy()
    
    if activity_type:
        activities = [a for a in activities if a.type == activity_type]
    
    # Apply pagination
    total = len(activities)
    activities = activities[offset:offset + limit]
    
    return {
        "activities": [a.dict() for a in activities],
        "total": total,
        "has_more": offset + limit < total
    }

@router.get("/stats")
async def get_activity_stats() -> Dict[str, Any]:
    """Get activity statistics"""
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    
    return {
        "today_count": len(mock_activities),
        "week_count": len(mock_activities),
        "total_count": len(mock_activities),
        "most_active_user": "Admin",
        "most_common_activity": "api_call",
        "last_activity": mock_activities[0].timestamp if mock_activities else None
    }

@router.get("/types")
async def get_activity_types() -> Dict[str, List[str]]:
    """Get available activity types"""
    types = list(set(a.type for a in mock_activities))
    return {"types": types}

@router.post("/")
async def create_activity(activity: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new activity entry"""
    new_activity = ActivityItem(
        id=str(len(mock_activities) + 1),
        type=activity.get("type", "custom"),
        title=activity.get("title", ""),
        description=activity.get("description", ""),
        user_name=activity.get("user_name", "Usuario"),
        user_avatar=activity.get("user_avatar"),
        timestamp=datetime.now().isoformat() + "Z",
        icon=activity.get("icon", "📝"),
        color=activity.get("color", "gray"),
        metadata=activity.get("metadata")
    )
    
    mock_activities.insert(0, new_activity)
    
    return {
        "message": "Activity created",
        "activity": new_activity.dict()
    }