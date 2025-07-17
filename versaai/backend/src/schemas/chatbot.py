from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class ChatbotStatus(str, Enum):
    """Chatbot status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRAINING = "training"
    ERROR = "error"

class ChatbotType(str, Enum):
    """Chatbot type enum"""
    CUSTOMER_SUPPORT = "customer_support"
    SALES = "sales"
    FAQ = "faq"
    GENERAL = "general"
    CUSTOM = "custom"

class ChatbotBase(BaseModel):
    """Base chatbot schema"""
    name: str = Field(..., min_length=2, max_length=100, description="Chatbot name")
    description: Optional[str] = Field(None, max_length=500, description="Chatbot description")
    is_active: bool = Field(default=True, description="Chatbot active status")
    
class ChatbotCreate(ChatbotBase):
    """Chatbot creation schema"""
    widget_id: Optional[str] = Field(None, description="Widget unique identifier (auto-generated if not provided)")
    knowledge_base_id: Optional[int] = Field(None, description="Knowledge base ID")
    is_public: bool = Field(default=False, description="Public chatbot status")
    model_name: str = Field(default="mixtral-8x7b-32768", description="AI model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="AI temperature")
    max_tokens: int = Field(default=1000, ge=1, le=4000, description="Maximum tokens")
    system_prompt: Optional[str] = Field(None, description="System prompt")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    primary_color: str = Field(default="#007bff", description="Primary color")
    secondary_color: str = Field(default="#6c757d", description="Secondary color")
    welcome_message: str = Field(default="Hello! How can I help you today?", description="Welcome message")
    widget_position: str = Field(default="bottom-right", description="Widget position")
    widget_size: str = Field(default="medium", description="Widget size")
    show_branding: bool = Field(default=True, description="Show branding")
    auto_suggestions: List[str] = Field(default_factory=list, description="Auto suggestions")
    fallback_message: str = Field(default="I'm sorry, I don't understand. Can you please rephrase?", description="Fallback message")
    max_conversation_length: int = Field(default=50, description="Max conversation length")
    collect_analytics: bool = Field(default=True, description="Collect analytics")
    collect_feedback: bool = Field(default=True, description="Collect feedback")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Settings")

class ChatbotUpdate(BaseModel):
    """Chatbot update schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Chatbot name")
    description: Optional[str] = Field(None, max_length=500, description="Chatbot description")
    is_active: Optional[bool] = Field(None, description="Chatbot active status")
    knowledge_base_id: Optional[int] = Field(None, description="Knowledge base ID")
    ai_settings: Optional[Dict[str, Any]] = Field(None, description="AI settings")
    appearance: Optional[Dict[str, Any]] = Field(None, description="Appearance settings")
    widget_settings: Optional[Dict[str, Any]] = Field(None, description="Widget settings")
    behavior_settings: Optional[Dict[str, Any]] = Field(None, description="Behavior settings")
    advanced_settings: Optional[Dict[str, Any]] = Field(None, description="Advanced settings")

class ChatbotAISettings(BaseModel):
    """Chatbot AI settings schema"""
    model_name: str = Field(default="mixtral-8x7b-32768", description="AI model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="AI temperature")
    max_tokens: int = Field(default=1000, ge=1, le=4000, description="Maximum tokens")
    top_p: float = Field(default=1.0, ge=0.0, le=1.0, description="Top P sampling")
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="Presence penalty")
    system_prompt: Optional[str] = Field(None, description="System prompt")
    context_window: int = Field(default=10, ge=1, le=50, description="Context window size")
    enable_rag: bool = Field(default=True, description="Enable RAG")
    rag_similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="RAG similarity threshold")
    rag_max_results: int = Field(default=5, ge=1, le=20, description="Maximum RAG results")

class ChatbotAppearance(BaseModel):
    """Chatbot appearance schema"""
    avatar_url: Optional[str] = Field(None, description="Chatbot avatar URL")
    primary_color: str = Field(default="#007bff", description="Primary color")
    secondary_color: str = Field(default="#6c757d", description="Secondary color")
    text_color: str = Field(default="#212529", description="Text color")
    background_color: str = Field(default="#ffffff", description="Background color")
    font_family: str = Field(default="Inter, sans-serif", description="Font family")
    border_radius: int = Field(default=8, ge=0, le=50, description="Border radius")
    welcome_message: str = Field(default="Hello! How can I help you today?", description="Welcome message")
    placeholder_text: str = Field(default="Type your message...", description="Input placeholder text")
    
class ChatbotWidgetSettings(BaseModel):
    """Chatbot widget settings schema"""
    position: str = Field(default="bottom-right", description="Widget position")
    size: str = Field(default="medium", description="Widget size")
    show_launcher: bool = Field(default=True, description="Show launcher button")
    launcher_text: str = Field(default="Chat with us", description="Launcher button text")
    auto_open: bool = Field(default=False, description="Auto open widget")
    auto_open_delay: int = Field(default=5, ge=0, description="Auto open delay in seconds")
    show_branding: bool = Field(default=True, description="Show VersaAI branding")
    custom_css: Optional[str] = Field(None, description="Custom CSS")
    allowed_domains: List[str] = Field(default_factory=list, description="Allowed domains")
    
