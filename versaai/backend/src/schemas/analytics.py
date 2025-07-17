from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class AnalyticsPeriod(str, Enum):
    """Analytics period enum"""
    LAST_7_DAYS = "7d"
    LAST_30_DAYS = "30d"
    LAST_90_DAYS = "90d"
    LAST_YEAR = "1y"
    CUSTOM = "custom"

class MetricType(str, Enum):
    """Metric type enum"""
    CONVERSATIONS = "conversations"
    MESSAGES = "messages"
    USERS = "users"
    RESPONSE_TIME = "response_time"
    SATISFACTION = "satisfaction"
    TOKENS = "tokens"

class AnalyticsRequest(BaseModel):
    """Analytics request schema"""
    period: AnalyticsPeriod = Field(default=AnalyticsPeriod.LAST_30_DAYS, description="Analytics period")
    start_date: Optional[datetime] = Field(None, description="Custom start date")
    end_date: Optional[datetime] = Field(None, description="Custom end date")
    chatbot_id: Optional[int] = Field(None, description="Filter by chatbot ID")
    metrics: Optional[List[MetricType]] = Field(None, description="Specific metrics to include")
    granularity: str = Field(default="day", description="Data granularity (hour, day, week, month)")

class OrganizationOverview(BaseModel):
    """Organization overview analytics schema"""
    total_users: int = Field(..., description="Total number of users")
    total_chatbots: int = Field(..., description="Total number of chatbots")
    total_conversations: int = Field(..., description="Total number of conversations")
    total_messages: int = Field(..., description="Total number of messages")
    total_knowledge_bases: int = Field(..., description="Total number of knowledge bases")
    total_documents: int = Field(..., description="Total number of documents")
    recent_conversations_30d: int = Field(..., description="Recent conversations (30 days)")
    recent_messages_30d: int = Field(..., description="Recent messages (30 days)")

class ChatbotAnalytics(BaseModel):
    """Chatbot analytics schema"""
    total_conversations: int = Field(..., description="Total conversations")
    active_conversations: int = Field(..., description="Active conversations")
    total_messages: int = Field(..., description="Total messages")
    recent_conversations: int = Field(..., description="Recent conversations")
    recent_messages: int = Field(..., description="Recent messages")
    user_messages: int = Field(..., description="User messages")
    assistant_messages: int = Field(..., description="Assistant messages")
    avg_response_time_ms: float = Field(..., description="Average response time in ms")
    avg_satisfaction: float = Field(..., description="Average satisfaction rating")
    satisfaction_responses: int = Field(..., description="Number of satisfaction responses")
    period_days: int = Field(..., description="Analysis period in days")

class ConversationAnalytics(BaseModel):
    """Conversation analytics schema"""
    daily_conversations: List[Dict[str, Any]] = Field(..., description="Daily conversation counts")
    avg_duration_minutes: float = Field(..., description="Average conversation duration")
    avg_messages_per_conversation: float = Field(..., description="Average messages per conversation")
    top_chatbots: List[Dict[str, Any]] = Field(..., description="Top performing chatbots")

class UsageAnalytics(BaseModel):
    """Usage analytics schema"""
    total_tokens: int = Field(..., description="Total tokens used")
    daily_tokens: List[Dict[str, Any]] = Field(..., description="Daily token usage")
    model_usage: List[Dict[str, Any]] = Field(..., description="Usage by AI model")
    hourly_usage: List[Dict[str, Any]] = Field(..., description="Hourly usage patterns")

class UserAnalytics(BaseModel):
    """User analytics schema"""
    active_users: int = Field(..., description="Active users")
    new_users: int = Field(..., description="New users")
    anonymous_conversations: int = Field(..., description="Anonymous conversations")
    registered_conversations: int = Field(..., description="Registered user conversations")
    user_activity: List[Dict[str, Any]] = Field(..., description="Daily user activity")

class KnowledgeBaseAnalytics(BaseModel):
    """Knowledge base analytics schema"""
    knowledge_bases: List[Dict[str, Any]] = Field(..., description="Knowledge base statistics")
    document_status: List[Dict[str, Any]] = Field(..., description="Documents by status")
    document_types: List[Dict[str, Any]] = Field(..., description="Documents by type")

class ComprehensiveAnalytics(BaseModel):
    """Comprehensive analytics schema"""
    overview: OrganizationOverview = Field(..., description="Organization overview")
    conversations: ConversationAnalytics = Field(..., description="Conversation analytics")
    usage: UsageAnalytics = Field(..., description="Usage analytics")
    users: UserAnalytics = Field(..., description="User analytics")
    knowledge_base: KnowledgeBaseAnalytics = Field(..., description="Knowledge base analytics")
    period_days: int = Field(..., description="Analysis period in days")
    generated_at: str = Field(..., description="Generation timestamp")

