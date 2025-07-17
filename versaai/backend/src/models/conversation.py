from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from datetime import datetime
import enum
import uuid

class ConversationStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"

class MessageType(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class MessageStatus(str, enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    ERROR = "error"

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # Relationships
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Can be anonymous
    
    # Status
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)
    is_active = Column(Boolean, default=True)
    
    # Metadata
    title = Column(String, nullable=True)  # Auto-generated or user-set
    summary = Column(Text, nullable=True)  # AI-generated summary
    
    # User info (for anonymous users)
    user_name = Column(String, nullable=True)
    user_email = Column(String, nullable=True)
    user_ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Analytics
    total_messages = Column(Integer, default=0)
    user_satisfaction = Column(Integer, nullable=True)  # 1-5 rating
    feedback = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Additional data
    extra_data = Column(JSON, default=dict)
    
    # Relationships
    chatbot = relationship("Chatbot", back_populates="conversations")
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", order_by="Message.created_at")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, session_id='{self.session_id}', status='{self.status}')>"
    
    @property
    def duration_minutes(self) -> float:
        """Calculate conversation duration in minutes"""
        if not self.last_message_at:
            return 0
        delta = self.last_message_at - self.created_at
        return delta.total_seconds() / 60
    
    @property
    def is_anonymous(self) -> bool:
        """Check if conversation is from anonymous user"""
        return self.user_id is None
    
    def close(self, reason: str = None):
        """Close the conversation"""
        self.status = ConversationStatus.CLOSED
        self.is_active = False
        self.closed_at = datetime.utcnow()
        if reason:
            self.set_extra_data("close_reason", reason)
    
    def get_extra_data(self, key: str, default=None):
        """Get extra data value"""
        if not self.extra_data:
            return default
        return self.extra_data.get(key, default)
    
    def set_extra_data(self, key: str, value):
        """Set extra data value"""
        if not self.extra_data:
            self.extra_data = {}
        self.extra_data[key] = value

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Message content
    content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT)
    
    # AI metadata
    model_used = Column(String, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Context and sources
    context_used = Column(JSON, nullable=True)  # RAG context
    sources = Column(JSON, nullable=True)  # Source documents
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional data
    extra_data = Column(JSON, default=dict)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, type='{self.message_type}', conversation_id={self.conversation_id})>"
    
    @property
    def is_from_user(self) -> bool:
        """Check if message is from user"""
        return self.message_type == MessageType.USER
    
    @property
    def is_from_assistant(self) -> bool:
        """Check if message is from assistant"""
        return self.message_type == MessageType.ASSISTANT
    
    def get_extra_data(self, key: str, default=None):
        """Get extra data value"""
        if not self.extra_data:
            return default
        return self.extra_data.get(key, default)
    
    def set_extra_data(self, key: str, value):
        """Set extra data value"""
        if not self.extra_data:
            self.extra_data = {}
        self.extra_data[key] = value