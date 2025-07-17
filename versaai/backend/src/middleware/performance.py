"""Performance Middleware for VersaAI"""

import time
import gzip
import json
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.gzip import GZipMiddleware
from typing import Callable
import logging
from datetime import datetime


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware para monitoreo de performance y métricas"""
    
    def __init__(self, app, min_response_time_log: float = 1.0):
        super().__init__(app)
        self.min_response_time_log = min_response_time_log
        self.logger = logging.getLogger("versaai.performance")
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Registrar inicio de request
        start_time = time.time()
        request_id = f"{int(start_time * 1000000)}"
        
        # Añadir headers de request
        request.state.request_id = request_id
        request.state.start_time = start_time
        
        # Procesar request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log de errores
            process_time = time.time() - start_time
            self.logger.error(
                f"Request {request_id} failed: {str(e)} "
                f"[{request.method} {request.url.path}] "
                f"Time: {process_time:.3f}s"
            )
            raise
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Añadir headers de performance
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        response.headers["X-Timestamp"] = str(int(start_time))
        
        # Log de requests lentos
        if process_time > self.min_response_time_log:
            self.logger.warning(
                f"Slow request {request_id}: {process_time:.3f}s "
                f"[{request.method} {request.url.path}] "
                f"Status: {response.status_code}"
            )
        
        # Log de métricas básicas
        self.logger.info(
            f"Request {request_id} completed: "
            f"[{request.method} {request.url.path}] "
            f"Status: {response.status_code} "
            f"Time: {process_time:.3f}s"
        )
        
        return response


class CompressionMiddleware(BaseHTTPMiddleware):
    """Middleware personalizado de compresión"""
    
    def __init__(self, app, minimum_size: int = 1024):
        super().__init__(app)
        self.minimum_size = minimum_size
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Verificar si el cliente acepta compresión
        accept_encoding = request.headers.get("accept-encoding", "")
        
        if "gzip" not in accept_encoding:
            return response
        
        # Verificar tipo de contenido
        content_type = response.headers.get("content-type", "")
        compressible_types = [
            "application/json",
            "text/html",
            "text/css",
            "text/javascript",
            "application/javascript",
            "text/plain"
        ]
        
        if not any(ct in content_type for ct in compressible_types):
            return response
        
        # Obtener contenido de la respuesta
        if hasattr(response, 'body'):
            content = response.body
        else:
            return response
        
        # Verificar tamaño mínimo
        if len(content) < self.minimum_size:
            return response
        
        # Comprimir contenido
        try:
            compressed_content = gzip.compress(content)
            
            # Crear nueva respuesta comprimida
            response.headers["content-encoding"] = "gzip"
            response.headers["content-length"] = str(len(compressed_content))
            response.headers["vary"] = "Accept-Encoding"
            
            # Actualizar el cuerpo de la respuesta
            response._content = compressed_content
            
        except Exception as e:
            logging.error(f"Error comprimiendo respuesta: {e}")
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware para añadir headers de seguridad"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Headers de seguridad
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }
        
        for header, value in security_headers.items():
            response.headers[header] = value
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware básico de rate limiting"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}  # En producción usar Redis
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host
        current_time = datetime.now()
        
        # Limpiar requests antiguos (simplificado)
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if (current_time - req_time).seconds < 60
            ]
        else:
            self.requests[client_ip] = []
        
        # Verificar límite
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.requests_per_minute} requests per minute"
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0"
                }
            )
        
        # Registrar request
        self.requests[client_ip].append(current_time)
        
        # Procesar request
        response = await call_next(request)
        
        # Añadir headers de rate limit
        remaining = self.requests_per_minute - len(self.requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response


class HealthCheckMiddleware(BaseHTTPMiddleware):
    """Middleware para health checks rápidos"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Health check endpoint rápido
        if request.url.path == "/health":
            return JSONResponse(
                content={
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "version": "1.0.0"
                },
                headers={"Cache-Control": "no-cache"}
            )
        
        return await call_next(request)