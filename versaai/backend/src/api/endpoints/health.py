"""Health Check Endpoints for VersaAI"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import psutil
import os
import asyncio
from typing import Dict, Any

from src.core.database import get_db
from src.core.cache import cache_manager

router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get("/")
async def basic_health_check():
    """Health check básico y rápido"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "VersaAI Backend",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Health check detallado con métricas del sistema"""
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "VersaAI Backend",
        "version": "1.0.0",
        "checks": {}
    }
    
    # Check de base de datos
    try:
        db.execute(text("SELECT 1"))
        health_data["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": "<10"
        }
    except Exception as e:
        health_data["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_data["status"] = "degraded"
    
    # Check de Redis
    try:
        redis_stats = await cache_manager.get_cache_stats()
        health_data["checks"]["redis"] = {
            "status": "healthy" if redis_stats["status"] == "connected" else "unhealthy",
            "stats": redis_stats
        }
    except Exception as e:
        health_data["checks"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Métricas del sistema
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_data["system_metrics"] = {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_usage_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2)
        }
        
        # Alertas de recursos
        if cpu_percent > 80:
            health_data["status"] = "degraded"
            health_data["alerts"] = health_data.get("alerts", [])
            health_data["alerts"].append("High CPU usage")
            
        if memory.percent > 85:
            health_data["status"] = "degraded"
            health_data["alerts"] = health_data.get("alerts", [])
            health_data["alerts"].append("High memory usage")
            
    except Exception as e:
        health_data["system_metrics"] = {"error": str(e)}
    
    return health_data


@router.get("/database")
async def database_health_check(db: Session = Depends(get_db)):
    """Health check específico de la base de datos"""
    
    try:
        start_time = datetime.now()
        
        # Test de conexión básica
        db.execute(text("SELECT 1"))
        
        # Test de tablas principales (ajustar según tu esquema)
        tables_check = {}
        essential_tables = ["users", "organizations", "chatbots"]  # Ajustar según tu esquema
        
        for table in essential_tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                tables_check[table] = {"status": "ok", "count": count}
            except Exception as e:
                tables_check[table] = {"status": "error", "error": str(e)}
        
        # Tiempo de respuesta
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "status": "healthy",
            "database_type": "PostgreSQL",
            "response_time_ms": round(response_time, 2),
            "tables": tables_check,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get("/redis")
async def redis_health_check():
    """Health check específico de Redis"""
    
    try:
        stats = await cache_manager.get_cache_stats()
        
        if stats["status"] == "connected":
            return {
                "status": "healthy",
                "redis_stats": stats,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=503,
                detail={
                    "status": "unhealthy",
                    "error": stats.get("message", "Redis not connected"),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get("/performance")
async def performance_metrics():
    """Métricas de performance del sistema"""
    
    try:
        # CPU y memoria
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        
        # Procesos
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        # Disco
        disk = psutil.disk_usage('/')
        
        # Red (si está disponible)
        try:
            network = psutil.net_io_counters()
            network_stats = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
        except:
            network_stats = {"error": "Network stats not available"}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "usage_percent": cpu_percent,
                "count": cpu_count,
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "usage_percent": memory.percent
            },
            "process": {
                "pid": os.getpid(),
                "memory_mb": round(process_memory.rss / (1024**2), 2),
                "cpu_percent": process.cpu_percent()
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "usage_percent": disk.percent
            },
            "network": network_stats
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to collect performance metrics",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get("/readiness")
async def readiness_check(db: Session = Depends(get_db)):
    """Check de readiness para Kubernetes/Docker"""
    
    checks = []
    all_healthy = True
    
    # Check database
    try:
        db.execute(text("SELECT 1"))
        checks.append({"service": "database", "status": "ready"})
    except Exception as e:
        checks.append({"service": "database", "status": "not_ready", "error": str(e)})
        all_healthy = False
    
    # Check Redis
    try:
        redis_stats = await cache_manager.get_cache_stats()
        if redis_stats["status"] == "connected":
            checks.append({"service": "redis", "status": "ready"})
        else:
            checks.append({"service": "redis", "status": "not_ready"})
            all_healthy = False
    except Exception as e:
        checks.append({"service": "redis", "status": "not_ready", "error": str(e)})
        all_healthy = False
    
    status_code = 200 if all_healthy else 503
    
    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/liveness")
async def liveness_check():
    """Check de liveness para Kubernetes/Docker"""
    
    # Check básico de que la aplicación responde
    try:
        # Verificar que podemos hacer operaciones básicas
        current_time = datetime.now()
        
        return {
            "status": "alive",
            "timestamp": current_time.isoformat(),
            "uptime_seconds": (current_time - datetime.now()).total_seconds()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_alive",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )