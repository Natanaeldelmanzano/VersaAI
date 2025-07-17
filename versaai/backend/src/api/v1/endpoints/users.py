from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from src.api.deps import (
    get_db,
    get_current_user,
    get_current_active_user,
    get_current_superuser,
    get_current_org_admin,
    get_current_user_organization,
    check_organization_access
)
from src.models.user import User, UserRole
from src.models.organization import Organization
from src.schemas.user import (
    User as UserSchema,
    UserCreate,
    UserUpdate,
    UserList,
    UserProfile,
    UserStats,
    UserActivity
)
from src.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin),
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    search: Optional[str] = Query(None, description="Search users by name, username, or email"),
    role: Optional[UserRole] = Query(None, description="Filter by user role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
) -> Any:
    """
    Retrieve users. Organization admins can only see users from their organization.
    """
    try:
        query = db.query(User)
        
        # If not super admin, filter by organization
        if current_user.role != UserRole.SUPER_ADMIN:
            query = query.filter(User.organization_id == current_user.organization_id)
        
        # Apply filters
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (User.full_name.ilike(search_filter)) |
                (User.username.ilike(search_filter)) |
                (User.email.ilike(search_filter))
            )
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Apply pagination
        users = query.offset(skip).limit(limit).all()
        
        return users
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Create a new user. Organization admins can only create users in their organization.
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Set organization for non-super admins
        if current_user.role != UserRole.SUPER_ADMIN:
            user_data.organization_id = current_user.organization_id
        
        # Validate role assignment
        if user_data.role == UserRole.SUPER_ADMIN and current_user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only super admins can create super admin users"
            )
        
        # Create user
        user = auth_service.create_user(db, user_data)
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User creation failed: {str(e)}"
        )

@router.get("/me", response_model=UserProfile)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user profile.
    """
    return current_user

@router.put("/me", response_model=UserProfile)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update current user profile.
    """
    try:
        # Users can't change their own role or organization
        user_update.role = None
        user_update.organization_id = None
        user_update.is_active = None
        
        # Check if email/username is already taken by another user
        if user_update.email:
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        if user_update.username:
            existing_user = db.query(User).filter(
                User.username == user_update.username,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Update user
        for field, value in user_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update failed: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get user by ID. Users can only access users from their organization.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check access permissions
        if current_user.role != UserRole.SUPER_ADMIN:
            if user.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        )

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Update user by ID. Organization admins can only update users from their organization.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check access permissions
        if current_user.role != UserRole.SUPER_ADMIN:
            if user.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            # Non-super admins can't change organization or create super admins
            user_update.organization_id = None
            if user_update.role == UserRole.SUPER_ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only super admins can assign super admin role"
                )
        
        # Check if email/username is already taken by another user
        if user_update.email:
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        if user_update.username:
            existing_user = db.query(User).filter(
                User.username == user_update.username,
                User.id != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Update user
        for field, value in user_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User update failed: {str(e)}"
        )

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Delete user by ID. Organization admins can only delete users from their organization.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check access permissions
        if current_user.role != UserRole.SUPER_ADMIN:
            if user.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        # Prevent self-deletion
        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        # Prevent deletion of super admins by non-super admins
        if user.role == UserRole.SUPER_ADMIN and current_user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only super admins can delete super admin users"
            )
        
        # Soft delete (deactivate) instead of hard delete
        user.is_active = False
        db.commit()
        
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User deletion failed: {str(e)}"
        )

@router.post("/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Activate user by ID.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check access permissions
        if current_user.role != UserRole.SUPER_ADMIN:
            if user.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        user.is_active = True
        db.commit()
        
        return {"message": "User activated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User activation failed: {str(e)}"
        )

@router.post("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Deactivate user by ID.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check access permissions
        if current_user.role != UserRole.SUPER_ADMIN:
            if user.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        # Prevent self-deactivation
        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate your own account"
            )
        
        user.is_active = False
        db.commit()
        
        return {"message": "User deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User deactivation failed: {str(e)}"
        )

@router.get("/stats/overview", response_model=UserStats)
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Get user statistics for the organization.
    """
    try:
        query = db.query(User)
        
        # Filter by organization for non-super admins
        if current_user.role != UserRole.SUPER_ADMIN:
            query = query.filter(User.organization_id == current_user.organization_id)
        
        total_users = query.count()
        active_users = query.filter(User.is_active == True).count()
        inactive_users = total_users - active_users
        
        # Count by role
        role_counts = {}
        for role in UserRole:
            count = query.filter(User.role == role).count()
            role_counts[role.value] = count
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,
            "role_distribution": role_counts
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user statistics: {str(e)}"
        )