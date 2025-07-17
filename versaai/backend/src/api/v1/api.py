from fastapi import APIRouter

from .endpoints import (
    auth,
    users,
    organizations,
    chatbots,
    conversations,
    knowledge_base,
    analytics,
    widgets,
    system,
    settings,
    notifications,
    activity,
    dashboard
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(chatbots.router, prefix="/chatbots", tags=["chatbots"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(knowledge_base.router, prefix="/knowledge-base", tags=["knowledge-base"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(widgets.router, prefix="/widgets", tags=["widgets"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])