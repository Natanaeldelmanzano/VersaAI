from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from datetime import datetime
import uuid

class Chatbot(Base):
    __tablename__ = "chatbots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Unique identifier for embedding
    widget_id = Column(String, unique=True, index=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # Organization and creator
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    
    # AI Configuration
    model_name = Column(String, default="mixtral-8x7b-32768")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=1000)
    system_prompt = Column(Text, nullable=True)
    
    # Appearance
    avatar_url = Column(String, nullable=True)
    primary_color = Column(String, default="#3B82F6")
    secondary_color = Column(String, default="#1F2937")
    welcome_message = Column(Text, default="¡Hola! ¿En qué puedo ayudarte hoy?")
    
    # Widget settings
    widget_position = Column(String, default="bottom-right")  # bottom-right, bottom-left, etc.
    widget_size = Column(String, default="medium")  # small, medium, large
    show_branding = Column(Boolean, default=True)
    
    # Behavior settings
    auto_suggestions = Column(JSON, default=list)  # List of suggested questions
    fallback_message = Column(Text, default="Lo siento, no pude entender tu pregunta. ¿Podrías reformularla?")
    max_conversation_length = Column(Integer, default=50)
    
    # Analytics settings
    collect_analytics = Column(Boolean, default=True)
    collect_feedback = Column(Boolean, default=True)
    
    # Advanced settings
    settings = Column(JSON, default=dict)
    
    # Knowledge base
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_trained = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="chatbots")
    created_by = relationship("User", back_populates="created_chatbots")
    knowledge_base = relationship("KnowledgeBase", back_populates="chatbots")
    conversations = relationship("Conversation", back_populates="chatbot")
    
    def __repr__(self):
        return f"<Chatbot(id={self.id}, name='{self.name}', widget_id='{self.widget_id}')>"
    
    @property
    def total_conversations(self) -> int:
        """Total number of conversations"""
        return len(self.conversations)
    
    @property
    def active_conversations(self) -> int:
        """Number of active conversations"""
        return len([c for c in self.conversations if c.is_active])
    
    def get_widget_config(self) -> dict:
        """Get widget configuration for embedding"""
        return {
            "widget_id": self.widget_id,
            "name": self.name,
            "welcome_message": self.welcome_message,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "avatar_url": self.avatar_url,
            "position": self.widget_position,
            "size": self.widget_size,
            "show_branding": self.show_branding,
            "auto_suggestions": self.auto_suggestions
        }
    
    def get_ai_config(self) -> dict:
        """Get AI configuration"""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "system_prompt": self.system_prompt or "Eres un asistente útil y amigable."
        }
    
    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        if not self.settings:
            return default
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value):
        """Set a specific setting value"""
        if not self.settings:
            self.settings = {}
        self.settings[key] = value