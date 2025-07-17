#!/usr/bin/env python3
"""
Script de diagnóstico detallado para el endpoint de chatbots
"""

import requests
import json
import traceback
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test1@versaai.com"
TEST_PASSWORD = "test123456"

def get_auth_token():
    """Obtener token de autenticación"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_health():
    """Probar endpoint de salud"""
    print("\n🏥 PROBANDO HEALTH CHECK...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Health check OK: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

def test_user_profile(token):
    """Probar endpoint de perfil de usuario"""
    print("\n👤 PROBANDO PERFIL DE USUARIO...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Usuario: {data.get('email')} (Org: {data.get('organization_id')})")
            return True, data
        else:
            print(f"❌ Error: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

def test_chatbots_detailed(token):
    """Probar endpoint de chatbots con detalles"""
    print("\n🤖 PROBANDO ENDPOINT DE CHATBOTS (DETALLADO)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Probar diferentes parámetros
    test_cases = [
        {
            "name": "Sin parámetros",
            "url": f"{BASE_URL}/api/v1/chatbots/"
        },
        {
            "name": "Con límite pequeño",
            "url": f"{BASE_URL}/api/v1/chatbots/?limit=1"
        },
        {
            "name": "Con skip=0",
            "url": f"{BASE_URL}/api/v1/chatbots/?skip=0&limit=10"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n  📋 {test_case['name']}:")
        try:
            response = requests.get(test_case['url'], headers=headers)
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"    ✅ Éxito: {len(data.get('chatbots', []))} chatbots")
                print(f"    Total: {data.get('total', 0)}")
                print(f"    Página: {data.get('page', 1)} de {data.get('pages', 1)}")
                return True, data.get('chatbots', [])
            else:
                print(f"    ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"    ❌ Excepción: {e}")
            traceback.print_exc()
    
    return False, []

def test_database_direct():
    """Probar conexión directa a la base de datos"""
    print("\n🗄️ PROBANDO CONEXIÓN DIRECTA A BD...")
    try:
        # Intentar importar y usar SQLAlchemy directamente
        import sys
        import os
        sys.path.append('backend/src')
        
        from core.database import get_db
        from models.chatbot import Chatbot
        
        # Obtener sesión de BD
        db = next(get_db())
        
        # Contar chatbots
        count = db.query(Chatbot).count()
        print(f"✅ Chatbots en BD: {count}")
        
        # Obtener algunos chatbots
        chatbots = db.query(Chatbot).limit(3).all()
        for chatbot in chatbots:
            print(f"  - ID: {chatbot.id}, Nombre: {chatbot.name}, Org: {chatbot.organization_id}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en BD: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO DETALLADO DEL ENDPOINT DE CHATBOTS")
    print("=" * 60)
    
    # Test 1: Health check
    health_ok = test_health()
    
    # Test 2: Obtener token
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token - abortando")
        return
    
    print(f"✅ Token obtenido: {token[:20]}...")
    
    # Test 3: Perfil de usuario
    profile_ok, user_data = test_user_profile(token)
    
    # Test 4: Chatbots detallado
    chatbots_ok, chatbots = test_chatbots_detailed(token)
    
    # Test 5: Base de datos directa
    db_ok = test_database_direct()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO:")
    print("=" * 60)
    print(f"🏥 Health Check: {'✅ OK' if health_ok else '❌ FAIL'}")
    print(f"🔐 Autenticación: {'✅ OK' if token else '❌ FAIL'}")
    print(f"👤 Perfil Usuario: {'✅ OK' if profile_ok else '❌ FAIL'}")
    print(f"🤖 Endpoint Chatbots: {'✅ OK' if chatbots_ok else '❌ FAIL'}")
    print(f"🗄️ Base de Datos: {'✅ OK' if db_ok else '❌ FAIL'}")
    
    if user_data:
        print(f"\n👤 Usuario actual: {user_data.get('email')} (Org: {user_data.get('organization_id')})")
    
    if not chatbots_ok:
        print("\n⚠️ RECOMENDACIONES:")
        print("1. Revisar logs del servidor backend")
        print("2. Verificar que la tabla chatbots existe")
        print("3. Verificar permisos de la organización")
        print("4. Revisar el modelo ChatbotWithStats")
    
    print(f"\n🕒 Diagnóstico completado: {datetime.now()}")

if __name__ == "__main__":
    main()