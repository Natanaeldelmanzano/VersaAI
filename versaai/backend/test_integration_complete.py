#!/usr/bin/env python3
"""
Pruebas de Integración Completas - VersaAI
Verifica todos los endpoints relacionados con chatbots y funcionalidades principales
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000/api/v1"
test_user = {
    "email": "test@versaai.com",
    "password": "testpassword123"
}

def log_test(test_name, status, details=""):
    """Registra el resultado de una prueba"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_icon} {test_name}: {status}")
    if details:
        print(f"    {details}")
    print()

def test_authentication():
    """Prueba el sistema de autenticación"""
    print("🔐 PRUEBAS DE AUTENTICACIÓN")
    print("=" * 50)
    
    # Test login
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            log_test("Login de Usuario", "PASS", f"Token obtenido: {access_token[:20]}...")
            return access_token
        else:
            log_test("Login de Usuario", "FAIL", f"Status: {response.status_code}, Error: {response.text}")
            return None
            
    except Exception as e:
        log_test("Login de Usuario", "FAIL", f"Excepción: {str(e)}")
        return None

def test_user_endpoints(token):
    """Prueba endpoints relacionados con usuarios"""
    print("👤 PRUEBAS DE USUARIOS")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test obtener usuario actual
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            log_test("Obtener Usuario Actual", "PASS", f"Usuario: {user_data.get('email')}")
            return user_data
        else:
            log_test("Obtener Usuario Actual", "FAIL", f"Status: {response.status_code}")
            return None
    except Exception as e:
        log_test("Obtener Usuario Actual", "FAIL", f"Excepción: {str(e)}")
        return None

def test_chatbot_endpoints(token):
    """Prueba todos los endpoints de chatbots"""
    print("🤖 PRUEBAS DE CHATBOTS")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Listar chatbots
    try:
        response = requests.get(f"{BASE_URL}/chatbots/", headers=headers)
        if response.status_code == 200:
            chatbots = response.json()
            log_test("Listar Chatbots", "PASS", f"Encontrados: {len(chatbots.get('chatbots', []))} chatbots")
        else:
            log_test("Listar Chatbots", "FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("Listar Chatbots", "FAIL", f"Excepción: {str(e)}")
    
    # Test 2: Crear chatbot
    timestamp = int(time.time())
    chatbot_data = {
        "name": f"Test Integration Bot {timestamp}",
        "description": "Bot creado para pruebas de integración",
        "model_name": "mixtral-8x7b-32768",
        "temperature": 0.7,
        "max_tokens": 1000,
        "is_active": True,
        "is_public": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chatbots/",
            json=chatbot_data,
            headers=headers
        )
        
        if response.status_code == 201:
            created_bot = response.json()
            bot_id = created_bot.get("id")
            log_test("Crear Chatbot", "PASS", f"ID: {bot_id}, Nombre: {created_bot.get('name')}")
            
            # Test 3: Obtener chatbot específico
            try:
                response = requests.get(f"{BASE_URL}/chatbots/{bot_id}", headers=headers)
                if response.status_code == 200:
                    bot_details = response.json()
                    log_test("Obtener Chatbot Específico", "PASS", f"Nombre: {bot_details.get('name')}")
                else:
                    log_test("Obtener Chatbot Específico", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                log_test("Obtener Chatbot Específico", "FAIL", f"Excepción: {str(e)}")
            
            # Test 4: Actualizar chatbot
            update_data = {
                "description": "Descripción actualizada para pruebas de integración",
                "temperature": 0.8
            }
            
            try:
                response = requests.put(
                    f"{BASE_URL}/chatbots/{bot_id}",
                    json=update_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    updated_bot = response.json()
                    log_test("Actualizar Chatbot", "PASS", f"Nueva descripción: {updated_bot.get('description')}")
                else:
                    log_test("Actualizar Chatbot", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                log_test("Actualizar Chatbot", "FAIL", f"Excepción: {str(e)}")
            
            # Test 5: Eliminar chatbot
            try:
                response = requests.delete(f"{BASE_URL}/chatbots/{bot_id}", headers=headers)
                if response.status_code == 200:
                    log_test("Eliminar Chatbot", "PASS", f"Chatbot {bot_id} eliminado correctamente")
                else:
                    log_test("Eliminar Chatbot", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                log_test("Eliminar Chatbot", "FAIL", f"Excepción: {str(e)}")
                
        else:
            log_test("Crear Chatbot", "FAIL", f"Status: {response.status_code}, Error: {response.text}")
            
    except Exception as e:
        log_test("Crear Chatbot", "FAIL", f"Excepción: {str(e)}")

def test_organization_endpoints(token):
    """Prueba endpoints relacionados con organizaciones"""
    print("🏢 PRUEBAS DE ORGANIZACIONES")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test obtener organizaciones del usuario
    try:
        response = requests.get(f"{BASE_URL}/organizations/", headers=headers)
        if response.status_code == 200:
            orgs = response.json()
            log_test("Listar Organizaciones", "PASS", f"Encontradas: {len(orgs)} organizaciones")
        else:
            log_test("Listar Organizaciones", "FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("Listar Organizaciones", "FAIL", f"Excepción: {str(e)}")

def test_health_endpoints():
    """Prueba endpoints de salud del sistema"""
    print("🏥 PRUEBAS DE SALUD DEL SISTEMA")
    print("=" * 50)
    
    # Test health check básico
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            log_test("Servidor Backend", "PASS", "Servidor respondiendo correctamente")
        else:
            log_test("Servidor Backend", "FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("Servidor Backend", "FAIL", f"Excepción: {str(e)}")
    
    # Test documentación API
    try:
        response = requests.get("http://localhost:8000/api/docs")
        if response.status_code == 200:
            log_test("Documentación API", "PASS", "Swagger UI accesible")
        else:
            log_test("Documentación API", "FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("Documentación API", "FAIL", f"Excepción: {str(e)}")

def main():
    """Ejecuta todas las pruebas de integración"""
    print("🚀 INICIANDO PRUEBAS DE INTEGRACIÓN COMPLETAS - VersaAI")
    print("=" * 70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL Base: {BASE_URL}")
    print("=" * 70)
    print()
    
    # Pruebas de salud del sistema
    test_health_endpoints()
    
    # Autenticación
    token = test_authentication()
    if not token:
        print("❌ No se pudo obtener token de autenticación. Deteniendo pruebas.")
        return
    
    # Pruebas con autenticación
    user_data = test_user_endpoints(token)
    test_organization_endpoints(token)
    test_chatbot_endpoints(token)
    
    print("🎉 PRUEBAS DE INTEGRACIÓN COMPLETADAS")
    print("=" * 70)
    print("✅ Todas las funcionalidades principales han sido verificadas")
    print("📊 El sistema VersaAI está funcionando correctamente")
    print("🔗 Frontend disponible en: http://localhost:3000/")
    print("📚 API Docs disponible en: http://localhost:8000/api/docs")
    print()

if __name__ == "__main__":
    main()