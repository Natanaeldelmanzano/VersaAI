"""Logging Configuration for VersaAI"""

import logging
import logging.config
import json
import sys
from datetime import datetime
from typing import Dict, Any
import os


class JSONFormatter(logging.Formatter):
    """Formatter para logs en formato JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Añadir información adicional si está disponible
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
            
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
            
        if hasattr(record, 'execution_time'):
            log_entry['execution_time_ms'] = record.execution_time
        
        # Añadir información de excepción si existe
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Añadir campos extra
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'lineno', 'funcName', 'created',
                          'msecs', 'relativeCreated', 'thread', 'threadName',
                          'processName', 'process', 'getMessage', 'exc_info',
                          'exc_text', 'stack_info']:
                log_entry[key] = value
        
        return json.dumps(log_entry, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """Formatter con colores para desarrollo"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        
        # Formato personalizado para desarrollo
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        return formatter.format(record)


def setup_logging(environment: str = "development", log_level: str = "INFO") -> None:
    """Configurar logging según el entorno"""
    
    # Configuración base
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {},
        "handlers": {},
        "loggers": {},
        "root": {
            "level": log_level,
            "handlers": []
        }
    }
    
    if environment == "production":
        # Configuración para producción (JSON)
        config["formatters"]["json"] = {
            "()": "src.core.logging_config.JSONFormatter"
        }
        
        config["handlers"]["console"] = {
            "class": "logging.StreamHandler",
            "level": log_level,
            "formatter": "json",
            "stream": "ext://sys.stdout"
        }
        
        # Handler para archivos de log
        config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": log_level,
            "formatter": "json",
            "filename": "logs/versaai.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
        
        # Handler para errores
        config["handlers"]["error_file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": "logs/versaai_errors.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
        
        config["root"]["handlers"] = ["console", "file", "error_file"]
        
    else:
        # Configuración para desarrollo (coloreado)
        config["formatters"]["colored"] = {
            "()": "src.core.logging_config.ColoredFormatter"
        }
        
        config["handlers"]["console"] = {
            "class": "logging.StreamHandler",
            "level": log_level,
            "formatter": "colored",
            "stream": "ext://sys.stdout"
        }
        
        config["root"]["handlers"] = ["console"]
    
    # Configurar loggers específicos
    config["loggers"]["versaai"] = {
        "level": log_level,
        "handlers": config["root"]["handlers"],
        "propagate": False
    }
    
    config["loggers"]["versaai.performance"] = {
        "level": "INFO",
        "handlers": config["root"]["handlers"],
        "propagate": False
    }
    
    config["loggers"]["versaai.security"] = {
        "level": "WARNING",
        "handlers": config["root"]["handlers"],
        "propagate": False
    }
    
    # Reducir verbosidad de librerías externas
    config["loggers"]["uvicorn"] = {
        "level": "INFO",
        "propagate": True
    }
    
    config["loggers"]["sqlalchemy"] = {
        "level": "WARNING",
        "propagate": True
    }
    
    config["loggers"]["redis"] = {
        "level": "WARNING",
        "propagate": True
    }
    
    # Crear directorio de logs si no existe
    if environment == "production":
        os.makedirs("logs", exist_ok=True)
    
    # Aplicar configuración
    logging.config.dictConfig(config)
    
    # Log de confirmación
    logger = logging.getLogger("versaai")
    logger.info(f"Logging configurado para entorno: {environment} (nivel: {log_level})")


class RequestLogger:
    """Logger especializado para requests HTTP"""
    
    def __init__(self):
        self.logger = logging.getLogger("versaai.requests")
    
    def log_request(self, request_id: str, method: str, path: str, 
                   user_id: str = None, ip: str = None):
        """Log de inicio de request"""
        extra = {
            'request_id': request_id,
            'method': method,
            'path': path,
            'event': 'request_start'
        }
        
        if user_id:
            extra['user_id'] = user_id
        if ip:
            extra['client_ip'] = ip
            
        self.logger.info(f"Request started: {method} {path}", extra=extra)
    
    def log_response(self, request_id: str, status_code: int, 
                    execution_time: float, response_size: int = None):
        """Log de respuesta"""
        extra = {
            'request_id': request_id,
            'status_code': status_code,
            'execution_time': execution_time,
            'event': 'request_complete'
        }
        
        if response_size:
            extra['response_size_bytes'] = response_size
        
        level = "INFO"
        if status_code >= 400:
            level = "WARNING"
        if status_code >= 500:
            level = "ERROR"
            
        getattr(self.logger, level.lower())(
            f"Request completed: {status_code} ({execution_time:.3f}s)",
            extra=extra
        )


class SecurityLogger:
    """Logger especializado para eventos de seguridad"""
    
    def __init__(self):
        self.logger = logging.getLogger("versaai.security")
    
    def log_auth_attempt(self, username: str, success: bool, ip: str = None):
        """Log de intento de autenticación"""
        extra = {
            'username': username,
            'auth_success': success,
            'event': 'auth_attempt'
        }
        
        if ip:
            extra['client_ip'] = ip
        
        if success:
            self.logger.info(f"Successful authentication for {username}", extra=extra)
        else:
            self.logger.warning(f"Failed authentication for {username}", extra=extra)
    
    def log_rate_limit(self, ip: str, endpoint: str):
        """Log de rate limiting"""
        extra = {
            'client_ip': ip,
            'endpoint': endpoint,
            'event': 'rate_limit_exceeded'
        }
        
        self.logger.warning(f"Rate limit exceeded from {ip} on {endpoint}", extra=extra)
    
    def log_suspicious_activity(self, description: str, ip: str = None, 
                              user_id: str = None, details: Dict[str, Any] = None):
        """Log de actividad sospechosa"""
        extra = {
            'event': 'suspicious_activity',
            'description': description
        }
        
        if ip:
            extra['client_ip'] = ip
        if user_id:
            extra['user_id'] = user_id
        if details:
            extra.update(details)
        
        self.logger.error(f"Suspicious activity detected: {description}", extra=extra)


# Instancias globales
request_logger = RequestLogger()
security_logger = SecurityLogger()