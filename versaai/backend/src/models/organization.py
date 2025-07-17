from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from datetime import datetime

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Contact info
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Subscription info
    plan_type = Column(String, default="free")  # free, basic, premium, enterprise
    max_chatbots = Column(Integer, default=1)
    max_users = Column(Integer, default=5)
    max_conversations_per_month = Column(Integer, default=1000)
    
    # Settings
    settings = Column(JSON, default=dict)
    
    # Branding
    logo_url = Column(String, nullable=True)
    primary_color = Column(String, default="#3B82F6")
    secondary_color = Column(String, default="#1F2937")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="organization")
    chatbots = relationship("Chatbot", back_populates="organization")
    knowledge_bases = relationship("KnowledgeBase", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', slug='{self.slug}')>"
    
    @property
    def active_users_count(self) -> int:
        """Count of active users in this organization"""
        return len([u for u in self.users if u.is_active])
    
    @property
    def active_chatbots_count(self) -> int:
        """Count of active chatbots in this organization"""
        return len([c for c in self.chatbots if c.is_active])
    
    def can_create_chatbot(self) -> bool:
        """Check if organization can create more chatbots"""
        return self.active_chatbots_count < self.max_chatbots
    
    def can_add_user(self) -> bool:
        """Check if organization can add more users"""
        return self.active_users_count < self.max_users
    
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