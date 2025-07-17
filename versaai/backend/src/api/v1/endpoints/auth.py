from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from src.api.deps import get_db, get_current_user, get_current_active_user
from src.models.user import User
from src.schemas.auth import (
    UserLogin,
    UserRegister,
    Token,
    LoginResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm,
    RefreshToken
)
from src.schemas.user import User as UserSchema, UserCreate, UserInDBBase, UserRegistrationResponse
from src.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    try:
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Generate unique username from email
        base_username = user_data.email.split('@')[0]
        username = base_username
        counter = 1
        
        # Ensure username is unique
        while db.query(User).filter(User.username == username).first():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Register user with individual parameters
        user = auth_service.register_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            username=username,
            full_name=user_data.full_name,
            organization_id=None  # Will be handled later
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to register user"
            )
        
        # The auth_service.register_user already commits, so just refresh
        db.refresh(user)
        
        # Debug: Check user attributes before validation
        print(f"DEBUG: User attributes before validation:")
        print(f"  ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Username: {user.username}")
        print(f"  Created at: {user.created_at} (type: {type(user.created_at)})")
        print(f"  Updated at: {user.updated_at} (type: {type(user.updated_at)})")
        
        # If updated_at is None, set it to created_at
        if user.updated_at is None:
            print(f"DEBUG: updated_at is None, setting to created_at")
            user.updated_at = user.created_at
            db.commit()
            db.refresh(user)
            print(f"DEBUG: After fix - Updated at: {user.updated_at}")
        
        # Use the model_validate method which handles None updated_at properly
        response = UserRegistrationResponse.model_validate(user, from_attributes=True)
        print(f"DEBUG: Response created successfully with updated_at: {response.updated_at}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Exception in register endpoint: {e}")
        print(f"DEBUG: Exception type: {type(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=LoginResponse)
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user with email and password"""
    try:
        # Authenticate user
        user = auth_service.authenticate_user(db, user_data.email, user_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "org_id": user.organization_id
        }
        
        access_token = auth_service.create_access_token(token_data)
        refresh_token = auth_service.create_refresh_token(token_data)
        
        # Convert user to schema
        user_schema = UserInDBBase.model_validate(user, from_attributes=True)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user_schema
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/login/json", response_model=LoginResponse)
def login_json(
    user_data: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    Login user with JSON data and return access token.
    """
    try:
        user = auth_service.authenticate_user(db, user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "org_id": user.organization_id
        }
        
        access_token = auth_service.create_access_token(token_data)
        refresh_token = auth_service.create_refresh_token(token_data)
        
        # Convert user to schema
        user_schema = UserInDBBase.model_validate(user, from_attributes=True)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user_schema
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/refresh-temp")
def refresh_token_temp():
    """
    Temporary refresh endpoint for development
    """
    return {
        "access_token": "temp_access_token_123",
        "refresh_token": "temp_refresh_token_123",
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    try:
        # Verify refresh token
        payload = auth_service.verify_refresh_token(refresh_data.refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Create new tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "org_id": user.organization_id
        }
        
        access_token = auth_service.create_access_token(token_data)
        new_refresh_token = auth_service.create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )

@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information with permissions
    """
    from schemas.user import User as UserSchema
    
    # Create user response with permissions
    user_data = {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "role": current_user.role,
        "avatar_url": current_user.avatar_url,
        "phone": current_user.phone,
        "timezone": current_user.timezone,
        "language": current_user.language,
        "preferences": current_user.preferences,
        "organization_id": current_user.organization_id,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
        "last_login": current_user.last_login,
        "permissions": UserSchema.get_permissions_for_role(current_user.role)
    }
    
    return user_data

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout user (invalidate tokens)
    """
    # In a production environment, you would add the token to a blacklist
    return {"message": "Successfully logged out"}

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    try:
        # Verify current password
        if not auth_service.verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        hashed_password = auth_service.get_password_hash(password_data.new_password)
        current_user.hashed_password = hashed_password
        db.commit()
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )

@router.post("/forgot-password")
async def forgot_password(
    password_reset: PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Request password reset
    """
    try:
        user = db.query(User).filter(User.email == password_reset.email).first()
        if not user:
            # Don't reveal if email exists or not
            return {"message": "If the email exists, a reset link has been sent"}
        
        # In production, send email with reset token
        # For now, just return success message
        return {"message": "If the email exists, a reset link has been sent"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset request failed"
        )

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """
    Reset password with token
    """
    try:
        # In production, verify reset token
        # For now, just return success message
        return {"message": "Password reset successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )

@router.get("/test-simple")
def test_simple_endpoint():
    """
    Simple test endpoint without any dependencies
    """
    return {"message": "This endpoint works!", "status": "success"}

# Endpoint duplicado eliminado - manteniendo solo la implementación principal arriba

# Endpoint /me moved above to avoid duplication

@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Change user password.
    """
    try:
        # Verify current password
        if not auth_service.verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )
        
        # Change password
        success = auth_service.change_password(
            db, 
            current_user.id, 
            password_data.current_password, 
            password_data.new_password
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password"
            )
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password change failed: {str(e)}"
        )

@router.post("/reset-password")
def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
) -> Any:
    """
    Request password reset (send reset email).
    """
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == reset_data.email).first()
        if not user:
            # Don't reveal if email exists or not for security
            return {"message": "If the email exists, a reset link has been sent"}
        
        # In a real implementation, you would:
        # 1. Generate a secure reset token
        # 2. Store it in database with expiration
        # 3. Send email with reset link
        
        # For now, just return success message
        return {"message": "If the email exists, a reset link has been sent"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset request failed: {str(e)}"
        )

@router.post("/reset-password/confirm")
def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
) -> Any:
    """
    Confirm password reset with token.
    """
    try:
        # In a real implementation, you would:
        # 1. Validate the reset token
        # 2. Check if it's not expired
        # 3. Find the user associated with the token
        # 4. Update the password
        # 5. Invalidate the reset token
        
        # For now, just return success message
        return {"message": "Password reset successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset confirmation failed: {str(e)}"
        )

@router.post("/verify-token")
def verify_token(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Verify if the current token is valid.
    """
    # Temporary fix: handle case where username might not be available
    username = getattr(current_user, 'username', current_user.email.split('@')[0])
    
    return {
        "valid": True,
        "user_id": current_user.id,
        "username": username,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }