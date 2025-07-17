from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from ..models.user import User
from ..models.organization import Organization
from ..models.chatbot import Chatbot
from ..models.conversation import Conversation, Message, MessageType
from ..models.knowledge_base import KnowledgeBase, Document
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        pass
    
    def get_organization_overview(self, db: Session, organization_id: int) -> Dict:
        """Get overview statistics for an organization"""
        try:
            # Basic counts
            total_users = db.query(User).filter(
                User.organization_id == organization_id,
                User.is_active == True
            ).count()
            
            total_chatbots = db.query(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Chatbot.is_active == True
            ).count()
            
            total_conversations = db.query(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id
            ).count()
            
            total_messages = db.query(Message).join(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id
            ).count()
            
            # Knowledge base stats
            total_knowledge_bases = db.query(KnowledgeBase).filter(
                KnowledgeBase.organization_id == organization_id
            ).count()
            
            total_documents = db.query(Document).join(KnowledgeBase).filter(
                KnowledgeBase.organization_id == organization_id
            ).count()
            
            # Recent activity (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            recent_conversations = db.query(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Conversation.created_at >= thirty_days_ago
            ).count()
            
            recent_messages = db.query(Message).join(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Message.created_at >= thirty_days_ago
            ).count()
            
            return {
                "total_users": total_users,
                "total_chatbots": total_chatbots,
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "total_knowledge_bases": total_knowledge_bases,
                "total_documents": total_documents,
                "recent_conversations_30d": recent_conversations,
                "recent_messages_30d": recent_messages
            }
            
        except Exception as e:
            logger.error(f"Error getting organization overview: {e}")
            return {}
    
    def get_chatbot_analytics(self, db: Session, chatbot_id: int, days: int = 30) -> Dict:
        """Get analytics for a specific chatbot"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Basic stats
            total_conversations = db.query(Conversation).filter(
                Conversation.chatbot_id == chatbot_id
            ).count()
            
            active_conversations = db.query(Conversation).filter(
                Conversation.chatbot_id == chatbot_id,
                Conversation.is_active == True
            ).count()
            
            total_messages = db.query(Message).join(Conversation).filter(
                Conversation.chatbot_id == chatbot_id
            ).count()
            
            # Recent activity
            recent_conversations = db.query(Conversation).filter(
                Conversation.chatbot_id == chatbot_id,
                Conversation.created_at >= start_date
            ).count()
            
            recent_messages = db.query(Message).join(Conversation).filter(
                Conversation.chatbot_id == chatbot_id,
                Message.created_at >= start_date
            ).count()
            
            # User vs Assistant messages
            user_messages = db.query(Message).join(Conversation).filter(
                Conversation.chatbot_id == chatbot_id,
                Message.message_type == MessageType.USER,
                Message.created_at >= start_date
            ).count()
            
            assistant_messages = db.query(Message).join(Conversation).filter(
                Conversation.chatbot_id == chatbot_id,
                Message.message_type == MessageType.ASSISTANT,
                Message.created_at >= start_date
            ).count()
            
            # Average response time
            avg_response_time = db.query(func.avg(Message.response_time_ms)).join(Conversation).filter(
                Conversation.chatbot_id == chatbot_id,
                Message.message_type == MessageType.ASSISTANT,
                Message.response_time_ms.isnot(None),
                Message.created_at >= start_date
            ).scalar() or 0
            
            # User satisfaction
            satisfaction_data = db.query(
                func.avg(Conversation.user_satisfaction),
                func.count(Conversation.user_satisfaction)
            ).filter(
                Conversation.chatbot_id == chatbot_id,
                Conversation.user_satisfaction.isnot(None),
                Conversation.created_at >= start_date
            ).first()
            
            avg_satisfaction = satisfaction_data[0] or 0
            satisfaction_count = satisfaction_data[1] or 0
            
            return {
                "total_conversations": total_conversations,
                "active_conversations": active_conversations,
                "total_messages": total_messages,
                "recent_conversations": recent_conversations,
                "recent_messages": recent_messages,
                "user_messages": user_messages,
                "assistant_messages": assistant_messages,
                "avg_response_time_ms": round(avg_response_time, 2),
                "avg_satisfaction": round(avg_satisfaction, 2),
                "satisfaction_responses": satisfaction_count,
                "period_days": days
            }
            
        except Exception as e:
            logger.error(f"Error getting chatbot analytics: {e}")
            return {}
    
    def get_conversation_analytics(self, db: Session, organization_id: int, days: int = 30) -> Dict:
        """Get conversation analytics for an organization"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Daily conversation counts
            daily_conversations = db.query(
                func.date(Conversation.created_at).label('date'),
                func.count(Conversation.id).label('count')
            ).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Conversation.created_at >= start_date
            ).group_by(func.date(Conversation.created_at)).all()
            
            # Conversation duration analysis
            avg_duration = db.query(
                func.avg(
                    func.extract('epoch', Conversation.last_message_at - Conversation.created_at) / 60
                )
            ).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Conversation.last_message_at.isnot(None),
                Conversation.created_at >= start_date
            ).scalar() or 0
            
            # Messages per conversation
            avg_messages_per_conversation = db.query(
                func.avg(Conversation.total_messages)
            ).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Conversation.created_at >= start_date
            ).scalar() or 0
            
            # Top performing chatbots
            top_chatbots = db.query(
                Chatbot.name,
                func.count(Conversation.id).label('conversation_count')
            ).join(Conversation).filter(
                Chatbot.organization_id == organization_id,
                Conversation.created_at >= start_date
            ).group_by(Chatbot.id, Chatbot.name).order_by(
                func.count(Conversation.id).desc()
            ).limit(5).all()
            
            return {
                "daily_conversations": [
                    {"date": str(date), "count": count} 
                    for date, count in daily_conversations
                ],
                "avg_duration_minutes": round(avg_duration, 2),
                "avg_messages_per_conversation": round(avg_messages_per_conversation, 2),
                "top_chatbots": [
                    {"name": name, "conversations": count}
                    for name, count in top_chatbots
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation analytics: {e}")
            return {}
    
    def get_usage_analytics(self, db: Session, organization_id: int, days: int = 30) -> Dict:
        """Get usage analytics for an organization"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Token usage
            total_tokens = db.query(
                func.sum(Message.tokens_used)
            ).join(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Message.tokens_used.isnot(None),
                Message.created_at >= start_date
            ).scalar() or 0
            
            # Daily token usage
            daily_tokens = db.query(
                func.date(Message.created_at).label('date'),
                func.sum(Message.tokens_used).label('tokens')
            ).join(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Message.tokens_used.isnot(None),
                Message.created_at >= start_date
            ).group_by(func.date(Message.created_at)).all()
            
            # Model usage
            model_usage = db.query(
                Message.model_used,
                func.count(Message.id).label('count'),
                func.sum(Message.tokens_used).label('tokens')
            ).join(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Message.model_used.isnot(None),
                Message.created_at >= start_date
            ).group_by(Message.model_used).all()
            
            # Peak usage hours
            hourly_usage = db.query(
                func.extract('hour', Message.created_at).label('hour'),
                func.count(Message.id).label('count')
            ).join(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Message.created_at >= start_date
            ).group_by(func.extract('hour', Message.created_at)).all()
            
            return {
                "total_tokens": int(total_tokens),
                "daily_tokens": [
                    {"date": str(date), "tokens": int(tokens or 0)}
                    for date, tokens in daily_tokens
                ],
                "model_usage": [
                    {
                        "model": model,
                        "message_count": count,
                        "total_tokens": int(tokens or 0)
                    }
                    for model, count, tokens in model_usage
                ],
                "hourly_usage": [
                    {"hour": int(hour), "count": count}
                    for hour, count in hourly_usage
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting usage analytics: {e}")
            return {}
    
    def get_user_analytics(self, db: Session, organization_id: int, days: int = 30) -> Dict:
        """Get user analytics for an organization"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Active users
            active_users = db.query(User).filter(
                User.organization_id == organization_id,
                User.is_active == True,
                User.last_login >= start_date
            ).count()
            
            # New users
            new_users = db.query(User).filter(
                User.organization_id == organization_id,
                User.created_at >= start_date
            ).count()
            
            # User activity
            user_activity = db.query(
                func.date(User.last_login).label('date'),
                func.count(User.id).label('active_users')
            ).filter(
                User.organization_id == organization_id,
                User.last_login >= start_date
            ).group_by(func.date(User.last_login)).all()
            
            # Anonymous vs registered conversations
            anonymous_conversations = db.query(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Conversation.user_id.is_(None),
                Conversation.created_at >= start_date
            ).count()
            
            registered_conversations = db.query(Conversation).join(Chatbot).filter(
                Chatbot.organization_id == organization_id,
                Conversation.user_id.isnot(None),
                Conversation.created_at >= start_date
            ).count()
            
            return {
                "active_users": active_users,
                "new_users": new_users,
                "anonymous_conversations": anonymous_conversations,
                "registered_conversations": registered_conversations,
                "user_activity": [
                    {"date": str(date), "active_users": count}
                    for date, count in user_activity
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting user analytics: {e}")
            return {}
    
    def get_knowledge_base_analytics(self, db: Session, organization_id: int) -> Dict:
        """Get knowledge base analytics for an organization"""
        try:
            # Knowledge base stats
            kb_stats = db.query(
                KnowledgeBase.name,
                KnowledgeBase.total_documents,
                KnowledgeBase.total_chunks,
                func.count(Chatbot.id).label('chatbot_count')
            ).outerjoin(Chatbot).filter(
                KnowledgeBase.organization_id == organization_id
            ).group_by(
                KnowledgeBase.id, 
                KnowledgeBase.name, 
                KnowledgeBase.total_documents, 
                KnowledgeBase.total_chunks
            ).all()
            
            # Document processing stats
            doc_stats = db.query(
                Document.status,
                func.count(Document.id).label('count')
            ).join(KnowledgeBase).filter(
                KnowledgeBase.organization_id == organization_id
            ).group_by(Document.status).all()
            
            # Document types
            doc_types = db.query(
                Document.document_type,
                func.count(Document.id).label('count')
            ).join(KnowledgeBase).filter(
                KnowledgeBase.organization_id == organization_id
            ).group_by(Document.document_type).all()
            
            return {
                "knowledge_bases": [
                    {
                        "name": name,
                        "documents": documents or 0,
                        "chunks": chunks or 0,
                        "chatbots": chatbot_count
                    }
                    for name, documents, chunks, chatbot_count in kb_stats
                ],
                "document_status": [
                    {"status": status.value, "count": count}
                    for status, count in doc_stats
                ],
                "document_types": [
                    {"type": doc_type.value, "count": count}
                    for doc_type, count in doc_types
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting knowledge base analytics: {e}")
            return {}
    
    def get_comprehensive_analytics(
        self, 
        db: Session, 
        organization_id: int, 
        days: int = 30
    ) -> Dict:
        """Get comprehensive analytics for an organization"""
        try:
            return {
                "overview": self.get_organization_overview(db, organization_id),
                "conversations": self.get_conversation_analytics(db, organization_id, days),
                "usage": self.get_usage_analytics(db, organization_id, days),
                "users": self.get_user_analytics(db, organization_id, days),
                "knowledge_base": self.get_knowledge_base_analytics(db, organization_id),
                "period_days": days,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting comprehensive analytics: {e}")
            return {}

# Global instance
analytics_service = AnalyticsService()