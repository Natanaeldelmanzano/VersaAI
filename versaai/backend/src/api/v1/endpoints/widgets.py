from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Any, Optional
import json

from src.api.deps import get_db, get_optional_current_user
from src.models.user import User
from src.models.chatbot import Chatbot
from src.models.organization import Organization
from src.schemas.conversation import ChatRequest, ChatResponse
from src.services.groq_service import GroqService
from src.services.rag_service import RAGService
from src.core.config import settings

router = APIRouter()
groq_service = GroqService()
rag_service = RAGService()

@router.get("/{chatbot_id}/config", response_model=dict)
def get_widget_config(
    chatbot_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get widget configuration for a chatbot.
    This endpoint is public and doesn't require authentication.
    """
    try:
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == chatbot_id,
            Chatbot.is_active == True
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found or inactive"
            )
        
        # Get organization branding
        organization = db.query(Organization).filter(
            Organization.id == chatbot.organization_id
        ).first()
        
        # Build widget configuration
        widget_config = {
            "chatbot_id": chatbot.id,
            "name": chatbot.name,
            "description": chatbot.description,
            "welcome_message": chatbot.welcome_message,
            "placeholder_text": chatbot.placeholder_text,
            "widget_settings": chatbot.widget_settings or {},
            "appearance": chatbot.appearance or {},
            "behavior_settings": chatbot.behavior_settings or {},
            "organization": {
                "name": organization.name if organization else "VersaAI",
                "branding": organization.branding if organization else {}
            },
            "api_endpoint": f"{settings.API_V1_STR}/widgets/{chatbot_id}/chat",
            "websocket_endpoint": f"ws://localhost:8000{settings.API_V1_STR}/widgets/{chatbot_id}/ws"
        }
        
        return widget_config
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve widget configuration: {str(e)}"
        )

@router.get("/{chatbot_id}/embed.js", response_class=HTMLResponse)
def get_widget_embed_script(
    chatbot_id: int,
    db: Session = Depends(get_db),
    theme: Optional[str] = Query("light", description="Widget theme (light, dark, auto)"),
    position: Optional[str] = Query("bottom-right", description="Widget position"),
    language: Optional[str] = Query("en", description="Widget language")
) -> str:
    """
    Get the JavaScript embed script for the widget.
    """
    try:
        # Verify chatbot exists and is active
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == chatbot_id,
            Chatbot.is_active == True
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found or inactive"
            )
        
        # Generate the embed script
        embed_script = f"""
(function() {{
    // VersaAI Widget Embed Script
    var chatbotId = {chatbot_id};
    var apiBase = '{settings.API_V1_STR}';
    var theme = '{theme}';
    var position = '{position}';
    var language = '{language}';
    
    // Create widget container
    var widgetContainer = document.createElement('div');
    widgetContainer.id = 'versaai-widget-' + chatbotId;
    widgetContainer.className = 'versaai-widget-container';
    
    // Add widget styles
    var widgetStyles = `
        .versaai-widget-container {{
            position: fixed;
            z-index: 9999;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        .versaai-widget-button {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }}
        
        .versaai-widget-button:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .versaai-widget-chat {{
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            display: none;
            flex-direction: column;
            overflow: hidden;
            margin-bottom: 20px;
        }}
        
        .versaai-widget-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            font-weight: 600;
        }}
        
        .versaai-widget-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 16px;
        }}
        
        .versaai-widget-input {{
            border-top: 1px solid #e5e7eb;
            padding: 16px;
            display: flex;
            gap: 8px;
        }}
        
        .versaai-widget-input input {{
            flex: 1;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 8px 12px;
            outline: none;
        }}
        
        .versaai-widget-input button {{
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            cursor: pointer;
        }}
        
        .versaai-message {{
            margin-bottom: 12px;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }}
        
        .versaai-message.user {{
            flex-direction: row-reverse;
        }}
        
        .versaai-message-content {{
            max-width: 80%;
            padding: 8px 12px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .versaai-message.user .versaai-message-content {{
            background: #667eea;
            color: white;
        }}
        
        .versaai-message.assistant .versaai-message-content {{
            background: #f3f4f6;
            color: #374151;
        }}
        
        /* Position classes */
        .versaai-widget-container.bottom-right {{
            bottom: 20px;
            right: 20px;
        }}
        
        .versaai-widget-container.bottom-left {{
            bottom: 20px;
            left: 20px;
        }}
        
        .versaai-widget-container.top-right {{
            top: 20px;
            right: 20px;
        }}
        
        .versaai-widget-container.top-left {{
            top: 20px;
            left: 20px;
        }}
        
        /* Dark theme */
        .versaai-widget-container.dark .versaai-widget-chat {{
            background: #1f2937;
            color: white;
        }}
        
        .versaai-widget-container.dark .versaai-message.assistant .versaai-message-content {{
            background: #374151;
            color: #f9fafb;
        }}
    `;
    
    // Add styles to page
    var styleSheet = document.createElement('style');
    styleSheet.textContent = widgetStyles;
    document.head.appendChild(styleSheet);
    
    // Set position class
    widgetContainer.className += ' ' + position;
    if (theme === 'dark') {{
        widgetContainer.className += ' dark';
    }}
    
    // Create widget HTML
    widgetContainer.innerHTML = `
        <div class="versaai-widget-chat" id="versaai-chat-${{chatbotId}}">
            <div class="versaai-widget-header">
                <div>{chatbot.name}</div>
                <div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">{chatbot.description or ''}</div>
            </div>
            <div class="versaai-widget-messages" id="versaai-messages-${{chatbotId}}"></div>
            <div class="versaai-widget-input">
                <input type="text" placeholder="{chatbot.placeholder_text or 'Type your message...'}" id="versaai-input-${{chatbotId}}">
                <button onclick="sendMessage(${{chatbotId}})">Send</button>
            </div>
        </div>
        <button class="versaai-widget-button" onclick="toggleWidget(${{chatbotId}})">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
        </button>
    `;
    
    // Add widget to page
    document.body.appendChild(widgetContainer);
    
    // Widget functionality
    var isOpen = false;
    var conversationId = null;
    var sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    
    window.toggleWidget = function(chatbotId) {{
        var chat = document.getElementById('versaai-chat-' + chatbotId);
        isOpen = !isOpen;
        chat.style.display = isOpen ? 'flex' : 'none';
        
        if (isOpen && !conversationId) {{
            // Show welcome message
            addMessage(chatbotId, '{chatbot.welcome_message or 'Hello! How can I help you today?'}', 'assistant');
        }}
    }};
    
    window.sendMessage = function(chatbotId) {{
        var input = document.getElementById('versaai-input-' + chatbotId);
        var message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        addMessage(chatbotId, message, 'user');
        input.value = '';
        
        // Send to API
        fetch(window.location.origin + apiBase + '/widgets/' + chatbotId + '/chat', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
                message: message,
                chatbot_id: chatbotId,
                conversation_id: conversationId,
                session_id: sessionId
            }})
        }})
        .then(response => response.json())
        .then(data => {{
            if (data.conversation_id) {{
                conversationId = data.conversation_id;
            }}
            addMessage(chatbotId, data.content, 'assistant');
        }})
        .catch(error => {{
            console.error('Error:', error);
            addMessage(chatbotId, 'Sorry, I encountered an error. Please try again.', 'assistant');
        }});
    }};
    
    function addMessage(chatbotId, content, type) {{
        var messagesContainer = document.getElementById('versaai-messages-' + chatbotId);
        var messageDiv = document.createElement('div');
        messageDiv.className = 'versaai-message ' + type;
        messageDiv.innerHTML = `
            <div class="versaai-message-content">${{content}}</div>
        `;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }}
    
    // Handle Enter key in input
    document.getElementById('versaai-input-' + chatbotId).addEventListener('keypress', function(e) {{
        if (e.key === 'Enter') {{
            sendMessage(chatbotId);
        }}
    }});
    
    // Auto-open widget if configured
    var autoOpen = {str(chatbot.behavior_settings.get('auto_open', False)).lower()};
    if (autoOpen) {{
        setTimeout(function() {{
            toggleWidget(chatbotId);
        }}, 2000);
    }}
}})();
"""
        
        return embed_script
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embed script: {str(e)}"
        )

@router.post("/{chatbot_id}/chat", response_model=ChatResponse)
def widget_chat(
    chatbot_id: int,
    chat_request: ChatRequest,
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """
    Handle chat messages from the widget.
    This endpoint is public and doesn't require authentication.
    """
    try:
        # Verify chatbot exists and is active
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == chatbot_id,
            Chatbot.is_active == True
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found or inactive"
            )
        
        # Check rate limiting (basic implementation)
        client_ip = request.client.host
        # TODO: Implement proper rate limiting with Redis or similar
        
        # Get or create conversation
        from src.models.conversation import Conversation, Message, MessageType, MessageStatus
        
        conversation = None
        if chat_request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == chat_request.conversation_id,
                Conversation.chatbot_id == chatbot_id
            ).first()
        
        if not conversation:
            # Create new conversation
            conversation = Conversation(
                chatbot_id=chatbot_id,
                session_id=chat_request.session_id,
                title="Widget Conversation",
                metadata={
                    "source": "widget",
                    "client_ip": client_ip,
                    "user_agent": request.headers.get("user-agent", "")
                }
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
        # Get conversation history for context
        recent_messages = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.desc()).limit(10).all()
        
        conversation_history = []
        for msg in reversed(recent_messages):
            role = "user" if msg.message_type == MessageType.USER else "assistant"
            conversation_history.append({"role": role, "content": msg.content})
        
        # Use RAG if enabled and knowledge bases are available
        context = ""
        sources = []
        if chatbot.use_rag and chatbot.knowledge_bases:
            try:
                rag_result = rag_service.search_and_generate(
                    query=chat_request.message,
                    knowledge_bases=chatbot.knowledge_bases,
                    conversation_history=conversation_history,
                    chatbot_config=chatbot.get_ai_config()
                )
                context = rag_result.get("context", "")
                sources = rag_result.get("sources", [])
            except Exception as e:
                # Log error but continue without RAG
                print(f"RAG error: {e}")
        
        # Generate response
        if context:
            # Use RAG-enhanced response
            ai_response = groq_service.generate_rag_response(
                query=chat_request.message,
                context=context,
                conversation_history=conversation_history,
                system_prompt=chatbot.system_prompt,
                model_name=chatbot.model_name,
                temperature=chatbot.temperature,
                max_tokens=chatbot.max_tokens
            )
        else:
            # Use standard response
            ai_response = groq_service.generate_response(
                messages=conversation_history + [{"role": "user", "content": chat_request.message}],
                system_prompt=chatbot.system_prompt,
                model_name=chatbot.model_name,
                temperature=chatbot.temperature,
                max_tokens=chatbot.max_tokens
            )
        
        # Create assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            content=ai_response["content"],
            message_type=MessageType.ASSISTANT,
            status=MessageStatus.SENT,
            ai_model=ai_response.get("model"),
            ai_tokens_used=ai_response.get("tokens_used"),
            ai_response_time_ms=ai_response.get("response_time_ms"),
            sources=sources,
            context=context if context else None
        )
        
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        # Update conversation title if it's the first exchange
        if len(conversation.messages) <= 2 and conversation.title == "Widget Conversation":
            try:
                title = groq_service.generate_conversation_title(chat_request.message)
                conversation.title = title
                db.commit()
            except:
                pass  # Keep default title if generation fails
        
        return {
            "conversation_id": conversation.id,
            "message_id": assistant_message.id,
            "content": assistant_message.content,
            "sources": sources,
            "model_used": ai_response.get("model"),
            "tokens_used": ai_response.get("tokens_used"),
            "response_time_ms": ai_response.get("response_time_ms")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Widget chat failed: {str(e)}"
        )

@router.get("/{chatbot_id}/iframe", response_class=HTMLResponse)
def get_widget_iframe(
    chatbot_id: int,
    db: Session = Depends(get_db),
    theme: Optional[str] = Query("light", description="Widget theme"),
    height: Optional[str] = Query("600px", description="Widget height"),
    width: Optional[str] = Query("400px", description="Widget width")
) -> str:
    """
    Get a full-page iframe version of the widget.
    """
    try:
        # Verify chatbot exists and is active
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == chatbot_id,
            Chatbot.is_active == True
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found or inactive"
            )
        
        # Generate iframe HTML
        iframe_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chatbot.name} - VersaAI Widget</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: {'#1f2937' if theme == 'dark' else '#ffffff'};
            color: {'#ffffff' if theme == 'dark' else '#000000'};
        }}
        
        .chat-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 100%;
            height: 100%;
        }}
        
        .chat-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            text-align: center;
        }}
        
        .chat-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .chat-input {{
            border-top: 1px solid {'#374151' if theme == 'dark' else '#e5e7eb'};
            padding: 16px;
            display: flex;
            gap: 8px;
        }}
        
        .chat-input input {{
            flex: 1;
            border: 1px solid {'#4b5563' if theme == 'dark' else '#d1d5db'};
            border-radius: 8px;
            padding: 12px;
            outline: none;
            background: {'#374151' if theme == 'dark' else '#ffffff'};
            color: {'#ffffff' if theme == 'dark' else '#000000'};
        }}
        
        .chat-input button {{
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            cursor: pointer;
            font-weight: 500;
        }}
        
        .chat-input button:hover {{
            background: #5a67d8;
        }}
        
        .message {{
            display: flex;
            align-items: flex-start;
            gap: 8px;
            max-width: 80%;
        }}
        
        .message.user {{
            align-self: flex-end;
            flex-direction: row-reverse;
        }}
        
        .message.assistant {{
            align-self: flex-start;
        }}
        
        .message-content {{
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .message.user .message-content {{
            background: #667eea;
            color: white;
        }}
        
        .message.assistant .message-content {{
            background: {'#374151' if theme == 'dark' else '#f3f4f6'};
            color: {'#f9fafb' if theme == 'dark' else '#374151'};
        }}
        
        .typing-indicator {{
            display: none;
            align-items: center;
            gap: 4px;
            padding: 12px 16px;
            background: {'#374151' if theme == 'dark' else '#f3f4f6'};
            border-radius: 12px;
            max-width: 80px;
        }}
        
        .typing-dot {{
            width: 6px;
            height: 6px;
            background: #9ca3af;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }}
        
        .typing-dot:nth-child(2) {{
            animation-delay: 0.2s;
        }}
        
        .typing-dot:nth-child(3) {{
            animation-delay: 0.4s;
        }}
        
        @keyframes typing {{
            0%, 60%, 100% {{
                transform: translateY(0);
            }}
            30% {{
                transform: translateY(-10px);
            }}
        }}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h3>{chatbot.name}</h3>
            <p style="font-size: 14px; opacity: 0.9; margin-top: 4px;">{chatbot.description or ''}</p>
        </div>
        
        <div class="chat-messages" id="messages">
            <div class="message assistant">
                <div class="message-content">
                    {chatbot.welcome_message or 'Hello! How can I help you today?'}
                </div>
            </div>
        </div>
        
        <div class="chat-input">
            <input type="text" placeholder="{chatbot.placeholder_text or 'Type your message...'}" id="messageInput">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    
    <script>
        var conversationId = null;
        var sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        var chatbotId = {chatbot_id};
        
        function sendMessage() {{
            var input = document.getElementById('messageInput');
            var message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Send to API
            fetch('/api/v1/widgets/' + chatbotId + '/chat', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    message: message,
                    chatbot_id: chatbotId,
                    conversation_id: conversationId,
                    session_id: sessionId
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                hideTypingIndicator();
                if (data.conversation_id) {{
                    conversationId = data.conversation_id;
                }}
                addMessage(data.content, 'assistant');
            }})
            .catch(error => {{
                hideTypingIndicator();
                console.error('Error:', error);
                addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            }});
        }}
        
        function addMessage(content, type) {{
            var messagesContainer = document.getElementById('messages');
            var messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + type;
            messageDiv.innerHTML = `
                <div class="message-content">${{content}}</div>
            `;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}
        
        function showTypingIndicator() {{
            var messagesContainer = document.getElementById('messages');
            var typingDiv = document.createElement('div');
            typingDiv.className = 'message assistant';
            typingDiv.id = 'typing-indicator';
            typingDiv.innerHTML = `
                <div class="typing-indicator" style="display: flex;">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            `;
            messagesContainer.appendChild(typingDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}
        
        function hideTypingIndicator() {{
            var typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {{
                typingIndicator.remove();
            }}
        }}
        
        // Handle Enter key
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }});
        
        // Focus input on load
        document.getElementById('messageInput').focus();
    </script>
</body>
</html>
"""
        
        return iframe_html
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate iframe: {str(e)}"
        )

