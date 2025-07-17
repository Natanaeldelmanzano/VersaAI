from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from src.api.deps import get_db
from src.models.chatbot import Chatbot as ChatbotModel
from src.models.user import User
from src.models.knowledge_base import KnowledgeBase
from src.schemas.chatbot import (
    ChatbotCreate, ChatbotUpdate, ChatbotResponse,
    ChatbotList, ChatbotStats, ChatbotConfig,
    ChatbotTraining,
    ChatbotAISettings,
    ChatbotAppearance,
    ChatbotWidgetSettings,
    ChatbotBehaviorSettings,
    ChatbotStatus
)
from src.api.deps import (
    get_current_active_user,
    get_current_org_admin,
    check_organization_access,
    validate_organization_limits
)
from src.services.chatbot_service import ChatbotService
from src.services.ai_service import AIService

router = APIRouter()
chatbot_service = ChatbotService()
ai_service = AIService()

@router.get("/", response_model=ChatbotList)
async def get_chatbots(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    status_filter: Optional[ChatbotStatus] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of chatbots for the current user's organization
    """
    try:
        query = db.query(ChatbotModel).filter(
            ChatbotModel.organization_id == current_user.organization_id
        )
        
        # Apply filters
        if search:
            search_filter = or_(
                ChatbotModel.name.ilike(f"%{search}%"),
                ChatbotModel.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Note: status_filter removed as Chatbot model doesn't have status field
        # if status_filter:
        #     query = query.filter(ChatbotModel.status == status_filter)
        
        if is_active is not None:
            query = query.filter(ChatbotModel.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        chatbots = query.offset(skip).limit(limit).all()
        
        # Calcular páginas
        pages = (total + limit - 1) // limit if limit > 0 else 1
        page = (skip // limit) + 1 if limit > 0 else 1
        
        # Convert to ChatbotWithStats format
        chatbots_with_stats = []
        for chatbot in chatbots:
            chatbot_dict = {
                "id": chatbot.id,
                "widget_id": chatbot.widget_id,
                "name": chatbot.name,
                "description": chatbot.description,
                "organization_id": chatbot.organization_id,
                "created_by_id": chatbot.created_by_id,
                "knowledge_base_id": chatbot.knowledge_base_id,
                "is_public": chatbot.is_public,
                "model_name": chatbot.model_name,
                "temperature": chatbot.temperature,
                "max_tokens": chatbot.max_tokens,
                "system_prompt": chatbot.system_prompt,
                "avatar_url": chatbot.avatar_url,
                "primary_color": chatbot.primary_color,
                "secondary_color": chatbot.secondary_color,
                "welcome_message": chatbot.welcome_message,
                "widget_position": chatbot.widget_position,
                "widget_size": chatbot.widget_size,
                "show_branding": chatbot.show_branding,
                "auto_suggestions": chatbot.auto_suggestions,
                "fallback_message": chatbot.fallback_message,
                "max_conversation_length": chatbot.max_conversation_length,
                "collect_analytics": chatbot.collect_analytics,
                "collect_feedback": chatbot.collect_feedback,
                "settings": chatbot.settings,
                "created_at": chatbot.created_at,
                "updated_at": chatbot.updated_at,
                "last_trained": chatbot.last_trained,
                "total_conversations": 0,
                "active_conversations": 0,
                "total_messages": 0,
                "avg_response_time": 0.0,
                "user_satisfaction": 0.0,
                "last_conversation_at": None
            }
            chatbots_with_stats.append(chatbot_dict)
        
        return ChatbotList(
            chatbots=chatbots_with_stats,
            total=total,
            page=page,
            per_page=limit,
            pages=pages
        )
        
    except Exception as e:
        import traceback
        print(f"ERROR in get_chatbots: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chatbots: {str(e)}"
        )

@router.get("/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(
    chatbot_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get chatbot by ID
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        return chatbot
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chatbot"
        )

@router.post("/", response_model=ChatbotResponse, status_code=status.HTTP_201_CREATED)
async def create_chatbot(
    chatbot_create: ChatbotCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create new chatbot
    """
    try:
        # Check if chatbot name already exists in organization
        existing_chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.name == chatbot_create.name,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if existing_chatbot:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chatbot name already exists in your organization"
            )
        
        # Create chatbot
        chatbot_data = chatbot_create.dict()
        chatbot_data["organization_id"] = current_user.organization_id
        chatbot_data["created_by_id"] = current_user.id
        
        # Generate widget_id if not provided
        if not chatbot_data.get("widget_id"):
            import uuid
            chatbot_data["widget_id"] = str(uuid.uuid4())
        
        new_chatbot = ChatbotModel(**chatbot_data)
        db.add(new_chatbot)
        db.commit()
        db.refresh(new_chatbot)
        
        return new_chatbot
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error creating chatbot: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chatbot: {str(e)}"
        )

