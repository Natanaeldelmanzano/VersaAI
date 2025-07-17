#!/usr/bin/env python3
"""
Servidor FastAPI simplificado para diagnosticar el problema
"""

from fastapi import FastAPI
import uvicorn

# Crear aplicación FastAPI mínima
app = FastAPI(
    title="VersaAI Debug Server",
    description="Servidor simplificado para diagnóstico",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "VersaAI Debug Server",
        "status": "running",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "server": "debug"
    }

@app.get("/test")
async def test():
    """Endpoint de prueba"""
    return {
        "test": "success",
        "message": "El servidor está funcionando correctamente"
    }

if __name__ == "__main__":
    print("🚀 Iniciando servidor de diagnóstico...")
    print("📋 URLs disponibles:")
    print("   - Root: http://localhost:8001/")
    print("   - Health: http://localhost:8001/health")
    print("   - Test: http://localhost:8001/test")
    print("   - Docs: http://localhost:8001/api/docs")
    print("   - ReDoc: http://localhost:8001/api/redoc")
    print("   - OpenAPI: http://localhost:8001/openapi.json")
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8001,  # Puerto diferente para evitar conflictos
        reload=False,
        log_level="info"
    )