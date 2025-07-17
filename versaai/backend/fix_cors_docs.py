#!/usr/bin/env python3
"""
Script para probar una configuración temporal de CORS más permisiva
para solucionar el problema de páginas en blanco en la documentación
"""

import os
import sys
import shutil
from pathlib import Path

def backup_config():
    """Crear backup del archivo de configuración actual"""
    config_path = Path("src/core/config.py")
    backup_path = Path("src/core/config.py.backup")
    
    if config_path.exists():
        shutil.copy2(config_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        return True
    else:
        print(f"❌ No se encontró el archivo de configuración: {config_path}")
        return False

def create_permissive_config():
    """Crear una configuración temporal más permisiva para CORS"""
    config_content = '''from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "VersaAI Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_HASH_ROUNDS: int = 12
    
    # Database
    DATABASE_URL: str = "sqlite:///./versaai.db"  # Default to SQLite for development
    DATABASE_POOL_SIZE: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None
    REDIS_POOL_SIZE: int = 10
    REDIS_POOL_TIMEOUT: int = 30
    REDIS_CACHE_TTL: int = 3600
    REDIS_MAX_CONNECTIONS: int = 10
    
    # Groq AI
    GROQ_API_KEY: str = ""
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "mixtral-8x7b-32768"
    GROQ_MAX_TOKENS: int = 2000
    GROQ_TEMPERATURE: float = 0.7
    GROQ_TIMEOUT: int = 30
    
    # OpenAI (optional)
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Embedding Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    EMBEDDING_MODEL_DIMENSION: int = 384
    EMBEDDING_BATCH_SIZE: int = 32
    
    # CORS - CONFIGURACIÓN TEMPORAL MÁS PERMISIVA
    ALLOWED_HOSTS: List[str] = ["*"]  # Permitir todos los hosts temporalmente
    ALLOWED_ORIGINS: List[str] = ["*"]  # Permitir todos los orígenes temporalmente
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # File uploads - Estandarizado en MB
    MAX_FILE_SIZE_MB: int = 10
    MAX_FILES_PER_UPLOAD: int = 10
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "txt", "docx", "md", "html", "csv"]
    UPLOAD_DIR: str = "uploads"
    DOCUMENTS_UPLOAD_DIR: str = "uploads/documents"
    AVATARS_UPLOAD_DIR: str = "uploads/avatars"
    
    # Data directory
    DATA_DIR: str = "./data"
    
    # AI Settings
    MAX_CONTEXT_LENGTH: int = 4000
    DEFAULT_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate limiting - Estandarizado
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    WIDGET_RATE_LIMIT_REQUESTS_PER_MINUTE: int = 180
    WIDGET_RATE_LIMIT_BURST: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

# Create settings instance
settings = Settings()

# Ensure upload directory exists
upload_path = Path(settings.UPLOAD_DIR)
upload_path.mkdir(exist_ok=True)
'''
    
    config_path = Path("src/core/config.py")
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"✅ Configuración temporal creada: {config_path}")
        return True
    except Exception as e:
        print(f"❌ Error al crear configuración temporal: {e}")
        return False

def restore_config():
    """Restaurar la configuración original desde el backup"""
    config_path = Path("src/core/config.py")
    backup_path = Path("src/core/config.py.backup")
    
    if backup_path.exists():
        shutil.copy2(backup_path, config_path)
        print(f"✅ Configuración original restaurada desde: {backup_path}")
        return True
    else:
        print(f"❌ No se encontró el backup: {backup_path}")
        return False

def main():
    """Función principal"""
    print("🔧 HERRAMIENTA DE CORRECCIÓN DE CORS PARA DOCUMENTACIÓN")
    print("="*60)
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python fix_cors_docs.py apply    - Aplicar configuración permisiva")
        print("  python fix_cors_docs.py restore  - Restaurar configuración original")
        return
    
    action = sys.argv[1].lower()
    
    if action == "apply":
        print("🔄 Aplicando configuración CORS permisiva...")
        
        # Crear backup
        if not backup_config():
            return
        
        # Aplicar configuración permisiva
        if create_permissive_config():
            print("\n✅ CONFIGURACIÓN APLICADA EXITOSAMENTE")
            print("\n📋 Próximos pasos:")
            print("1. Reiniciar el servidor backend")
            print("2. Probar las URLs de documentación:")
            print("   - http://localhost:8000/api/docs")
            print("   - http://localhost:8000/api/redoc")
            print("3. Si funciona, el problema era CORS")
            print("4. Restaurar configuración original con: python fix_cors_docs.py restore")
            print("\n⚠️  IMPORTANTE: Esta configuración es TEMPORAL y menos segura")
            print("   Solo para diagnóstico. Restaurar después de las pruebas.")
        
    elif action == "restore":
        print("🔄 Restaurando configuración original...")
        
        if restore_config():
            print("\n✅ CONFIGURACIÓN ORIGINAL RESTAURADA")
            print("\n📋 Próximos pasos:")
            print("1. Reiniciar el servidor backend")
            print("2. La configuración CORS vuelve a ser restrictiva")
            print("3. Si las páginas siguen funcionando, el problema estaba en CORS")
            print("4. Si vuelven a fallar, buscar otra causa")
        
    else:
        print(f"❌ Acción no reconocida: {action}")
        print("Acciones válidas: apply, restore")

if __name__ == "__main__":
    main()