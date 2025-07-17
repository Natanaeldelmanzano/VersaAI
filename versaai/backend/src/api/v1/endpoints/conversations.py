from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from datetime import datetime

from src.api.deps import (
    get_db,
    get_current_user,
    get_current_active_user,
    get_optional_current_user,
    check_organization_access
)
from src.models.user import User, UserRole
from src.models.chatbot import Chatbot
from src.models.conversation import Conversation, Message, ConversationStatus, MessageType, MessageStatus
from src.schemas.conversation import (
    Conversation as ConversationSchema,
    ConversationCreate,
    ConversationUpdate,
    ConversationWithMessages,
    ConversationWithLastMessage,
    ConversationList,
    ConversationStats,
    Message as MessageSchema,
    MessageCreate,
    MessageUpdate,
    MessageWithSources,
    ChatRequest,
    ChatResponse,
    ConversationRating,
    ConversationExport,
    MessageSearch,
    MessageSearchResult
)
from src.services.ai_service import ai_service
import time

router = APIRouter()

@router.get("/", response_model=List[ConversationSchema])
def read_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0, description="Number of conversations to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of conversations to return"),
    chatbot_id: Optional[int] = Query(None, description="Filter by chatbot ID"),
    status: Optional[ConversationStatus] = Query(None, description="Filter by conversation status"),
    search: Optional[str] = Query(None, description="Search conversations by title or content")
) -> Any:
    """
    Retrieve conversations from the current user's organization.
    """
    try:
        query = db.query(Conversation).join(Chatbot)
        
        # Filter by organization
        if current_user.role != UserRole.SUPER_ADMIN:
            query = query.filter(Chatbot.organization_id == current_user.organization_id)
        
        # Apply filters
        if chatbot_id:
            query = query.filter(Conversation.chatbot_id == chatbot_id)
        
        if status:
            query = query.filter(Conversation.status == status)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Conversation.title.ilike(search_filter)) |
                (Conversation.summary.ilike(search_filter))
            )
        
        # Order by most recent
        query = query.order_by(Conversation.updated_at.desc())
        
        # Apply pagination
        conversations = query.offset(skip).limit(limit).all()
        
        return conversations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversations: {str(e)}"
        )

