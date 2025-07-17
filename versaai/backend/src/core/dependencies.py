from typing import Generator, Optional
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import logging

from .database import get_db
from .config import settings
from ..repositories.user_repository import UserRepository
from ..repositories.chatbot_repository import ChatbotRepository
from ..repositories.conversation_repository import ConversationRepository
from ..repositories.message_repository import MessageRepository
from ..repositories.organization_repository import OrganizationRepository
from ..repositories.knowledge_base_repository import KnowledgeBaseRepository
from ..models.user import User
from ..models.organization import Organization

logger = logging.getLogger(__name__)
security = HTTPBearer()
# settings is already imported from config

# ============================================================================
# Repository Dependencies
# ============================================================================

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Get UserRepository instance"""
    return UserRepository(db)

def get_chatbot_repository(db: Session = Depends(get_db)) -> ChatbotRepository:
    """Get ChatbotRepository instance"""
    return ChatbotRepository(db)

def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    """Get ConversationRepository instance"""
    return ConversationRepository(db)

def get_message_repository(db: Session = Depends(get_db)) -> MessageRepository:
    """Get MessageRepository instance"""
    return MessageRepository(db)

def get_organization_repository(db: Session = Depends(get_db)) -> OrganizationRepository:
    """Get OrganizationRepository instance"""
    return OrganizationRepository(db)

def get_knowledge_base_repository(db: Session = Depends(get_db)) -> KnowledgeBaseRepository:
    """Get KnowledgeBaseRepository instance"""
    return KnowledgeBaseRepository(db)

# ============================================================================
# Authentication Dependencies
# ============================================================================

def get_token_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Extract and validate JWT token payload"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(
    payload: dict = Depends(get_token_payload),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    """Get current authenticated user"""
    try:
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        user = user_repo.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )
        
        return user
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (alias for clarity)"""
    return current_user

def get_current_organization(
    current_user: User = Depends(get_current_user),
    org_repo: OrganizationRepository = Depends(get_organization_repository)
) -> Optional[Organization]:
    """Get current user's organization"""
    if not current_user.organization_id:
        return None
    
    try:
        organization = org_repo.get(current_user.organization_id)
        if not organization or not organization.is_active:
            return None
        return organization
    except Exception as e:
        logger.error(f"Error getting current organization: {str(e)}")
        return None

def require_organization(
    organization: Organization = Depends(get_current_organization)
) -> Organization:
    """Require user to have an active organization"""
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization membership required"
        )
    return organization

# ============================================================================
# Role-based Dependencies
# ============================================================================

def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Require admin role"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def require_manager(
    current_user: User = Depends(get_current_user)
) -> User:
    """Require manager role or higher"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager privileges required"
        )
    return current_user

def require_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Require any authenticated user (alias for clarity)"""
    return current_user

# ============================================================================
# Optional Authentication Dependencies
# ============================================================================

def get_optional_current_user(
    user_repo: UserRepository = Depends(get_user_repository),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        
        user = user_repo.get(user_id)
        if user and user.is_active:
            return user
        return None
    except JWTError:
        return None
    except Exception as e:
        logger.error(f"Error in optional authentication: {str(e)}")
        return None

# ============================================================================
# Resource Access Dependencies
# ============================================================================

def get_user_chatbot(
    chatbot_id: int,
    current_user: User = Depends(get_current_user),
    chatbot_repo: ChatbotRepository = Depends(get_chatbot_repository)
):
    """Get chatbot owned by current user"""
    chatbot = chatbot_repo.get(chatbot_id)
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    # Check ownership or organization access
    if (chatbot.user_id != current_user.id and 
        chatbot.organization_id != current_user.organization_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this chatbot"
        )
    
    return chatbot

def get_user_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    conversation_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """Get conversation accessible by current user"""
    conversation = conversation_repo.get(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Check access through user or organization
    if (conversation.user_id != current_user.id and 
        conversation.chatbot.organization_id != current_user.organization_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this conversation"
        )
    
    return conversation

def get_organization_knowledge_base(
    kb_id: int,
    current_user: User = Depends(get_current_user),
    kb_repo: KnowledgeBaseRepository = Depends(get_knowledge_base_repository)
):
    """Get knowledge base accessible by current user's organization"""
    kb = kb_repo.get(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge base not found"
        )
    
    # Check organization access
    if kb.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this knowledge base"
        )
    
    return kb

# ============================================================================
# Pagination Dependencies
# ============================================================================

def get_pagination_params(
    skip: int = 0,
    limit: int = 100
) -> dict:
    """Get pagination parameters with validation"""
    if skip < 0:
        skip = 0
    if limit <= 0 or limit > 1000:
        limit = 100
    
    return {"skip": skip, "limit": limit}

# ============================================================================
# Search Dependencies
# ============================================================================

def get_search_params(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> dict:
    """Get search parameters with validation"""
    pagination = get_pagination_params(skip, limit)
    
    return {
        "search_term": q.strip() if q else None,
        **pagination
    }

# ============================================================================
# Cache Dependencies
# ============================================================================

@lru_cache()
def get_cached_settings():
    """Get cached application settings"""
    return get_settings()

# ============================================================================
# Utility Dependencies
# ============================================================================

def get_request_id() -> str:
    """Generate unique request ID for tracing"""
    import uuid
    return str(uuid.uuid4())

def get_client_ip(request) -> str:
    """Get client IP address"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

# ============================================================================
# Service Layer Dependencies (for future use)
# ============================================================================

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Get UserService instance (placeholder for service layer)"""
    from ..services.user_service import UserService
    return UserService(user_repo)

def get_chatbot_service(
    chatbot_repo: ChatbotRepository = Depends(get_chatbot_repository)
):
    """Get ChatbotService instance (placeholder for service layer)"""
    from ..services.chatbot_service import ChatbotService
    return ChatbotService(chatbot_repo)

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Get AuthService instance (placeholder for service layer)"""
    from ..services.auth_service import AuthService
    return AuthService(user_repo)