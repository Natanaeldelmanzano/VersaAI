from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from src.api.deps import get_db
from src.models.organization import Organization
from src.models.user import User, UserRole
from src.schemas.organization import (
    OrganizationCreate, OrganizationUpdate, Organization,
    OrganizationList, OrganizationStats, OrganizationWithStats,
    OrganizationSettings, OrganizationSubscriptionUpdate, OrganizationUsage,
    OrganizationStatus, OrganizationBranding
)
from src.api.deps import (
    get_current_active_user,
    get_current_superuser,
    get_current_org_admin
)

router = APIRouter()

@router.get("/", response_model=List[Organization])
def read_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
    skip: int = Query(0, ge=0, description="Number of organizations to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of organizations to return"),
    search: Optional[str] = Query(None, description="Search organizations by name or slug"),
    is_active: Optional[bool] = Query(None, description="Filter by organization status"),
    plan_type: Optional[str] = Query(None, description="Filter by subscription plan")
) -> Any:
    """
    Retrieve organizations. Only accessible by super admins.
    """
    try:
        query = db.query(Organization)
        
        # Apply filters
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Organization.name.ilike(search_filter)) |
                (Organization.slug.ilike(search_filter))
            )
        
        if is_active is not None:
            query = query.filter(Organization.is_active == is_active)
        
        if plan_type:
            query = query.filter(Organization.plan_type == plan_type)
        
        # Apply pagination
        organizations = query.offset(skip).limit(limit).all()
        
        return organizations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve organizations: {str(e)}"
        )

@router.post("/", response_model=Organization, status_code=status.HTTP_201_CREATED)
def create_organization(
    organization_data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new organization. Only accessible by super admins.
    """
    try:
        # Check if organization with same name or slug already exists
        existing_org = db.query(Organization).filter(
            (Organization.name == organization_data.name) |
            (Organization.slug == organization_data.slug)
        ).first()
        
        if existing_org:
            if existing_org.name == organization_data.name:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization name already exists"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization slug already exists"
                )
        
        # Create organization
        organization = Organization(**organization_data.dict())
        db.add(organization)
        db.commit()
        db.refresh(organization)
        
        return organization
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Organization creation failed: {str(e)}"
        )

@router.get("/me", response_model=OrganizationWithStats)
def read_my_organization(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user's organization with statistics.
    """
    try:
        if not current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not associated with any organization"
            )
        
        organization = db.query(Organization).filter(
            Organization.id == current_user.organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Add statistics
        stats = {
            "active_users": organization.get_active_users_count(db),
            "total_chatbots": organization.get_chatbots_count(db),
            "active_chatbots": len([c for c in organization.chatbots if c.is_active]),
            "total_conversations": sum(len(c.conversations) for c in organization.chatbots),
            "total_knowledge_bases": len(organization.knowledge_bases)
        }
        
        # Convert to dict and add stats
        org_dict = {
            **organization.__dict__,
            **stats
        }
        
        return org_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve organization: {str(e)}"
        )