@router.put("/{chatbot_id}", response_model=ChatbotResponse)
async def update_chatbot(
    chatbot_id: int,
    chatbot_update: ChatbotUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update chatbot
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check if new name already exists
        if chatbot_update.name and chatbot_update.name != chatbot.name:
            existing_chatbot = db.query(ChatbotModel).filter(
                and_(
                    ChatbotModel.name == chatbot_update.name,
                    ChatbotModel.organization_id == current_user.organization_id,
                    ChatbotModel.id != chatbot_id
                )
            ).first()
            
            if existing_chatbot:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Chatbot name already exists in your organization"
                )
        
        # Update chatbot fields
        for field, value in chatbot_update.dict(exclude_unset=True).items():
            setattr(chatbot, field, value)
        
        chatbot.updated_by_id = current_user.id
        db.commit()
        db.refresh(chatbot)
        
        return chatbot
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update chatbot"
        )

@router.delete("/{chatbot_id}")
async def delete_chatbot(
    chatbot_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete chatbot
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Soft delete (deactivate) instead of hard delete
        chatbot.is_active = False
        chatbot.status = ChatbotStatus.INACTIVE
        chatbot.updated_by_id = current_user.id
        db.commit()
        
        return {"message": "Chatbot deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chatbot"
        )

@router.post("/{chatbot_id}/train")
async def train_chatbot(
    chatbot_id: int,
    training_data: ChatbotTraining,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Train chatbot with provided data
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Update chatbot status to training
        chatbot.status = ChatbotStatus.TRAINING
        chatbot.updated_by_id = current_user.id
        db.commit()
        
        # Start training process (async)
        await chatbot_service.train_chatbot(chatbot, training_data)
        
        return {"message": "Chatbot training started successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start chatbot training"
        )

@router.post("/{chatbot_id}/upload-documents")
async def upload_training_documents(
    chatbot_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload training documents for chatbot
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Process uploaded files
        uploaded_files = await chatbot_service.process_training_documents(
            chatbot, files
        )
        
        return {
            "message": "Documents uploaded successfully",
            "files": uploaded_files
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload training documents"
        )

# @router.post("/{chatbot_id}/deploy")
# async def deploy_chatbot(
#     chatbot_id: int,
#     deployment_config: dict,  # ChatbotDeployment not defined
#     current_user: User = Depends(get_current_active_user),
#     db: Session = Depends(get_db)
# ):
#     """
#     Deploy chatbot to production
#     """
#     try:
#         chatbot = db.query(Chatbot).filter(
#             and_(
#                 Chatbot.id == chatbot_id,
#                 Chatbot.organization_id == current_user.organization_id
#             )
#         ).first()
#         
#         if not chatbot:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Chatbot not found"
#             )
#         
#         if chatbot.status != ChatbotStatus.TRAINED:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Chatbot must be trained before deployment"
#             )
#         
#         # Deploy chatbot
#         deployment_result = await chatbot_service.deploy_chatbot(
#             chatbot, deployment_config
#         )
#         
#         # Update chatbot status
#         chatbot.status = ChatbotStatus.DEPLOYED
#         chatbot.is_active = True
#         chatbot.updated_by = current_user.id
#         db.commit()
#         
#         return {
#             "message": "Chatbot deployed successfully",
#             "deployment": deployment_result
#         }
#         
#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to deploy chatbot"
#         )

@router.post("/{chatbot_id}/test")
async def test_chatbot(
    chatbot_id: int,
    message: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Test chatbot with a message
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Generate response using AI service
        response = await ai_service.generate_response(
            chatbot, message, test_mode=True
        )
        
        return {
            "message": message,
            "response": response,
            "timestamp": "2024-01-01T00:00:00Z"  # Current timestamp
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to test chatbot"
        )

@router.get("/{chatbot_id}/stats", response_model=ChatbotStats)
async def get_chatbot_stats(
    chatbot_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get chatbot statistics
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Get chatbot statistics
        stats = await chatbot_service.get_chatbot_stats(chatbot)
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chatbot statistics"
        )

@router.get("/{chatbot_id}/config", response_model=ChatbotConfig)
async def get_chatbot_config(
    chatbot_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get chatbot configuration
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        return chatbot.config or {}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chatbot configuration"
        )

@router.put("/{chatbot_id}/config", response_model=ChatbotConfig)
async def update_chatbot_config(
    chatbot_id: int,
    config: ChatbotConfig,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update chatbot configuration
    """
    try:
        chatbot = db.query(ChatbotModel).filter(
            and_(
                ChatbotModel.id == chatbot_id,
                ChatbotModel.organization_id == current_user.organization_id
            )
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Update configuration
        chatbot.config = config.dict()
        chatbot.updated_by_id = current_user.id
        db.commit()
        
        return chatbot.config
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update chatbot configuration"
        )

@router.post("/", response_model=ChatbotResponse, status_code=status.HTTP_201_CREATED)
def create_chatbot(
    chatbot_data: ChatbotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a new chatbot in the current user's organization.
    """
    try:
        # Check organization limits
        organization = validate_organization_limits(db, current_user.organization_id, "chatbots")
        
        # Check if chatbot name already exists in the organization
        existing_chatbot = db.query(ChatbotModel).filter(
            ChatbotModel.name == chatbot_data.name,
            ChatbotModel.organization_id == current_user.organization_id
        ).first()
        
        if existing_chatbot:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chatbot name already exists in this organization"
            )
        
        # Create chatbot
        chatbot_dict = chatbot_data.dict()
        chatbot_dict["organization_id"] = current_user.organization_id
        chatbot_dict["created_by_id"] = current_user.id
        
        chatbot = ChatbotModel(**chatbot_dict)
        db.add(chatbot)
        db.commit()
        db.refresh(chatbot)
        
        return chatbot
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot creation failed: {str(e)}"
        )

@router.get("/{chatbot_id}", response_model=ChatbotResponse)
def read_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get chatbot by ID with statistics.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Add statistics
        stats = {
            "total_conversations": len(chatbot.conversations),
            "active_conversations": len([c for c in chatbot.conversations if c.is_active]),
            "total_messages": sum(len(c.messages) for c in chatbot.conversations),
            "avg_response_time_ms": 0,  # Calculate from message metadata
            "satisfaction_rating": 0,  # Calculate from conversation ratings
            "knowledge_bases_count": 1 if chatbot.knowledge_base else 0
        }
        
        # Convert to dict and add stats
        chatbot_dict = {
            **chatbot.__dict__,
            **stats
        }
        
        return chatbot_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chatbot: {str(e)}"
        )

@router.put("/{chatbot_id}", response_model=ChatbotResponse)
def update_chatbot(
    chatbot_id: int,
    chatbot_update: ChatbotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update chatbot by ID.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Check if name is already taken by another chatbot in the organization
        if chatbot_update.name:
            existing_chatbot = db.query(ChatbotModel).filter(
                ChatbotModel.name == chatbot_update.name,
                ChatbotModel.organization_id == chatbot.organization_id,
                ChatbotModel.id != chatbot_id
            ).first()
            if existing_chatbot:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Chatbot name already exists in this organization"
                )
        
        # Update chatbot
        for field, value in chatbot_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(chatbot, field, value)
        
        db.commit()
        db.refresh(chatbot)
        
        return chatbot
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot update failed: {str(e)}"
        )

@router.delete("/{chatbot_id}")
def delete_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete chatbot by ID.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Soft delete (deactivate) instead of hard delete
        chatbot.is_active = False
        db.commit()
        
        return {"message": "Chatbot deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot deletion failed: {str(e)}"
        )

@router.get("/{chatbot_id}/config", response_model=ChatbotConfig)
def get_chatbot_config(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get chatbot configuration for widget embedding.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        return chatbot.get_widget_config()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chatbot config: {str(e)}"
        )

@router.put("/{chatbot_id}/ai-settings", response_model=ChatbotAISettings)
def update_chatbot_ai_settings(
    chatbot_id: int,
    ai_settings: ChatbotAISettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update chatbot AI settings.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Update AI settings
        for field, value in ai_settings.dict(exclude_unset=True).items():
            if value is not None:
                setattr(chatbot, field, value)
        
        db.commit()
        db.refresh(chatbot)
        
        return {
            "model_name": chatbot.model_name,
            "temperature": chatbot.temperature,
            "max_tokens": chatbot.max_tokens,
            "system_prompt": chatbot.system_prompt
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI settings update failed: {str(e)}"
        )

@router.put("/{chatbot_id}/appearance", response_model=ChatbotAppearance)
def update_chatbot_appearance(
    chatbot_id: int,
    appearance: ChatbotAppearance,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update chatbot appearance settings.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Update appearance settings
        for field, value in appearance.dict(exclude_unset=True).items():
            if value is not None:
                setattr(chatbot, field, value)
        
        db.commit()
        db.refresh(chatbot)
        
        return {
            "avatar_url": chatbot.avatar_url,
            "primary_color": chatbot.primary_color,
            "secondary_color": chatbot.secondary_color,
            "welcome_message": chatbot.welcome_message
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Appearance update failed: {str(e)}"
        )

@router.put("/{chatbot_id}/widget-settings", response_model=ChatbotWidgetSettings)
def update_chatbot_widget_settings(
    chatbot_id: int,
    widget_settings: ChatbotWidgetSettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update chatbot widget settings.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Update widget settings
        for field, value in widget_settings.dict(exclude_unset=True).items():
            if value is not None:
                setattr(chatbot, field, value)
        
        db.commit()
        db.refresh(chatbot)
        
        return {
            "widget_position": chatbot.widget_position,
            "widget_size": chatbot.widget_size,
            "show_branding": chatbot.show_branding
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Widget settings update failed: {str(e)}"
        )

@router.put("/{chatbot_id}/behavior-settings", response_model=ChatbotBehaviorSettings)
def update_chatbot_behavior_settings(
    chatbot_id: int,
    behavior_settings: ChatbotBehaviorSettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update chatbot behavior settings.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Update behavior settings
        for field, value in behavior_settings.dict(exclude_unset=True).items():
            if value is not None:
                setattr(chatbot, field, value)
        
        db.commit()
        db.refresh(chatbot)
        
        return {
            "auto_suggestions": chatbot.auto_suggestions,
            "fallback_message": chatbot.fallback_message,
            "max_conversation_length": chatbot.max_conversation_length,
            "collect_analytics": chatbot.collect_analytics,
            "collect_feedback": chatbot.collect_feedback
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Behavior settings update failed: {str(e)}"
        )

@router.post("/{chatbot_id}/activate")
def activate_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Activate chatbot.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        chatbot.is_active = True
        chatbot.status = ChatbotStatus.ACTIVE
        db.commit()
        
        return {"message": "Chatbot activated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot activation failed: {str(e)}"
        )

@router.post("/{chatbot_id}/deactivate")
def deactivate_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Deactivate chatbot.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        chatbot.is_active = False
        chatbot.status = ChatbotStatus.INACTIVE
        db.commit()
        
        return {"message": "Chatbot deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot deactivation failed: {str(e)}"
        )

@router.get("/{chatbot_id}/knowledge-bases", response_model=List[dict])
def get_chatbot_knowledge_bases(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get knowledge bases associated with the chatbot.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        return [{
            "id": kb.id,
            "name": kb.name,
            "description": kb.description,
            "document_count": len(kb.documents),
            "status": kb.status
        } for kb in chatbot.knowledge_bases]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve knowledge bases: {str(e)}"
        )

@router.post("/{chatbot_id}/knowledge-bases/{kb_id}")
def add_knowledge_base_to_chatbot(
    chatbot_id: int,
    kb_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Add knowledge base to chatbot.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        knowledge_base = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Add knowledge base to chatbot
        if knowledge_base not in chatbot.knowledge_bases:
            chatbot.knowledge_bases.append(knowledge_base)
            db.commit()
        
        return {"message": "Knowledge base added to chatbot successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add knowledge base: {str(e)}"
        )

@router.delete("/{chatbot_id}/knowledge-bases/{kb_id}")
def remove_knowledge_base_from_chatbot(
    chatbot_id: int,
    kb_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Remove knowledge base from chatbot.
    """
    try:
        chatbot = db.query(ChatbotModel).filter(ChatbotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        knowledge_base = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        # Check access permissions
        check_organization_access(current_user, chatbot.organization_id)
        
        # Remove knowledge base from chatbot
        if knowledge_base in chatbot.knowledge_bases:
            chatbot.knowledge_bases.remove(knowledge_base)
            db.commit()
        
        return {"message": "Knowledge base removed from chatbot successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove knowledge base: {str(e)}"
        )