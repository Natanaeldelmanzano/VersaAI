import requests
import json
import traceback
import time

def test_chatbot_creation():
    print("🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA VERSAAI")
    print("=" * 60)

    base_url = "http://localhost:8000/api/v1"

    try:
        # 1. Login
        print("\n🔐 Paso 1: Autenticación...")
        login_data = {
            "email": "testuser@versaai.com",
            "password": "testpassword123"
        }

        login_response = requests.post(f"{base_url}/auth/login", json=login_data, headers={"Content-Type": "application/json"})
        print(f"   Status: {login_response.status_code}")

        if login_response.status_code != 200:
            print(f"   ❌ Error en login: {login_response.text}")
            return

        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("   ✅ Login exitoso")

        # 2. Verificar usuario actual
        print("\n👤 Paso 2: Verificando usuario actual...")
        user_response = requests.get(f"{base_url}/auth/me", headers=headers)
        print(f"   Status: {user_response.status_code}")

        if user_response.status_code == 200:
            user_data = user_response.json()
            print(f"   ✅ Usuario: {user_data.get('email')} (ID: {user_data.get('id')})")
            print(f"   📍 Organización ID: {user_data.get('organization_id')}")
        else:
            print(f"   ❌ Error obteniendo usuario: {user_response.text}")

        # 3. Probar GET chatbots
        print("\n📋 Paso 3: Listando chatbots existentes...")
        get_response = requests.get(f"{base_url}/chatbots/", headers=headers)
        print(f"   Status: {get_response.status_code}")

        if get_response.status_code == 200:
            chatbots = get_response.json()
            print(f"   ✅ Chatbots encontrados: {len(chatbots)}")
        else:
            print(f"   ❌ Error listando chatbots: {get_response.text}")

        # 4. Intentar crear chatbot con datos mínimos
        print("\n🆕 Paso 4: Creando chatbot con datos mínimos...")
        timestamp = int(time.time())
        minimal_chatbot = {
            "name": f"Test Bot Minimal {timestamp}",
            "description": "Bot de prueba mínimo"
        }

        create_response = requests.post(f"{base_url}/chatbots/", headers=headers, json=minimal_chatbot)
        print(f"   Status: {create_response.status_code}")
        print(f"   Response: {create_response.text}")

        # 5. Intentar crear chatbot con todos los campos
        print("\n🆕 Paso 5: Creando chatbot con todos los campos...")
        complete_chatbot = {
            "name": f"Test Bot Complete {timestamp}",
            "description": "Bot de prueba completo",
            "system_prompt": "Eres un asistente útil",
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
            "is_active": True,
            "is_public": False,
            "welcome_message": "¡Hola! ¿En qué puedo ayudarte?",
            "primary_color": "#3B82F6",
            "secondary_color": "#1F2937"
        }

        create_response2 = requests.post(f"{base_url}/chatbots/", headers=headers, json=complete_chatbot)
        print(f"   Status: {create_response2.status_code}")
        print(f"   Response: {create_response2.text}")

        # 6. Verificar estructura de respuesta de error
        if create_response2.status_code != 201:
            print("\n🔍 Paso 6: Analizando error detallado...")
            try:
                error_data = create_response2.json()
                print(f"   Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error texto: {create_response2.text}")

    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("🏁 DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    test_chatbot_creation()