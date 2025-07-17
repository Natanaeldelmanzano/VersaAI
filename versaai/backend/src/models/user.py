from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    USER = "user"
    VIEWER = "viewer"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Role and organization
    role = Column(Enum(UserRole), default=UserRole.USER)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Profile info
    avatar_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    timezone = Column(String, default="UTC")
    language = Column(String, default="en")
    preferences = Column(JSON, default=lambda: {})
    login_count = Column(Integer, default=0)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    conversations = relationship("Conversation", back_populates="user")
    created_chatbots = relationship("Chatbot", back_populates="created_by")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def is_admin(self) -> bool:
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]
    
    @property
    def is_super_admin(self) -> bool:
        return self.role == UserRole.SUPER_ADMIN
    
    def can_access_organization(self, org_id: int) -> bool:
        """Check if user can access a specific organization"""
        if self.is_super_admin:
            return True
        return self.organization_id == org_id
    
    def can_manage_chatbot(self, chatbot) -> bool:
        """Check if user can manage a specific chatbot"""
        if self.is_super_admin:
            return True
        if self.role == UserRole.ORG_ADMIN and chatbot.organization_id == self.organization_id:
            return True
        return chatbot.created_by_id == self.id