@router.get("/{chatbot_id}/preview", response_class=HTMLResponse)
def preview_widget(
    chatbot_id: int,
    db: Session = Depends(get_db)
) -> str:
    """
    Preview the widget in a test page.
    """
    try:
        # Verify chatbot exists and is active
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == chatbot_id,
            Chatbot.is_active == True
        ).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found or inactive"
            )
        
        # Generate preview page
        preview_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Widget Preview - {chatbot.name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .preview-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .preview-header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .preview-header h1 {{
            color: #1f2937;
            margin-bottom: 8px;
        }}
        
        .preview-header p {{
            color: #6b7280;
            font-size: 16px;
        }}
        
        .preview-content {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .preview-content h2 {{
            color: #374151;
            margin-bottom: 16px;
        }}
        
        .preview-content p {{
            color: #6b7280;
            margin-bottom: 24px;
        }}
        
        .embed-code {{
            background: #1f2937;
            color: #f9fafb;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 14px;
            text-align: left;
            overflow-x: auto;
            margin-bottom: 20px;
        }}
        
        .copy-button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }}
        
        .copy-button:hover {{
            background: #5a67d8;
        }}
    </style>
</head>
<body>
    <div class="preview-container">
        <div class="preview-header">
            <h1>Widget Preview</h1>
            <p>Preview and test your {chatbot.name} chatbot widget</p>
        </div>
        
        <div class="preview-content">
            <h2>Test the Widget</h2>
            <p>Click the chat button in the bottom-right corner to test your widget.</p>
            
            <h3>Embed Code</h3>
            <p>Copy this code and paste it into your website's HTML:</p>
            
            <div class="embed-code" id="embedCode">
