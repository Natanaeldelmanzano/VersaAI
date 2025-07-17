from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .user import UserInDBBase

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")

class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")
    full_name: str = Field(..., min_length=2, max_length=100, description="User full name")
    organization_name: Optional[str] = Field(None, max_length=100, description="Organization name for new org")
    organization_slug: Optional[str] = Field(None, max_length=50, description="Organization slug for new org")

class Token(BaseModel):
    """Token response schema"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")

class LoginResponse(BaseModel):
    """Login response schema with user data"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserInDBBase = Field(..., description="User data")

class TokenData(BaseModel):
    """Token data schema"""
    user_id: Optional[int] = None
    email: Optional[str] = None

class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")

class PasswordReset(BaseModel):
    """Password reset request schema"""
    email: EmailStr = Field(..., description="User email")

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=8, description="New password")

class RefreshToken(BaseModel):
    """Refresh token schema"""
    refresh_token: str = Field(..., description="Refresh token")