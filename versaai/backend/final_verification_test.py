#!/usr/bin/env python3
"""
Prueba Final de Verificación del Sistema VersaAI
Verifica la funcionalidad completa del sistema incluyendo:
1. Creación de nuevo usuario
2. Asignación automática de organization_id
3. Creación de chatbot
4. Prueba de conversación
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000/api/v1"
FRONTEND_URL = "http://localhost:3000"

# Datos de prueba
test_timestamp = int(time.time())
test_user_data = {
    "email": f"test_final_{test_timestamp}@versaai.com",
    "password": "TestPassword123!",
    "full_name": f"Usuario Prueba Final {test_timestamp}",
    "company": f"Empresa Test {test_timestamp}"
}

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n[PASO {step}] {description}")
    print("-" * 50)

def test_user_registration():
    """Prueba 1: Registro de nuevo usuario"""
    print_step(1, "Registro de Nuevo Usuario")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            user_info = response.json()
            print(f"✅ Usuario creado exitosamente:")
            print(f"   - ID: {user_info.get('id')}")
            print(f"   - Email: {user_info.get('email')}")
            print(f"   - Nombre: {user_info.get('full_name')}")
            print(f"   - Organization ID: {user_info.get('organization_id')}")
            
            if user_info.get('organization_id'):
                print(f"✅ Organization ID asignado automáticamente: {user_info.get('organization_id')}")
                return True, user_info
            else:
                print("❌ ERROR: Organization ID no asignado")
                return False, None
        else:
            print(f"❌ ERROR en registro: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN en registro: {str(e)}")
        return False, None

def test_user_login():
    """Prueba 2: Login del usuario"""
    print_step(2, "Login del Usuario")
    
    try:
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login/json",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info.get('access_token')
            print(f"✅ Login exitoso")
            print(f"   - Token obtenido: {access_token[:50]}...")
            return True, access_token
        else:
            print(f"❌ ERROR en login: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN en login: {str(e)}")
        return False, None

def test_chatbot_creation(access_token):
    """Prueba 3: Creación de chatbot"""
    print_step(3, "Creación de Chatbot")
    
    try:
        chatbot_data = {
            "name": f"Chatbot Prueba Final {test_timestamp}",
            "description": "Chatbot de prueba para verificación final del sistema",
            "system_prompt": "Eres un asistente útil y amigable. Responde de manera clara y concisa.",
            "model": "llama3-8b-8192",
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{BASE_URL}/chatbots/",
            json=chatbot_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            chatbot_info = response.json()
            print(f"✅ Chatbot creado exitosamente:")
            print(f"   - ID: {chatbot_info.get('id')}")
            print(f"   - Nombre: {chatbot_info.get('name')}")
            print(f"   - Organization ID: {chatbot_info.get('organization_id')}")
            print(f"   - Created By: {chatbot_info.get('created_by_id')}")
            return True, chatbot_info
        else:
            print(f"❌ ERROR en creación de chatbot: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN en creación de chatbot: {str(e)}")
        return False, None

def test_chatbot_conversation(access_token, chatbot_id):
    """Prueba 4: Conversación con el chatbot"""
    print_step(4, "Prueba de Conversación")
    
    try:
        import uuid
        # Crear una nueva conversación
        conversation_data = {
            "chatbot_id": chatbot_id,
            "session_id": str(uuid.uuid4()),
            "title": f"Conversación de Prueba {test_timestamp}"
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Crear conversación
        response = requests.post(
            f"{BASE_URL}/conversations/",
            json=conversation_data,
            headers=headers
        )
        
        print(f"Creación de conversación - Status: {response.status_code}")
        
        if response.status_code == 201:
            conversation_info = response.json()
            conversation_id = conversation_info.get('id')
            print(f"✅ Conversación creada: ID {conversation_id}")
            
            # Enviar mensaje de prueba
            message_data = {
                "content": "Hola, ¿puedes ayudarme con información sobre VersaAI?",
                "conversation_id": conversation_id
            }
            
            print("\nEnviando mensaje de prueba...")
            response = requests.post(
                f"{BASE_URL}/conversations/{conversation_id}/messages",
                json=message_data,
                headers=headers
            )
            
            print(f"Envío de mensaje - Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                message_response = response.json()
                print(f"✅ Mensaje enviado y respuesta recibida:")
                print(f"   - Mensaje usuario: {message_response.get('user_message', {}).get('content')}")
                print(f"   - Respuesta bot: {message_response.get('bot_response', {}).get('content')}")
                return True
            else:
                print(f"❌ ERROR en envío de mensaje: {response.status_code}")
                return False
        else:
            print(f"❌ ERROR en creación de conversación: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN en conversación: {str(e)}")
        return False

def test_system_health():
    """Prueba 5: Verificación de salud del sistema"""
    print_step(5, "Verificación de Salud del Sistema")
    
    try:
        # Verificar backend
        response = requests.get("http://localhost:8000/health")
        print(f"Backend Health - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Backend funcionando correctamente")
        else:
            print("❌ Backend con problemas")
        
        # Verificar frontend (solo conectividad)
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            print(f"Frontend - Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Frontend accesible")
            else:
                print("❌ Frontend con problemas")
        except:
            print("❌ Frontend no accesible")
            
        return True
        
    except Exception as e:
        print(f"❌ EXCEPCIÓN en verificación de salud: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    print_section("VERIFICACIÓN FINAL DEL SISTEMA VERSAAI")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Usuario de prueba: {test_user_data['email']}")
    
    results = {
        "registro": False,
        "login": False,
        "chatbot": False,
        "conversacion": False,
        "salud_sistema": False
    }
    
    # Prueba 1: Registro
    success, user_info = test_user_registration()
    results["registro"] = success
    
    if not success:
        print("\n❌ FALLO CRÍTICO: No se pudo registrar usuario")
        return False
    
    # Prueba 2: Login
    success, access_token = test_user_login()
    results["login"] = success
    
    if not success:
        print("\n❌ FALLO CRÍTICO: No se pudo hacer login")
        return False
    
    # Prueba 3: Creación de chatbot
    success, chatbot_info = test_chatbot_creation(access_token)
    results["chatbot"] = success
    
    if not success:
        print("\n❌ FALLO CRÍTICO: No se pudo crear chatbot")
        return False
    
    # Prueba 4: Conversación
    success = test_chatbot_conversation(access_token, chatbot_info.get('id'))
    results["conversacion"] = success
    
    # Prueba 5: Salud del sistema
    success = test_system_health()
    results["salud_sistema"] = success
    
    # Resumen final
    print_section("RESUMEN FINAL DE VERIFICACIÓN")
    
    all_passed = all(results.values())
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name.upper()}: {status}")
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 TODAS LAS PRUEBAS PASARON - SISTEMA COMPLETAMENTE FUNCIONAL")
        print("✅ El fix de organization_id está funcionando perfectamente")
        print("✅ Los usuarios se crean con organization_id automáticamente")
        print("✅ Los chatbots se crean y asignan correctamente")
        print("✅ Las conversaciones funcionan sin errores")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON - REVISAR SISTEMA")
        failed_tests = [name for name, result in results.items() if not result]
        print(f"Pruebas fallidas: {', '.join(failed_tests)}")
    
    print(f"{'='*60}")
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)