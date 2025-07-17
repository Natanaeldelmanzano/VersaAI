#!/usr/bin/env python3
"""
Script de verificación del sistema VersaAI
Verifica el estado de la base de datos, servicios y configuración
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from sqlalchemy import text
    from src.core.database import engine, get_db
    from src.core.config import settings
    from src.models.user import User
    from src.services.auth_service import AuthService
    import requests
except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
    print("💡 Ejecuta: pip install -r requirements.txt")
    sys.exit(1)

def print_header(title):
    """Imprime un encabezado formateado"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_status(item, status, details=""):
    """Imprime el estado de un elemento"""
    icon = "✅" if status else "❌"
    print(f"{icon} {item}: {'OK' if status else 'ERROR'}")
    if details:
        print(f"   📝 {details}")

def check_environment():
    """Verifica las variables de entorno"""
    print_header("VERIFICACIÓN DE ENTORNO")
    
    required_vars = [
        "GROQ_API_KEY",
        "SECRET_KEY",
        "DATABASE_URL"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Ocultar valores sensibles
            display_value = value[:10] + "..." if len(value) > 10 else value
            print_status(f"Variable {var}", True, f"Configurada: {display_value}")
        else:
            print_status(f"Variable {var}", False, "No configurada")
    
    # Verificar configuración de settings
    print(f"\n📊 Configuración actual:")
    print(f"   🗄️  Base de datos: {settings.DATABASE_URL}")
    print(f"   🤖 Modelo IA: {settings.GROQ_MODEL}")
    print(f"   🌐 CORS Origins: {settings.ALLOWED_ORIGINS}")
    print(f"   📁 Upload Max Size: {settings.MAX_FILE_SIZE_MB}MB")

def check_database():
    """Verifica la conexión y estado de la base de datos"""
    print_header("VERIFICACIÓN DE BASE DE DATOS")
    
    try:
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print_status("Conexión a base de datos", True, "Conectado exitosamente")
            
            # Verificar si es SQLite o PostgreSQL
            db_type = "SQLite" if "sqlite" in str(engine.url) else "PostgreSQL"
            print_status(f"Tipo de base de datos", True, db_type)
            
            # Verificar tablas existentes
            if "sqlite" in str(engine.url):
                tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            else:
                tables_query = "SELECT tablename FROM pg_tables WHERE schemaname='public'"
            
            tables_result = conn.execute(text(tables_query))
            tables = [row[0] for row in tables_result]
            
            if tables:
                print_status("Tablas en base de datos", True, f"Encontradas: {', '.join(tables)}")
            else:
                print_status("Tablas en base de datos", False, "No se encontraron tablas")
                print("   💡 Ejecuta: alembic upgrade head")
            
            # Verificar archivo de base de datos SQLite
            if "sqlite" in str(engine.url):
                db_file = str(engine.url).replace("sqlite:///", "")
                if os.path.exists(db_file):
                    size = os.path.getsize(db_file)
                    print_status("Archivo SQLite", True, f"Tamaño: {size} bytes")
                else:
                    print_status("Archivo SQLite", False, "Archivo no encontrado")
    
    except Exception as e:
        print_status("Conexión a base de datos", False, str(e))
        return False
    
    return True

def check_auth_service():
    """Verifica el servicio de autenticación"""
    print_header("VERIFICACIÓN DE AUTENTICACIÓN")
    
    try:
        auth_service = AuthService()
        
        # Verificar hash de contraseña
        test_password = "test123"
        hashed = auth_service.get_password_hash(test_password)
        verify_result = auth_service.verify_password(test_password, hashed)
        print_status("Hash de contraseñas", verify_result, "Funciona correctamente")
        
        # Verificar generación de tokens
        test_data = {"sub": "test@example.com", "user_id": 1}
        access_token = auth_service.create_access_token(test_data)
        refresh_token = auth_service.create_refresh_token(test_data)
        
        print_status("Generación de tokens", bool(access_token and refresh_token), 
                    "Access y refresh tokens generados")
        
        # Verificar validación de tokens
        try:
            decoded = auth_service.verify_token(access_token)
            print_status("Validación de tokens", True, "Token decodificado correctamente")
        except Exception as e:
            print_status("Validación de tokens", False, str(e))
    
    except Exception as e:
        print_status("Servicio de autenticación", False, str(e))
        return False
    
    return True

def check_backend_service():
    """Verifica si el backend está ejecutándose"""
    print_header("VERIFICACIÓN DE SERVICIOS")
    
    # Verificar backend
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print_status("Backend (Puerto 8000)", True, "Servicio activo")
            data = response.json()
            print(f"   📊 Respuesta: {data}")
        else:
            print_status("Backend (Puerto 8000)", False, f"Código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_status("Backend (Puerto 8000)", False, "Servicio no disponible")
        print("   💡 Ejecuta: python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
    
    # Verificar frontend
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print_status("Frontend (Puerto 3000)", True, "Servicio activo")
        else:
            print_status("Frontend (Puerto 3000)", False, f"Código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_status("Frontend (Puerto 3000)", False, "Servicio no disponible")
        print("   💡 Ejecuta: cd frontend && npm run dev")

def check_groq_service():
    """Verifica la conexión con Groq AI"""
    print_header("VERIFICACIÓN DE GROQ AI")
    
    try:
        from src.services.groq_service import GroqService
        
        groq_service = GroqService()
        
        if not groq_service.api_key:
            print_status("API Key de Groq", False, "No configurada")
            return False
        
        print_status("API Key de Groq", True, "Configurada")
        
        # Test simple de conexión (sin hacer llamada real para ahorrar tokens)
        print_status("Servicio Groq", True, "Configurado correctamente")
        print(f"   🤖 Modelo: {groq_service.model}")
        
    except Exception as e:
        print_status("Servicio Groq", False, str(e))
        return False
    
    return True

def generate_report():
    """Genera un reporte del estado del sistema"""
    print_header("REPORTE FINAL")
    
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Sistema: {os.name} - {sys.platform}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Directorio: {os.getcwd()}")
    
    print("\n📋 Próximos pasos recomendados:")
    print("   1. Si hay errores de base de datos: alembic upgrade head")
    print("   2. Si faltan servicios: iniciar backend y frontend")
    print("   3. Si falta configuración: revisar archivo .env")
    print("   4. Crear usuario de prueba con la API")
    print("   5. Probar integración frontend-backend")
    
    print("\n🔗 URLs importantes:")
    print("   📖 Documentación API: http://localhost:8000/docs")
    print("   🌐 Frontend: http://localhost:3000")
    print("   ⚡ API Health: http://localhost:8000/api/health")

def main():
    """Función principal"""
    print("🚀 VersaAI - Verificación del Sistema")
    print(f"Iniciando verificación en: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar todas las verificaciones
    check_environment()
    db_ok = check_database()
    auth_ok = check_auth_service()
    check_backend_service()
    groq_ok = check_groq_service()
    
    generate_report()
    
    # Resumen final
    print("\n" + "="*60)
    if db_ok and auth_ok and groq_ok:
        print("✅ Sistema verificado exitosamente")
        print("🎯 Listo para continuar con el desarrollo")
    else:
        print("⚠️  Se encontraron algunos problemas")
        print("🔧 Revisa los errores anteriores y sigue las recomendaciones")
    print("="*60)

if __name__ == "__main__":
    main()