&lt;script src="{settings.API_V1_STR}/widgets/{chatbot_id}/embed.js"&gt;&lt;/script&gt;
            </div>
            
            <button class="copy-button" onclick="copyEmbedCode()">Copy Embed Code</button>
            
            <h3 style="margin-top: 40px;">iFrame Version</h3>
            <p>Alternatively, you can embed the widget as an iframe:</p>
            
            <div class="embed-code" id="iframeCode">
&lt;iframe src="{settings.API_V1_STR}/widgets/{chatbot_id}/iframe" width="400" height="600" frameborder="0"&gt;&lt;/iframe&gt;
            </div>
            
            <button class="copy-button" onclick="copyIframeCode()">Copy iFrame Code</button>
        </div>
    </div>
    
    <!-- Load the actual widget -->
    <script src="{settings.API_V1_STR}/widgets/{chatbot_id}/embed.js"></script>
    
    <script>
        function copyEmbedCode() {{
            var embedCode = document.getElementById('embedCode').textContent;
            navigator.clipboard.writeText(embedCode).then(function() {{
                alert('Embed code copied to clipboard!');
            }});
        }}
        
        function copyIframeCode() {{
            var iframeCode = document.getElementById('iframeCode').textContent;
            navigator.clipboard.writeText(iframeCode).then(function() {{
                alert('iFrame code copied to clipboard!');
            }});
        }}
    </script>
</body>
</html>
"""
        
        return preview_html
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate preview: {str(e)}"
        )