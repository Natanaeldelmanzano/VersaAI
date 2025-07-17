from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import time
import os

from .core.config import settings
from .core.database import engine, create_tables
from .core.cache import cache_manager
from .api.v1.api import api_router
from .api.endpoints.health import router as health_router
from .middleware.performance import (
    PerformanceMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    HealthCheckMiddleware
)
from .models import Base

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting VersaAI application...")
    
    # Initialize Redis Cache
    try:
        cache_initialized = await cache_manager.init_cache()
        if cache_initialized:
            logger.info("Redis cache initialized successfully")
        else:
            logger.warning("Redis cache initialization failed - continuing without cache")
    except Exception as e:
        logger.error(f"Error initializing Redis cache: {e}")
    
    # Create database tables
    try:
        await create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    
    # Create upload directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/documents", exist_ok=True)
    os.makedirs("uploads/avatars", exist_ok=True)
    
    # Initialize demo users for multi-user system
    try:
        from .utils.demo_setup import initialize_demo_users
        await initialize_demo_users()
        logger.info("Demo users initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing demo users: {e}")
    
    logger.info("✅ VersaAI application startup completed")
    logger.info("🎯 Multi-user demo mode ready - Check documentation for user credentials")
    
    yield
    
    # Shutdown
    logger.info("Shutting down VersaAI application...")
    logger.info("✅ VersaAI application shutdown completed")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise AI Chatbot Platform with RAG capabilities",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add performance and security middlewares
app.add_middleware(PerformanceMiddleware, min_response_time_log=1.0)
# SecurityHeadersMiddleware removido - causaba CSP restrictivo en páginas de documentación
app.add_middleware(RateLimitMiddleware, requests_per_minute=120)
app.add_middleware(HealthCheckMiddleware)

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add CORS middleware con configuración más permisiva
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Más permisivo para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware con configuración más permisiva
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Más permisivo para desarrollo
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )

# Basic health check endpoint (kept for backward compatibility)
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "timestamp": time.time()
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/api/docs",
        "health": "/health"
    }

# Include API routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api")

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )