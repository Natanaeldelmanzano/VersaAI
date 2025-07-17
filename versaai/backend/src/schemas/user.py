from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """User role enum"""
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    USER = "user"
    VIEWER = "viewer"

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr = Field(..., description="User email")
    full_name: str = Field(..., min_length=2, max_length=100, description="User full name")
    is_active: bool = Field(default=True, description="User active status")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    phone: Optional[str] = Field(None, max_length=20, description="User phone number")
    timezone: Optional[str] = Field(default="UTC", description="User timezone")
    language: Optional[str] = Field(default="en", description="User preferred language")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User preferences")

class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=6, description="User password")
    organization_id: Optional[int] = Field(None, description="Organization ID")

class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User full name")
    is_active: Optional[bool] = Field(None, description="User active status")
    role: Optional[UserRole] = Field(None, description="User role")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    phone: Optional[str] = Field(None, max_length=20, description="User phone number")
    timezone: Optional[str] = Field(None, description="User timezone")
    language: Optional[str] = Field(None, description="User preferred language")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")

class UserInDBBase(UserBase):
    """Base user schema with database fields"""
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    organization_id: Optional[int] = Field(None, description="Organization ID")
    is_verified: bool = Field(default=False, description="Email verification status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """User schema for API responses"""
    permissions: Optional[List[str]] = Field(default_factory=list, description="User permissions based on role")
    
    @classmethod
    def get_permissions_for_role(cls, role: UserRole) -> List[str]:
        """Get permissions based on user role"""
        role_permissions = {
            UserRole.SUPER_ADMIN: [
                'full_access', 'system_config', 'user_management', 
                'organization_management', 'read_all_data', 'create_users', 
                'manage_system', 'delete_data', 'view_analytics'
            ],
            UserRole.ORG_ADMIN: [
                'manage_organization', 'create_users', 'view_analytics',
                'read_org_data', 'manage_org_users', 'org_settings'
            ],
            UserRole.USER: [
                'read_own_data', 'create_conversations', 'manage_own_chatbots',
                'upload_files', 'basic_analytics'
            ],
            UserRole.VIEWER: [
                'read_only', 'view_conversations', 'view_chatbots'
            ]
        }
        return role_permissions.get(role, [])

class UserRegistrationResponse(BaseModel):
    """User registration response schema"""
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="User full name")
    is_active: bool = Field(default=True, description="User active status")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    organization_id: Optional[int] = Field(None, description="Organization ID")
    is_verified: bool = Field(default=False, description="Email verification status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True
        
    # No need for custom model_validate since updated_at is now optional

class UserInDB(UserInDBBase):
    """User schema with password hash"""
    hashed_password: str = Field(..., description="Hashed password")

class UserProfile(BaseModel):
    """User profile schema"""
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    role: UserRole = Field(..., description="User role")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    phone: Optional[str] = Field(None, description="User phone number")
    timezone: str = Field(..., description="User timezone")
    language: str = Field(..., description="User preferred language")
    preferences: Dict[str, Any] = Field(..., description="User preferences")
    organization_id: Optional[int] = Field(None, description="Organization ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    login_count: int = Field(..., description="Login count")

    class Config:
        from_attributes = True

class UserList(BaseModel):
    """User list schema"""
    users: list[User] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")

class UserStats(BaseModel):
    """User statistics schema"""
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    new_users_this_month: int = Field(..., description="New users this month")
    users_by_role: Dict[str, int] = Field(..., description="Users grouped by role")
    recent_logins: int = Field(..., description="Recent logins (last 7 days)")

class UserActivity(BaseModel):
    """User activity schema"""
    user_id: int = Field(..., description="User ID")
    action: str = Field(..., description="Action performed")
    resource: Optional[str] = Field(None, description="Resource affected")
    resource_id: Optional[int] = Field(None, description="Resource ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    timestamp: datetime = Field(..., description="Action timestamp")
    ip_address: Optional[str] = Field(None, description="User IP address")
    user_agent: Optional[str] = Field(None, description="User agent")

    class Config:
        from_attributes = True