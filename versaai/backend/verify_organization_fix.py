# verify_organization_fix.py
# Script para verificar que la corrección del organization_id funcionó

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.database import engine, SessionLocal
from src.core.config import settings

def verify_database():
    """Verificar estado de la base de datos"""
    try:
        # Usar la configuración existente de la base de datos
        db = SessionLocal()
        
        print(f"🔗 Conectando a la base de datos: {settings.DATABASE_URL[:20]}...")
        
        print("🔍 VERIFICANDO BASE DE DATOS...")
        print("=" * 50)
        
        # Verificar columna organization_id en users
        result = db.execute(text("""
            SELECT COUNT(*) FROM information_schema.columns
            WHERE table_name='users' AND column_name='organization_id';
        """))
        
        if result.scalar() > 0:
            print("✅ Columna organization_id existe en users")
        else:
            print("❌ Columna organization_id NO existe en users")
            return False
        
        # Verificar usuarios sin organization_id
        result = db.execute(text("""
            SELECT COUNT(*) FROM users WHERE organization_id IS NULL;
        """))
        null_count = result.scalar()
        
        if null_count == 0:
            print("✅ Todos los usuarios tienen organization_id")
        else:
            print(f"⚠️  {null_count} usuarios sin organization_id")
        
        # Verificar organizaciones
        result = db.execute(text("""
            SELECT COUNT(*) FROM organizations;
        """))
        org_count = result.scalar()
        print(f"📊 Total organizaciones: {org_count}")
        
        # Verificar relación usuarios-organizaciones
        result = db.execute(text("""
            SELECT u.id, u.email, u.organization_id, o.name as org_name
            FROM users u
            LEFT JOIN organizations o ON u.organization_id = o.id
            LIMIT 5;
        """))
        
        print("\n👥 Muestra de usuarios y sus organizaciones:")
        for row in result.fetchall():
            user_id, email, org_id, org_name = row
            print(f"   Usuario {user_id} ({email}) -> Org {org_id} ({org_name})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando DB: {e}")
        return False

def verify_api():
    """Verificar que la API está funcionando"""
    try:
        print("\n🔍 VERIFICANDO API...")
        print("=" * 50)
        
        # Verificar health endpoint
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ API está funcionando")
        else:
            print(f"⚠️ API responde pero con código: {response.status_code}")
        
        # Verificar documentación
        response = requests.get("http://localhost:8000/api/docs")
        if response.status_code == 200:
            print("✅ Documentación API accesible")
        else:
            print("⚠️ Documentación API no accesible")
        
        return True
        
    except Exception as e:
        print(f"❌ API no está accesible: {e}")
        return False

def test_chatbot_creation():
    """Probar la creación de un chatbot"""
    try:
        print("\n🤖 PROBANDO CREACIÓN DE CHATBOT...")
        print("=" * 50)
        
        base_url = "http://localhost:8000/api/v1"
        
        # 1. Login para obtener token
        login_data = {
            "email": "integration_test@versaai.com",
            "password": "testpassword123"
        }
        
        login_response = requests.post(
            f"{base_url}/auth/login/json",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✅ Login exitoso")
        
        # 2. Obtener información del usuario
        user_response = requests.get(f"{base_url}/auth/me", headers=headers)
        if user_response.status_code == 200:
            user_data = user_response.json()
            print(f"✅ Usuario: {user_data.get('email')}")
            print(f"📋 Organization ID: {user_data.get('organization_id', 'NO ENCONTRADO')}")
        
        # 3. Intentar crear un chatbot de prueba con nombre único
        from datetime import datetime
        timestamp = int(datetime.now().timestamp())
        chatbot_data = {
            "name": f"Test Chatbot Verificación {timestamp}",
            "description": "Chatbot de prueba para verificar la corrección",
            "system_prompt": "Eres un asistente útil",
            "model": "llama3-8b-8192",
            "temperature": 0.7,
            "max_tokens": 1000,
            "is_active": True
        }
        
        chatbot_response = requests.post(
            f"{base_url}/chatbots/",
            json=chatbot_data,
            headers=headers
        )
        
        if chatbot_response.status_code == 201:
            chatbot = chatbot_response.json()
            print(f"✅ Chatbot creado exitosamente: {chatbot.get('name')}")
            print(f"📋 ID: {chatbot.get('id')}")
            print(f"🏢 Organization ID: {chatbot.get('organization_id')}")
            return True
        else:
            print(f"❌ Error creando chatbot: {chatbot_response.status_code}")
            print(f"Response: {chatbot_response.text}")
            return False
        
    except Exception as e:
        print(f"❌ Error en test de chatbot: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔧 VERIFICACIÓN COMPLETA DE LA CORRECCIÓN")
    print("=" * 60)
    
    # Verificar base de datos
    db_ok = verify_database()
    
    # Verificar API
    api_ok = verify_api()
    
    # Probar creación de chatbot
    chatbot_ok = test_chatbot_creation()
    
    # Resumen final
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    print(f"Base de datos: {'✅ OK' if db_ok else '❌ ERROR'}")
    print(f"API: {'✅ OK' if api_ok else '❌ ERROR'}")
    print(f"Creación de chatbot: {'✅ OK' if chatbot_ok else '❌ ERROR'}")
    
    if db_ok and api_ok and chatbot_ok:
        print("\n🎉 ¡CORRECCIÓN EXITOSA! El problema de organization_id está resuelto.")
    else:
        print("\n⚠️ Algunos problemas persisten. Revisar los errores arriba.")
    
    return db_ok and api_ok and chatbot_ok

if __name__ == "__main__":
    main()