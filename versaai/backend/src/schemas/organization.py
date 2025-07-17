from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class SubscriptionPlan(str, Enum):
    """Subscription plan enum"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class OrganizationStatus(str, Enum):
    """Organization status enum"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    TRIAL = "trial"

class OrganizationBase(BaseModel):
    """Base organization schema"""
    name: str = Field(..., min_length=2, max_length=100, description="Organization name")
    slug: str = Field(..., min_length=2, max_length=50, description="Organization slug")
    description: Optional[str] = Field(None, max_length=500, description="Organization description")
    website: Optional[str] = Field(None, description="Organization website")
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    address: Optional[str] = Field(None, description="Organization address")
    
    @validator('slug')
    def validate_slug(cls, v):
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Slug must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower()

class OrganizationCreate(OrganizationBase):
    """Organization creation schema"""
    subscription_plan: SubscriptionPlan = Field(default=SubscriptionPlan.FREE, description="Subscription plan")
    max_chatbots: Optional[int] = Field(default=1, description="Maximum number of chatbots")
    max_users: Optional[int] = Field(default=5, description="Maximum number of users")
    max_conversations_per_month: Optional[int] = Field(default=1000, description="Maximum conversations per month")

class OrganizationUpdate(BaseModel):
    """Organization update schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Organization name")
    description: Optional[str] = Field(None, max_length=500, description="Organization description")
    website: Optional[str] = Field(None, description="Organization website")
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    address: Optional[str] = Field(None, description="Organization address")
    is_active: Optional[bool] = Field(None, description="Organization active status")
    status: Optional[OrganizationStatus] = Field(None, description="Organization status")
    settings: Optional[Dict[str, Any]] = Field(None, description="Organization settings")
    branding: Optional[Dict[str, Any]] = Field(None, description="Organization branding")

class OrganizationSubscriptionUpdate(BaseModel):
    """Organization subscription update schema"""
    subscription_plan: SubscriptionPlan = Field(..., description="Subscription plan")
    max_chatbots: int = Field(..., ge=1, description="Maximum number of chatbots")
    max_users: int = Field(..., ge=1, description="Maximum number of users")
    max_conversations_per_month: int = Field(..., ge=100, description="Maximum conversations per month")
    subscription_start_date: Optional[datetime] = Field(None, description="Subscription start date")
    subscription_end_date: Optional[datetime] = Field(None, description="Subscription end date")

class OrganizationInDBBase(OrganizationBase):
    """Base organization schema with database fields"""
    id: int = Field(..., description="Organization ID")
    is_active: bool = Field(default=True, description="Organization active status")
    status: OrganizationStatus = Field(default=OrganizationStatus.TRIAL, description="Organization status")
    subscription_plan: SubscriptionPlan = Field(default=SubscriptionPlan.FREE, description="Subscription plan")
    max_chatbots: int = Field(default=1, description="Maximum number of chatbots")
    max_users: int = Field(default=5, description="Maximum number of users")
    max_conversations_per_month: int = Field(default=1000, description="Maximum conversations per month")
    subscription_start_date: Optional[datetime] = Field(None, description="Subscription start date")
    subscription_end_date: Optional[datetime] = Field(None, description="Subscription end date")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Organization settings")
    branding: Dict[str, Any] = Field(default_factory=dict, description="Organization branding")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class Organization(OrganizationInDBBase):
    """Organization schema for API responses"""
    pass

class OrganizationWithStats(Organization):
    """Organization schema with statistics"""
    active_users_count: int = Field(default=0, description="Number of active users")
    active_chatbots_count: int = Field(default=0, description="Number of active chatbots")
    conversations_this_month: int = Field(default=0, description="Conversations this month")
    storage_used_mb: float = Field(default=0.0, description="Storage used in MB")

class OrganizationList(BaseModel):
    """Organization list schema"""
    organizations: List[OrganizationWithStats] = Field(..., description="List of organizations")
    total: int = Field(..., description="Total number of organizations")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")

class OrganizationStats(BaseModel):
    """Organization statistics schema"""
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    total_chatbots: int = Field(..., description="Total number of chatbots")
    active_chatbots: int = Field(..., description="Number of active chatbots")
    total_conversations: int = Field(..., description="Total number of conversations")
    conversations_this_month: int = Field(..., description="Conversations this month")
    total_messages: int = Field(..., description="Total number of messages")
    messages_this_month: int = Field(..., description="Messages this month")
    storage_used_mb: float = Field(..., description="Storage used in MB")
    subscription_plan: SubscriptionPlan = Field(..., description="Current subscription plan")
    subscription_status: OrganizationStatus = Field(..., description="Subscription status")
    days_until_renewal: Optional[int] = Field(None, description="Days until subscription renewal")

class OrganizationUsage(BaseModel):
    """Organization usage schema"""
    chatbots_used: int = Field(..., description="Number of chatbots used")
    chatbots_limit: int = Field(..., description="Chatbot limit")
    users_used: int = Field(..., description="Number of users")
    users_limit: int = Field(..., description="User limit")
    conversations_this_month: int = Field(..., description="Conversations this month")
    conversations_limit: int = Field(..., description="Monthly conversation limit")
    storage_used_mb: float = Field(..., description="Storage used in MB")
    storage_limit_mb: float = Field(..., description="Storage limit in MB")
    
class OrganizationBranding(BaseModel):
    """Organization branding schema"""
    logo_url: Optional[str] = Field(None, description="Logo URL")
    primary_color: Optional[str] = Field(None, description="Primary brand color")
    secondary_color: Optional[str] = Field(None, description="Secondary brand color")
    accent_color: Optional[str] = Field(None, description="Accent color")
    font_family: Optional[str] = Field(None, description="Font family")
    custom_css: Optional[str] = Field(None, description="Custom CSS")
    favicon_url: Optional[str] = Field(None, description="Favicon URL")

class OrganizationSettings(BaseModel):
    """Organization settings schema"""
    default_language: str = Field(default="en", description="Default language")
    default_timezone: str = Field(default="UTC", description="Default timezone")
    allow_anonymous_conversations: bool = Field(default=True, description="Allow anonymous conversations")
    require_user_approval: bool = Field(default=False, description="Require user approval")
    enable_analytics: bool = Field(default=True, description="Enable analytics")
    data_retention_days: int = Field(default=365, description="Data retention period in days")
    max_file_size_mb: int = Field(default=10, description="Maximum file size in MB")
    allowed_file_types: List[str] = Field(default_factory=lambda: ["pdf", "docx", "txt"], description="Allowed file types")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for notifications")
    email_notifications: bool = Field(default=True, description="Enable email notifications")