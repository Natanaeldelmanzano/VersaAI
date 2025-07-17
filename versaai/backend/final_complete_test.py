import requests
import json
from datetime import datetime

# VERIFICACIÓN FINAL COMPLETA DEL SISTEMA VERSAAI
# Todas las funcionalidades principales

BASE_URL = "http://localhost:8000/api/v1"

def complete_system_test():
    """Prueba completa de todas las funcionalidades"""

    print("🚀 VERIFICACIÓN FINAL COMPLETA - VERSAAI")
    print("="*60)

    timestamp = int(datetime.now().timestamp())
    results = {
        "registro": False,
        "login": False,
        "chatbot": False,
        "conversacion": False,
        "mensaje": False,
        "salud": False
    }

    # PASO 1: Registro
    print(f"\n[PASO 1] Registro de Usuario")
    print("-" * 40)

    user_data = {
        "email": f"final_test_{timestamp}@versaai.com",
        "username": f"final_test_{timestamp}",
        "password": "password123",
        "full_name": f"Usuario Final {timestamp}"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 201:
            user_info = response.json()
            print(f"✅ REGISTRO EXITOSO")
            print(f"   - Usuario ID: {user_info['id']}")
            print(f"   - Email: {user_info['email']}")
            print(f"   - Organization ID: {user_info['organization_id']}")
            results["registro"] = True
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(f"   Response: {response.text}")
            return results
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return results

    # PASO 2: Login
    print(f"\n[PASO 2] Autenticación")
    print("-" * 40)

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            auth_info = response.json()
            token = auth_info["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print(f"✅ LOGIN EXITOSO")
            print(f"   - Token obtenido: {token[:50]}...")
            results["login"] = True
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   Response: {response.text}")
            return results
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return results

    # PASO 3: Crear Chatbot
    print(f"\n[PASO 3] Creación de Chatbot")
    print("-" * 40)

    chatbot_data = {
        "name": f"Chatbot Final {timestamp}",
        "description": "Chatbot de prueba final completa",
        "model_name": "mixtral-8x7b-32768",
        "system_prompt": "Eres un asistente útil para pruebas finales.",
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(f"{BASE_URL}/chatbots/", json=chatbot_data, headers=headers)
        if response.status_code == 201:
            chatbot_info = response.json()
            chatbot_id = chatbot_info["id"]
            print(f"✅ CHATBOT CREADO")
            print(f"   - Chatbot ID: {chatbot_id}")
            print(f"   - Nombre: {chatbot_info['name']}")
            print(f"   - Widget ID: {chatbot_info['widget_id']}")
            results["chatbot"] = True
        else:
            print(f"❌ Error creando chatbot: {response.status_code}")
            print(f"   Response: {response.text}")
            return results
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return results

    # PASO 4: Crear Conversación
    print(f"\n[PASO 4] Creación de Conversación")
    print("-" * 40)

    import uuid
    
    conversation_data = {
        "chatbot_id": chatbot_id,
        "session_id": str(uuid.uuid4())
    }

    try:
        response = requests.post(f"{BASE_URL}/conversations/",
                               json=conversation_data,
                               headers=headers)
        if response.status_code == 201:
            conversation_info = response.json()
            conversation_id = conversation_info["id"]
            print(f"✅ CONVERSACIÓN CREADA")
            print(f"   - Conversación ID: {conversation_id}")
            print(f"   - Session ID: {conversation_info['session_id']}")
            print(f"   - Status: {conversation_info['status']}")
            results["conversacion"] = True
        else:
            print(f"❌ Error creando conversación: {response.status_code}")
            print(f"   Response: {response.text}")
            return results
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return results

    # PASO 5: Enviar Mensaje
    print(f"\n[PASO 5] Envío de Mensaje")
    print("-" * 40)

    message_data = {
        "content": "Hola, esta es una prueba final del sistema",
        "message_type": "user",
        "conversation_id": conversation_id
    }

    try:
        response = requests.post(f"{BASE_URL}/conversations/{conversation_id}/messages",
                               json=message_data,
                               headers=headers)
        if response.status_code == 201:
            message_info = response.json()
            print(f"✅ MENSAJE ENVIADO")
            print(f"   - Mensaje ID: {message_info['id']}")
            print(f"   - Contenido: {message_info['content']}")
            results["mensaje"] = True
        else:
            print(f"❌ Error enviando mensaje: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # PASO 6: Health Check
    print(f"\n[PASO 6] Verificación de Salud")
    print("-" * 40)

    try:
        response = requests.get(f"http://localhost:8000/health")
        if response.status_code == 200:
            print(f"✅ SISTEMA SALUDABLE")
            results["salud"] = True
        else:
            print(f"❌ Problemas de salud: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    return results

def print_final_report(results):
    """Imprime el reporte final"""

    print(f"\n" + "="*60)
    print(f"📊 REPORTE FINAL DE VERIFICACIÓN")
    print(f"="*60)

    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100

    print(f"🎯 RESULTADOS:")
    for test, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {test.upper()}: {'PASÓ' if status else 'FALLÓ'}")

    print(f"\n📈 ESTADÍSTICAS:")
    print(f"   - Pruebas pasadas: {passed_tests}/{total_tests}")
    print(f"   - Tasa de éxito: {success_rate:.1f}%")

    if success_rate == 100:
        print(f"\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print(f"   ✅ Todas las funcionalidades operativas")
        print(f"   ✅ Listo para producción")
    elif success_rate >= 80:
        print(f"\n⚠️  SISTEMA MAYORMENTE FUNCIONAL")
        print(f"   ✅ Funcionalidades core operativas")
        print(f"   🔧 Revisar funcionalidades fallidas")
    else:
        print(f"\n❌ SISTEMA CON PROBLEMAS CRÍTICOS")
        print(f"   🚨 Requiere corrección inmediata")

    print(f"="*60)

if __name__ == "__main__":
    results = complete_system_test()
    print_final_report(results)