@router.put("/me", response_model=Organization)
def update_my_organization(
    organization_update: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Update current user's organization. Only accessible by organization admins.
    """
    try:
        if not current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not associated with any organization"
            )
        
        organization = db.query(Organization).filter(
            Organization.id == current_user.organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Check if name or slug is already taken by another organization
        if organization_update.name:
            existing_org = db.query(Organization).filter(
                Organization.name == organization_update.name,
                Organization.id != organization.id
            ).first()
            if existing_org:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization name already exists"
                )
        
        if organization_update.slug:
            existing_org = db.query(Organization).filter(
                Organization.slug == organization_update.slug,
                Organization.id != organization.id
            ).first()
            if existing_org:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization slug already exists"
                )
        
        # Update organization (exclude subscription fields for non-super admins)
        update_data = organization_update.dict(exclude_unset=True)
        if current_user.role != UserRole.SUPER_ADMIN:
            # Remove subscription-related fields
            update_data.pop('subscription_plan', None)
            update_data.pop('max_chatbots', None)
            update_data.pop('max_users', None)
            update_data.pop('max_conversations_per_month', None)
            update_data.pop('status', None)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(organization, field, value)
        
        db.commit()
        db.refresh(organization)
        
        return organization
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Organization update failed: {str(e)}"
        )

@router.get("/{organization_id}", response_model=OrganizationWithStats)
def read_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Get organization by ID with statistics. Only accessible by super admins.
    """
    try:
        organization = db.query(Organization).filter(
            Organization.id == organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Add statistics
        stats = {
            "active_users": organization.get_active_users_count(db),
            "total_chatbots": organization.get_chatbots_count(db),
            "active_chatbots": len([c for c in organization.chatbots if c.is_active]),
            "total_conversations": sum(len(c.conversations) for c in organization.chatbots),
            "total_knowledge_bases": len(organization.knowledge_bases)
        }
        
        # Convert to dict and add stats
        org_dict = {
            **organization.__dict__,
            **stats
        }
        
        return org_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve organization: {str(e)}"
        )

@router.put("/{organization_id}", response_model=Organization)
def update_organization(
    organization_id: int,
    organization_update: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Update organization by ID. Only accessible by super admins.
    """
    try:
        organization = db.query(Organization).filter(
            Organization.id == organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Check if name or slug is already taken by another organization
        if organization_update.name:
            existing_org = db.query(Organization).filter(
                Organization.name == organization_update.name,
                Organization.id != organization_id
            ).first()
            if existing_org:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization name already exists"
                )
        
        if organization_update.slug:
            existing_org = db.query(Organization).filter(
                Organization.slug == organization_update.slug,
                Organization.id != organization_id
            ).first()
            if existing_org:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Organization slug already exists"
                )
        
        # Update organization
        for field, value in organization_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(organization, field, value)
        
        db.commit()
        db.refresh(organization)
        
        return organization
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Organization update failed: {str(e)}"
        )

@router.delete("/{organization_id}")
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Delete organization by ID. Only accessible by super admins.
    """
    try:
        organization = db.query(Organization).filter(
            Organization.id == organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Check if organization has users
        users_count = db.query(User).filter(
            User.organization_id == organization_id
        ).count()
        
        if users_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete organization with existing users"
            )
        
        # Soft delete (deactivate) instead of hard delete
        organization.status = OrganizationStatus.INACTIVE
        db.commit()
        
        return {"message": "Organization deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Organization deletion failed: {str(e)}"
        )

@router.put("/{organization_id}/subscription", response_model=Organization)
def update_organization_subscription(
    organization_id: int,
    subscription_update: OrganizationSubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Update organization subscription. Only accessible by super admins.
    """
    try:
        organization = db.query(Organization).filter(
            Organization.id == organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Update subscription
        for field, value in subscription_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(organization, field, value)
        
        db.commit()
        db.refresh(organization)
        
        return organization
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Subscription update failed: {str(e)}"
        )

@router.get("/me/usage", response_model=OrganizationUsage)
def get_organization_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current organization usage statistics.
    """
    try:
        if not current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not associated with any organization"
            )
        
        organization = db.query(Organization).filter(
            Organization.id == current_user.organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Calculate usage
        active_users = organization.get_active_users_count(db)
        total_chatbots = organization.get_chatbots_count(db)
        
        # Calculate conversations this month (simplified)
        total_conversations = sum(len(c.conversations) for c in organization.chatbots)
        
        usage = {
            "current_users": active_users,
            "max_users": organization.max_users,
            "current_chatbots": total_chatbots,
            "max_chatbots": organization.max_chatbots,
            "current_conversations_this_month": total_conversations,
            "max_conversations_per_month": organization.max_conversations_per_month,
            "subscription_plan": organization.subscription_plan,
            "users_percentage": (active_users / organization.max_users * 100) if organization.max_users > 0 else 0,
            "chatbots_percentage": (total_chatbots / organization.max_chatbots * 100) if organization.max_chatbots > 0 else 0,
            "conversations_percentage": (total_conversations / organization.max_conversations_per_month * 100) if organization.max_conversations_per_month > 0 else 0
        }
        
        return usage
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve usage statistics: {str(e)}"
        )

@router.get("/me/branding", response_model=OrganizationBranding)
def get_organization_branding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current organization branding settings.
    """
    try:
        if not current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not associated with any organization"
            )
        
        organization = db.query(Organization).filter(
            Organization.id == current_user.organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        return {
            "logo_url": organization.logo_url,
            "primary_color": organization.primary_color,
            "secondary_color": organization.secondary_color,
            "custom_css": organization.custom_css
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve branding: {str(e)}"
        )

@router.put("/me/branding", response_model=OrganizationBranding)
def update_organization_branding(
    branding_update: OrganizationBranding,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_org_admin)
) -> Any:
    """
    Update current organization branding settings.
    """
    try:
        if not current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not associated with any organization"
            )
        
        organization = db.query(Organization).filter(
            Organization.id == current_user.organization_id
        ).first()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Update branding
        for field, value in branding_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(organization, field, value)
        
        db.commit()
        db.refresh(organization)
        
        return {
            "logo_url": organization.logo_url,
            "primary_color": organization.primary_color,
            "secondary_color": organization.secondary_color,
            "custom_css": organization.custom_css
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Branding update failed: {str(e)}"
        )