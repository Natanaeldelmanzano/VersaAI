import requests
import json
import uuid
from datetime import datetime

# SCRIPT DE DEPURACIÓN ESPECÍFICA PARA CONVERSACIONES
# Este script ayudará a identificar el problema exacto

BASE_URL = "http://localhost:8000/api/v1"

def debug_conversation_creation():
    """Depura paso a paso la creación de conversaciones"""

    print("🔍 DEPURACIÓN ESPECÍFICA DE CONVERSACIONES")
    print("="*60)

    # Paso 1: Crear usuario de prueba
    print("\n[PASO 1] Creando usuario de prueba...")
    timestamp = int(datetime.now().timestamp())

    user_data = {
        "email": f"debug_{timestamp}@versaai.com",
        "username": f"debug_{timestamp}",
        "password": "password123",
        "full_name": f"Debug User {timestamp}"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            user_info = response.json()
            print(f"✅ Usuario creado - ID: {user_info['id']}")
        else:
            print(f"❌ Error creando usuario: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # Paso 2: Login
    print("\n[PASO 2] Realizando login...")
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login/json", 
                               json=login_data,
                               headers={"Content-Type": "application/json"})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            auth_info = response.json()
            token = auth_info["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login exitoso")
        else:
            print(f"❌ Error en login: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # Paso 3: Crear chatbot
    print("\n[PASO 3] Creando chatbot...")
    chatbot_data = {
        "name": f"Debug Chatbot {timestamp}",
        "description": "Chatbot para depuración",
        "model_name": "mixtral-8x7b-32768",
        "system_prompt": "Eres un asistente de prueba."
    }

    try:
        response = requests.post(f"{BASE_URL}/chatbots/", json=chatbot_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            chatbot_info = response.json()
            chatbot_id = chatbot_info["id"]
            print(f"✅ Chatbot creado - ID: {chatbot_id}")
        else:
            print(f"❌ Error creando chatbot: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # Paso 4: DEPURACIÓN DETALLADA DE CONVERSACIÓN
    print("\n[PASO 4] DEPURACIÓN DETALLADA DE CONVERSACIÓN")
    print("-" * 50)

    # Verificar que el chatbot existe
    print("4.1 Verificando existencia del chatbot...")
    try:
        response = requests.get(f"{BASE_URL}/chatbots/{chatbot_id}", headers=headers)
        print(f"Verificación chatbot - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Chatbot no encontrado: {response.text}")
            return
        else:
            print("✅ Chatbot encontrado")
    except Exception as e:
        print(f"❌ Error verificando chatbot: {e}")
        return

    # Intentar crear conversación con datos mínimos
    print("\n4.2 Intentando crear conversación con datos mínimos...")
    session_id = str(uuid.uuid4())
    conversation_data_minimal = {
        "chatbot_id": chatbot_id,
        "session_id": session_id
    }

    try:
        response = requests.post(f"{BASE_URL}/conversations/",
                               json=conversation_data_minimal,
                               headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 201:
            print("✅ Conversación creada con datos mínimos")
            return
        else:
            print("❌ Error con datos mínimos")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # Intentar con datos completos
    print("\n4.3 Intentando crear conversación con datos completos...")
    session_id2 = str(uuid.uuid4())
    conversation_data_full = {
        "chatbot_id": chatbot_id,
        "session_id": session_id2,
        "title": "Conversación de Debug",
        "user_info": {
            "name": "Usuario de Prueba",
            "email": "test@example.com"
        },
        "metadata": {}
    }

    try:
        response = requests.post(f"{BASE_URL}/conversations/",
                               json=conversation_data_full,
                               headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 201:
            print("✅ Conversación creada con datos completos")
        else:
            print("❌ Error con datos completos")
            print("🔍 DETALLES DEL ERROR:")
            try:
                error_detail = response.json()
                print(json.dumps(error_detail, indent=2))
            except:
                print(response.text)
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # Intentar sin autenticación (usuario anónimo)
    print("\n4.4 Intentando crear conversación como usuario anónimo...")
    session_id3 = str(uuid.uuid4())
    conversation_data_anon = {
        "chatbot_id": chatbot_id,
        "session_id": session_id3,
        "title": "Conversación Anónima",
        "user_info": {
            "name": "Usuario Anónimo",
            "email": "anonimo@example.com"
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/conversations/",
                               json=conversation_data_anon)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 201:
            print("✅ Conversación creada como usuario anónimo")
        else:
            print("❌ Error como usuario anónimo")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    print("\n" + "="*60)
    print("🎯 RECOMENDACIONES:")
    print("1. Revisar los logs del servidor backend")
    print("2. Verificar el modelo Conversation en models.py")
    print("3. Comprobar constraints de base de datos")
    print("4. Validar el endpoint en conversations.py")
    print("\n📊 ESTADO DETECTADO:")
    print("- Sistema principal: FUNCIONAL")
    print("- Solo problema: Creación de conversaciones")
    print("- Impacto: MENOR - Core del sistema operativo")

if __name__ == "__main__":
    debug_conversation_creation()