class ChatbotBehaviorSettings(BaseModel):
    """Chatbot behavior settings schema"""
    enable_typing_indicator: bool = Field(default=True, description="Enable typing indicator")
    response_delay: int = Field(default=1, ge=0, le=10, description="Response delay in seconds")
    enable_quick_replies: bool = Field(default=True, description="Enable quick replies")
    quick_replies: List[str] = Field(default_factory=list, description="Quick reply options")
    enable_file_upload: bool = Field(default=False, description="Enable file upload")
    max_file_size_mb: int = Field(default=5, ge=1, le=50, description="Maximum file size in MB")
    allowed_file_types: List[str] = Field(default_factory=lambda: ["pdf", "txt", "docx"], description="Allowed file types")
    fallback_message: str = Field(default="I'm sorry, I don't understand. Can you please rephrase?", description="Fallback message")
    max_conversation_length: int = Field(default=100, ge=10, le=500, description="Maximum conversation length")
    enable_conversation_rating: bool = Field(default=True, description="Enable conversation rating")
    enable_human_handoff: bool = Field(default=False, description="Enable human handoff")
    handoff_message: str = Field(default="Let me connect you with a human agent.", description="Handoff message")

class ChatbotInDBBase(ChatbotBase):
    """Base chatbot schema with database fields"""
    id: int = Field(..., description="Chatbot ID")
    widget_id: str = Field(..., description="Widget unique identifier")
    organization_id: int = Field(..., description="Organization ID")
    created_by_id: int = Field(..., description="Creator user ID")
    knowledge_base_id: Optional[int] = Field(None, description="Knowledge base ID")
    is_public: bool = Field(default=False, description="Public chatbot status")
    model_name: str = Field(..., description="AI model name")
    temperature: float = Field(..., description="AI temperature")
    max_tokens: int = Field(..., description="Maximum tokens")
    system_prompt: Optional[str] = Field(None, description="System prompt")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    primary_color: str = Field(..., description="Primary color")
    secondary_color: str = Field(..., description="Secondary color")
    welcome_message: str = Field(..., description="Welcome message")
    widget_position: str = Field(..., description="Widget position")
    widget_size: str = Field(..., description="Widget size")
    show_branding: bool = Field(..., description="Show branding")
    auto_suggestions: List[str] = Field(default_factory=list, description="Auto suggestions")
    fallback_message: str = Field(..., description="Fallback message")
    max_conversation_length: int = Field(..., description="Max conversation length")
    collect_analytics: bool = Field(..., description="Collect analytics")
    collect_feedback: bool = Field(..., description="Collect feedback")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Settings")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    last_trained: Optional[datetime] = Field(None, description="Last training timestamp")

    class Config:
        from_attributes = True

class Chatbot(ChatbotInDBBase):
    """Chatbot schema for API responses"""
    pass

class ChatbotWithStats(Chatbot):
    """Chatbot schema with statistics"""
    total_conversations: int = Field(default=0, description="Total conversations")
    active_conversations: int = Field(default=0, description="Active conversations")
    total_messages: int = Field(default=0, description="Total messages")
    avg_response_time: float = Field(default=0.0, description="Average response time in ms")
    user_satisfaction: float = Field(default=0.0, description="Average user satisfaction")
    last_conversation_at: Optional[datetime] = Field(None, description="Last conversation timestamp")

class ChatbotList(BaseModel):
    """Chatbot list schema"""
    chatbots: List[ChatbotWithStats] = Field(..., description="List of chatbots")
    total: int = Field(..., description="Total number of chatbots")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")

class ChatbotStats(BaseModel):
    """Chatbot statistics schema"""
    total_conversations: int = Field(..., description="Total conversations")
    active_conversations: int = Field(..., description="Active conversations")
    total_messages: int = Field(..., description="Total messages")
    user_messages: int = Field(..., description="User messages")
    assistant_messages: int = Field(..., description="Assistant messages")
    avg_response_time: float = Field(..., description="Average response time in ms")
    avg_conversation_length: float = Field(..., description="Average conversation length")
    user_satisfaction: float = Field(..., description="Average user satisfaction")
    satisfaction_responses: int = Field(..., description="Number of satisfaction responses")
    peak_hours: List[Dict[str, Any]] = Field(..., description="Peak usage hours")
    daily_conversations: List[Dict[str, Any]] = Field(..., description="Daily conversation counts")

class ChatbotConfig(BaseModel):
    """Chatbot configuration schema for widget"""
    id: int = Field(..., description="Chatbot ID")
    name: str = Field(..., description="Chatbot name")
    welcome_message: str = Field(..., description="Welcome message")
    placeholder_text: str = Field(..., description="Input placeholder")
    appearance: Dict[str, Any] = Field(..., description="Appearance settings")
    widget_settings: Dict[str, Any] = Field(..., description="Widget settings")
    behavior_settings: Dict[str, Any] = Field(..., description="Behavior settings")
    is_active: bool = Field(..., description="Chatbot active status")

class ChatbotTraining(BaseModel):
    """Chatbot training schema"""
    knowledge_base_id: int = Field(..., description="Knowledge base ID")
    retrain_all: bool = Field(default=False, description="Retrain all documents")
    training_notes: Optional[str] = Field(None, description="Training notes")

class ChatbotTrainingStatus(BaseModel):
    """Chatbot training status schema"""
    status: ChatbotStatus = Field(..., description="Training status")
    progress: float = Field(..., ge=0.0, le=100.0, description="Training progress percentage")
    message: str = Field(..., description="Status message")
    started_at: Optional[datetime] = Field(None, description="Training start time")
    completed_at: Optional[datetime] = Field(None, description="Training completion time")
    error_message: Optional[str] = Field(None, description="Error message if failed")

# Alias for response model consistency
ChatbotResponse = Chatbot