@router.post("/", response_model=ConversationSchema, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Create a new conversation. Can be used by authenticated users or anonymously.
    """
    try:
        # Verify chatbot exists and is active
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == conversation_data.chatbot_id,
            Chatbot.is_active == True
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found or inactive"
            )
        
        # Create conversation
        from datetime import datetime
        now = datetime.utcnow()
        conversation = Conversation(
            chatbot_id=conversation_data.chatbot_id,
            user_id=current_user.id if current_user else conversation_data.user_id,
            session_id=conversation_data.session_id,
            title=conversation_data.title or "New Conversation",
            extra_data=conversation_data.metadata or {},
            created_at=now,
            updated_at=now
        )
        
        # Handle user_info for anonymous users
        if conversation_data.user_info:
            user_info = conversation_data.user_info
            conversation.user_name = user_info.get('name')
            conversation.user_email = user_info.get('email')
            # Note: user_phone doesn't exist in the model, so we'll store it in extra_data
            if 'phone' in user_info:
                if not conversation.extra_data:
                    conversation.extra_data = {}
                conversation.extra_data['user_phone'] = user_info['phone']
        
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return conversation
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversation creation failed: {str(e)}"
        )

@router.get("/{conversation_id}", response_model=ConversationWithMessages)
def read_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Get conversation by ID with all messages.
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Check access permissions
        if current_user:
            if current_user.role != UserRole.SUPER_ADMIN:
                # Check if user owns the conversation or belongs to the same organization
                if (conversation.user_id != current_user.id and 
                    conversation.chatbot.organization_id != current_user.organization_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied"
                    )
        else:
            # For anonymous users, check session_id if provided
            # This would require session validation logic
            pass
        
        # Load messages
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
        
        # Convert to response format
        conversation_dict = conversation.__dict__.copy()
        conversation_dict['messages'] = messages
        
        return conversation_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation: {str(e)}"
        )

@router.put("/{conversation_id}", response_model=ConversationSchema)
def update_conversation(
    conversation_id: int,
    conversation_update: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update conversation by ID.
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Check access permissions
        if current_user.role != UserRole.SUPER_ADMIN:
            if (conversation.user_id != current_user.id and 
                conversation.chatbot.organization_id != current_user.organization_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        # Update conversation
        for field, value in conversation_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(conversation, field, value)
        
        db.commit()
        db.refresh(conversation)
        
        return conversation
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversation update failed: {str(e)}"
        )

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete conversation by ID.
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Check access permissions
        if current_user.role != UserRole.SUPER_ADMIN:
            if (conversation.user_id != current_user.id and 
                conversation.chatbot.organization_id != current_user.organization_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
        
        # Soft delete (archive) instead of hard delete
        conversation.status = ConversationStatus.ARCHIVED
        db.commit()
        
        return {"message": "Conversation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversation deletion failed: {str(e)}"
        )

@router.post("/{conversation_id}/messages", response_model=MessageSchema, status_code=status.HTTP_201_CREATED)
def create_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Create a new message in a conversation.
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Check if conversation is active
        if conversation.status != ConversationStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot add messages to inactive conversation"
            )
        
        from datetime import datetime
        
        # Create user message
        user_message = Message(
            conversation_id=conversation_id,
            content=message_data.content,
            message_type=MessageType.USER,
            status=MessageStatus.SENT,
            extra_data=message_data.metadata or {},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        return user_message
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Message creation failed: {str(e)}"
        )

@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Send a message and get AI response.
    """
    try:
        # Get or create conversation
        conversation = None
        if chat_request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == chat_request.conversation_id
            ).first()
        
        if not conversation:
            # Create new conversation - require chatbot_id for new conversations
            if not chat_request.chatbot_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="chatbot_id is required for new conversations"
                )
            
            chatbot = db.query(Chatbot).filter(
                Chatbot.id == chat_request.chatbot_id,
                Chatbot.is_active == True
            ).first()
            
            if not chatbot:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chatbot not found or inactive"
                )
            
            # Check if user has access to this chatbot
            if current_user and current_user.organization_id != chatbot.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this chatbot"
                )
            
            conversation = Conversation(
                chatbot_id=chat_request.chatbot_id,
                user_id=current_user.id if current_user else None,
                session_id=chat_request.session_id,
                title="New Conversation"
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Create user message
        user_message = Message(
            conversation_id=conversation.id,
            content=chat_request.message,
            message_type=MessageType.USER,
            status=MessageStatus.SENT
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Generate AI response
        chatbot = conversation.chatbot
        start_time = time.time()
        
        # Get conversation history for context
        recent_messages = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.desc()).limit(10).all()
        
        conversation_history = []
        for msg in reversed(recent_messages):
            role = "user" if msg.message_type == MessageType.USER else "assistant"
            conversation_history.append({"role": role, "content": msg.content})
        
        # Generate AI response using the unified ai_service
        ai_response = await ai_service.generate_response(
            message=chat_request.message,
            chatbot=chatbot,
            conversation_history=conversation_history,
            db=db
        )
        
        response_time_ms = (time.time() - start_time) * 1000
        sources = ai_response.get("sources", [])
        
        # Create assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            content=ai_response["response"],
            message_type=MessageType.ASSISTANT,
            status=MessageStatus.SENT,
            ai_model=ai_response.get("metadata", {}).get("model", "unknown"),
            ai_tokens_used=ai_response.get("metadata", {}).get("tokens_used"),
            ai_response_time_ms=response_time_ms,
            sources=sources,
            context=ai_response.get("metadata", {})
        )
        
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        # Update conversation title if it's the first exchange
        if len(conversation.messages) <= 2 and conversation.title == "New Conversation":
            try:
                # Generate a simple title from the first message
                title = chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
                conversation.title = title
                db.commit()
            except:
                pass  # Keep default title if generation fails
        
        return {
            "message": ai_response["response"],
            "conversation_id": conversation.id,
            "message_id": assistant_message.id,
            "sources": sources,
            "confidence_score": ai_response.get("confidence"),
            "response_time_ms": response_time_ms,
            "tokens_used": ai_response.get("metadata", {}).get("tokens_used"),
            "model_used": ai_response.get("metadata", {}).get("model", "unknown")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )

@router.get("/{conversation_id}/messages", response_model=List[MessageSchema])
def read_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    skip: int = Query(0, ge=0, description="Number of messages to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of messages to return")
) -> Any:
    """
    Get messages from a conversation.
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Check access permissions
        if current_user:
            if current_user.role != UserRole.SUPER_ADMIN:
                if (conversation.user_id != current_user.id and 
                    conversation.chatbot.organization_id != current_user.organization_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied"
                    )
        
        # Get messages
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
        
        return messages
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve messages: {str(e)}"
        )

@router.post("/{conversation_id}/close")
def close_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Close a conversation.
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Check access permissions
        if current_user:
            if current_user.role != UserRole.SUPER_ADMIN:
                if (conversation.user_id != current_user.id and 
                    conversation.chatbot.organization_id != current_user.organization_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied"
                    )
        
        conversation.close_conversation()
        db.commit()
        
        return {"message": "Conversation closed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to close conversation: {str(e)}"
        )

@router.post("/{conversation_id}/rate")
def rate_conversation(
    conversation_id: int,
    rating_data: ConversationRating,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    Rate a conversation.
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Update conversation rating
        conversation.rating = rating_data.rating
        conversation.feedback = rating_data.feedback
        db.commit()
        
        return {"message": "Conversation rated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rate conversation: {str(e)}"
        )