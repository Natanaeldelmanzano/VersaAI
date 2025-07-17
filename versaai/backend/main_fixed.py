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

from src.core.config import settings
from src.core.database import engine, create_tables
from src.core.cache import cache_manager
from src.api.v1.api import api_router
from src.api.endpoints.health import router as health_router
from src.middleware.performance import (
    PerformanceMiddleware,
    RateLimitMiddleware,
    HealthCheckMiddleware
)
from src.models import Base

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
    
    logger.info("✅ VersaAI application startup completed")
    
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

# Add performance and security middlewares (sin SecurityHeadersMiddleware problemático)
app.add_middleware(PerformanceMiddleware, min_response_time_log=1.0)
app.add_middleware(RateLimitMiddleware, requests_per_minute=120)
app.add_middleware(HealthCheckMiddleware)

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Add trusted host middleware
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Middleware de seguridad corregido (sin CSP restrictivo)
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # Headers de seguridad básicos (sin CSP restrictivo para docs)
    if not request.url.path.startswith("/api/docs") and not request.url.path.startswith("/api/redoc"):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
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
        "main_fixed:app",
        host="0.0.0.0",
        port=8003,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )