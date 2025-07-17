from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from datetime import datetime, timedelta

from src.api.deps import (
    get_db,
    get_current_active_user,
    check_organization_access
)
from src.models.user import User, UserRole
from src.schemas.analytics import (
    AnalyticsRequest,
    OrganizationOverview,
    ChatbotAnalytics,
    ConversationAnalytics,
    UsageAnalytics,
    UserAnalytics,
    KnowledgeBaseAnalytics,
    ComprehensiveAnalytics,
    AnalyticsReport,
    AnalyticsExport,
    RealTimeMetrics,
    PerformanceMetrics,
    UserEngagementMetrics,
    SatisfactionMetrics,
    AnalyticsPeriod,
    MetricType
)
from src.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()

@router.get("/overview", response_model=OrganizationOverview)
def get_organization_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics")
) -> Any:
    """
    Get organization overview analytics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        overview = analytics_service.get_organization_overview(
            db=db,
            organization_id=organization_id,
            period=period
        )
        
        return overview
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve organization overview: {str(e)}"
        )

@router.get("/chatbots", response_model=List[ChatbotAnalytics])
def get_chatbot_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics"),
    chatbot_id: Optional[int] = Query(None, description="Specific chatbot ID")
) -> Any:
    """
    Get chatbot analytics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        analytics = analytics_service.get_chatbot_analytics(
            db=db,
            organization_id=organization_id,
            period=period,
            chatbot_id=chatbot_id
        )
        
        return analytics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chatbot analytics: {str(e)}"
        )

@router.get("/conversations", response_model=ConversationAnalytics)
def get_conversation_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics"),
    chatbot_id: Optional[int] = Query(None, description="Specific chatbot ID")
) -> Any:
    """
    Get conversation analytics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        analytics = analytics_service.get_conversation_analytics(
            db=db,
            organization_id=organization_id,
            period=period,
            chatbot_id=chatbot_id
        )
        
        return analytics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation analytics: {str(e)}"
        )

@router.get("/usage", response_model=UsageAnalytics)
def get_usage_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics"),
    metric_type: Optional[MetricType] = Query(None, description="Specific metric type")
) -> Any:
    """
    Get usage analytics (tokens, models, etc.).
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        analytics = analytics_service.get_usage_analytics(
            db=db,
            organization_id=organization_id,
            period=period,
            metric_type=metric_type
        )
        
        return analytics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve usage analytics: {str(e)}"
        )

@router.get("/users", response_model=UserAnalytics)
def get_user_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics")
) -> Any:
    """
    Get user analytics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        analytics = analytics_service.get_user_analytics(
            db=db,
            organization_id=organization_id,
            period=period
        )
        
        return analytics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user analytics: {str(e)}"
        )

@router.get("/knowledge-base", response_model=KnowledgeBaseAnalytics)
def get_knowledge_base_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics"),
    knowledge_base_id: Optional[int] = Query(None, description="Specific knowledge base ID")
) -> Any:
    """
    Get knowledge base analytics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        analytics = analytics_service.get_knowledge_base_analytics(
            db=db,
            organization_id=organization_id,
            period=period,
            knowledge_base_id=knowledge_base_id
        )
        
        return analytics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve knowledge base analytics: {str(e)}"
        )

@router.get("/comprehensive", response_model=ComprehensiveAnalytics)
def get_comprehensive_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics")
) -> Any:
    """
    Get comprehensive analytics combining all metrics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        analytics = analytics_service.get_comprehensive_analytics(
            db=db,
            organization_id=organization_id,
            period=period
        )
        
        return analytics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve comprehensive analytics: {str(e)}"
        )

@router.get("/real-time", response_model=RealTimeMetrics)
def get_real_time_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get real-time metrics for the last hour.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        metrics = analytics_service.get_real_time_metrics(
            db=db,
            organization_id=organization_id
        )
        
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve real-time metrics: {str(e)}"
        )

@router.get("/performance", response_model=PerformanceMetrics)
def get_performance_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics"),
    chatbot_id: Optional[int] = Query(None, description="Specific chatbot ID")
) -> Any:
    """
    Get performance metrics (response times, success rates, etc.).
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        metrics = analytics_service.get_performance_metrics(
            db=db,
            organization_id=organization_id,
            period=period,
            chatbot_id=chatbot_id
        )
        
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve performance metrics: {str(e)}"
        )

@router.get("/engagement", response_model=UserEngagementMetrics)
def get_engagement_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics"),
    chatbot_id: Optional[int] = Query(None, description="Specific chatbot ID")
) -> Any:
    """
    Get user engagement metrics.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        metrics = analytics_service.get_engagement_metrics(
            db=db,
            organization_id=organization_id,
            period=period,
            chatbot_id=chatbot_id
        )
        
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve engagement metrics: {str(e)}"
        )

@router.get("/satisfaction", response_model=SatisfactionMetrics)
def get_satisfaction_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics"),
    chatbot_id: Optional[int] = Query(None, description="Specific chatbot ID")
) -> Any:
    """
    Get user satisfaction metrics (ratings, feedback).
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        metrics = analytics_service.get_satisfaction_metrics(
            db=db,
            organization_id=organization_id,
            period=period,
            chatbot_id=chatbot_id
        )
        
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve satisfaction metrics: {str(e)}"
        )

@router.post("/report", response_model=AnalyticsReport)
def generate_analytics_report(
    request: AnalyticsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Generate a custom analytics report.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        # Override organization_id if user is not super admin
        if current_user.role != UserRole.SUPER_ADMIN:
            request.organization_id = organization_id
        
        report = analytics_service.generate_analytics_report(
            db=db,
            request=request
        )
        
        return report
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate analytics report: {str(e)}"
        )

@router.post("/export", response_model=AnalyticsExport)
def export_analytics(
    request: AnalyticsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    format: str = Query("csv", description="Export format (csv, json, xlsx)")
) -> Any:
    """
    Export analytics data in various formats.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        # Override organization_id if user is not super admin
        if current_user.role != UserRole.SUPER_ADMIN:
            request.organization_id = organization_id
        
        export_data = analytics_service.export_analytics(
            db=db,
            request=request,
            format=format
        )
        
        return export_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export analytics: {str(e)}"
        )

@router.get("/chatbots/{chatbot_id}/detailed", response_model=ChatbotAnalytics)
def get_detailed_chatbot_analytics(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for analytics")
) -> Any:
    """
    Get detailed analytics for a specific chatbot.
    """
    try:
        # Verify chatbot exists and user has access
        from src.models.chatbot import Chatbot
        chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
        
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        
        # Check organization access
        if current_user.role != UserRole.SUPER_ADMIN:
            check_organization_access(current_user, chatbot.organization_id)
        
        analytics = analytics_service.get_detailed_chatbot_analytics(
            db=db,
            chatbot_id=chatbot_id,
            period=period
        )
        
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve detailed chatbot analytics: {str(e)}"
        )

@router.get("/trends", response_model=List[dict])
def get_analytics_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    metric: MetricType = Query(MetricType.CONVERSATIONS, description="Metric to analyze trends for"),
    period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Time period for trends"),
    granularity: str = Query("daily", description="Trend granularity (hourly, daily, weekly, monthly)")
) -> Any:
    """
    Get analytics trends over time.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        trends = analytics_service.get_analytics_trends(
            db=db,
            organization_id=organization_id,
            metric=metric,
            period=period,
            granularity=granularity
        )
        
        return trends
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve analytics trends: {str(e)}"
        )

@router.get("/comparison", response_model=dict)
def get_analytics_comparison(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Current period"),
    comparison_period: AnalyticsPeriod = Query(AnalyticsPeriod.LAST_30_DAYS, description="Comparison period"),
    metrics: List[MetricType] = Query([MetricType.CONVERSATIONS, MetricType.MESSAGES], description="Metrics to compare")
) -> Any:
    """
    Compare analytics between two time periods.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        comparison = analytics_service.get_analytics_comparison(
            db=db,
            organization_id=organization_id,
            current_period=current_period,
            comparison_period=comparison_period,
            metrics=metrics
        )
        
        return comparison
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve analytics comparison: {str(e)}"
        )

@router.get("/dashboard", response_model=dict)
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get dashboard data with key metrics and charts.
    """
    try:
        organization_id = None if current_user.role == UserRole.SUPER_ADMIN else current_user.organization_id
        
        dashboard_data = analytics_service.get_dashboard_data(
            db=db,
            organization_id=organization_id
        )
        
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve dashboard data: {str(e)}"
        )