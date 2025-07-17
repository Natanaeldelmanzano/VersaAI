from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, Dict
from sqlalchemy import func

from src.api.deps import get_db, get_current_active_user
from src.models.user import User, UserRole
from src.models.chatbot import Chatbot
from src.models.conversation import Conversation
from src.models.knowledge_base import KnowledgeBase
from src.models.organization import Organization

router = APIRouter()

@router.get("/stats", response_model=Dict[str, Any])
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get dashboard statistics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        # Base queries
        chatbots_query = db.query(Chatbot)
        users_query = db.query(User)
        conversations_query = db.query(Conversation)
        knowledge_bases_query = db.query(KnowledgeBase)
        
        # Filter by organization if not super admin
        if organization_id:
            chatbots_query = chatbots_query.filter(Chatbot.organization_id == organization_id)
            users_query = users_query.filter(User.organization_id == organization_id)
            conversations_query = conversations_query.join(Chatbot).filter(Chatbot.organization_id == organization_id)
            knowledge_bases_query = knowledge_bases_query.filter(KnowledgeBase.organization_id == organization_id)
        
        # Get counts
        chatbots_count = chatbots_query.count()
        users_count = users_query.count()
        conversations_count = conversations_query.count()
        knowledge_bases_count = knowledge_bases_query.count()
        
        # Get active chatbots count
        active_chatbots_query = chatbots_query.filter(Chatbot.is_active == True)
        active_chatbots_count = active_chatbots_query.count()
        
        # Get recent conversations count (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_conversations_count = conversations_query.filter(
            Conversation.created_at >= yesterday
        ).count()
        
        return {
            "chatbots": chatbots_count,
            "active_chatbots": active_chatbots_count,
            "users": users_count,
            "conversations": conversations_count,
            "recent_conversations": recent_conversations_count,
            "knowledge_bases": knowledge_bases_count,
            "organization_id": organization_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve dashboard stats: {str(e)}"
        )

@router.get("/recent-activity", response_model=Dict[str, Any])
def get_recent_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 10
) -> Any:
    """
    Get recent activity for dashboard.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        # Get recent conversations
        conversations_query = db.query(Conversation).join(Chatbot)
        if organization_id:
            conversations_query = conversations_query.filter(Chatbot.organization_id == organization_id)
        
        recent_conversations = conversations_query.order_by(
            Conversation.created_at.desc()
        ).limit(limit).all()
        
        # Get recent chatbots
        chatbots_query = db.query(Chatbot)
        if organization_id:
            chatbots_query = chatbots_query.filter(Chatbot.organization_id == organization_id)
        
        recent_chatbots = chatbots_query.order_by(
            Chatbot.created_at.desc()
        ).limit(limit).all()
        
        return {
            "recent_conversations": [
                {
                    "id": conv.id,
                    "user_name": conv.user_name or "Usuario Anónimo",
                    "chatbot_name": conv.chatbot.name if conv.chatbot else "Chatbot",
                    "created_at": conv.created_at.isoformat(),
                    "status": conv.status
                }
                for conv in recent_conversations
            ],
            "recent_chatbots": [
                {
                    "id": bot.id,
                    "name": bot.name,
                    "description": bot.description,
                    "is_active": bot.is_active,
                    "created_at": bot.created_at.isoformat()
                }
                for bot in recent_chatbots
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve recent activity: {str(e)}"
        )