class MetricDataPoint(BaseModel):
    """Metric data point schema"""
    timestamp: datetime = Field(..., description="Data point timestamp")
    value: float = Field(..., description="Metric value")
    label: Optional[str] = Field(None, description="Data point label")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class TimeSeriesMetric(BaseModel):
    """Time series metric schema"""
    metric_name: str = Field(..., description="Metric name")
    metric_type: MetricType = Field(..., description="Metric type")
    data_points: List[MetricDataPoint] = Field(..., description="Time series data")
    total: Optional[float] = Field(None, description="Total value")
    average: Optional[float] = Field(None, description="Average value")
    min_value: Optional[float] = Field(None, description="Minimum value")
    max_value: Optional[float] = Field(None, description="Maximum value")
    trend: Optional[str] = Field(None, description="Trend direction (up, down, stable)")
    period: str = Field(..., description="Analysis period")

class AnalyticsReport(BaseModel):
    """Analytics report schema"""
    report_id: str = Field(..., description="Report ID")
    organization_id: int = Field(..., description="Organization ID")
    report_type: str = Field(..., description="Report type")
    period: AnalyticsPeriod = Field(..., description="Report period")
    start_date: datetime = Field(..., description="Report start date")
    end_date: datetime = Field(..., description="Report end date")
    metrics: List[TimeSeriesMetric] = Field(..., description="Report metrics")
    summary: Dict[str, Any] = Field(..., description="Report summary")
    insights: List[str] = Field(..., description="Key insights")
    recommendations: List[str] = Field(..., description="Recommendations")
    generated_at: datetime = Field(..., description="Generation timestamp")
    generated_by: int = Field(..., description="Generator user ID")

class AnalyticsExport(BaseModel):
    """Analytics export schema"""
    format: str = Field(default="json", description="Export format (json, csv, pdf)")
    include_charts: bool = Field(default=True, description="Include charts in export")
    include_raw_data: bool = Field(default=False, description="Include raw data")
    metrics: Optional[List[MetricType]] = Field(None, description="Specific metrics to export")
    period: AnalyticsPeriod = Field(default=AnalyticsPeriod.LAST_30_DAYS, description="Export period")
    start_date: Optional[datetime] = Field(None, description="Custom start date")
    end_date: Optional[datetime] = Field(None, description="Custom end date")

class RealTimeMetrics(BaseModel):
    """Real-time metrics schema"""
    active_conversations: int = Field(..., description="Currently active conversations")
    messages_last_hour: int = Field(..., description="Messages in the last hour")
    avg_response_time_last_hour: float = Field(..., description="Average response time last hour")
    online_users: int = Field(..., description="Currently online users")
    system_load: float = Field(..., description="System load percentage")
    api_requests_per_minute: int = Field(..., description="API requests per minute")
    error_rate_percentage: float = Field(..., description="Error rate percentage")
    timestamp: datetime = Field(..., description="Metrics timestamp")

class PerformanceMetrics(BaseModel):
    """Performance metrics schema"""
    avg_response_time_ms: float = Field(..., description="Average response time")
    p95_response_time_ms: float = Field(..., description="95th percentile response time")
    p99_response_time_ms: float = Field(..., description="99th percentile response time")
    error_rate_percentage: float = Field(..., description="Error rate percentage")
    throughput_requests_per_second: float = Field(..., description="Throughput (requests/second)")
    uptime_percentage: float = Field(..., description="Uptime percentage")
    total_requests: int = Field(..., description="Total requests")
    successful_requests: int = Field(..., description="Successful requests")
    failed_requests: int = Field(..., description="Failed requests")
    period: str = Field(..., description="Metrics period")

class UserEngagementMetrics(BaseModel):
    """User engagement metrics schema"""
    daily_active_users: int = Field(..., description="Daily active users")
    weekly_active_users: int = Field(..., description="Weekly active users")
    monthly_active_users: int = Field(..., description="Monthly active users")
    avg_session_duration_minutes: float = Field(..., description="Average session duration")
    avg_conversations_per_user: float = Field(..., description="Average conversations per user")
    user_retention_rate: float = Field(..., description="User retention rate")
    bounce_rate_percentage: float = Field(..., description="Bounce rate percentage")
    repeat_user_percentage: float = Field(..., description="Repeat user percentage")
    period: str = Field(..., description="Metrics period")

class SatisfactionMetrics(BaseModel):
    """Satisfaction metrics schema"""
    avg_rating: float = Field(..., description="Average satisfaction rating")
    total_ratings: int = Field(..., description="Total number of ratings")
    rating_distribution: Dict[str, int] = Field(..., description="Rating distribution (1-5 stars)")
    nps_score: Optional[float] = Field(None, description="Net Promoter Score")
    satisfaction_trend: List[Dict[str, Any]] = Field(..., description="Satisfaction trend over time")
    top_positive_feedback: List[str] = Field(..., description="Top positive feedback themes")
    top_negative_feedback: List[str] = Field(..., description="Top negative feedback themes")
    period: str = Field(..., description="Metrics period")