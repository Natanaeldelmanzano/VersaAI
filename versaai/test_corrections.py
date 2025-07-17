#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones en VersaAI
"""

import requests
import json
import uuid
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
        return None
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_chatbots_fixed(token):
    """Probar endpoint de chatbots corregido"""
    print("\n🤖 PROBANDO ENDPOINT DE CHATBOTS CORREGIDO...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/chatbots/", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chatbots endpoint funcional")
            print(f"Total chatbots: {data.get('total', 0)}")
            print(f"Página: {data.get('page', 1)} de {data.get('pages', 1)}")
            return True, data.get('chatbots', [])
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False, []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def test_chat_fixed(token, chatbots):
    """Probar chat con chatbot_id correcto"""
    print("\n💬 PROBANDO CHAT CORREGIDO...")
    
    if not chatbots:
        print("❌ No hay chatbots disponibles para probar")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    chatbot_id = chatbots[0].get('id', 1)
    session_id = str(uuid.uuid4())
    
    chat_data = {
        "message": "Hola, esta es una prueba del chat corregido",
        "chatbot_id": chatbot_id,
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/conversations/chat",
            headers=headers,
            json=chat_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat funcional")
            print(f"Respuesta: {data.get('message', '')[:100]}...")
            print(f"Conversation ID: {data.get('conversation_id')}")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 PROBANDO CORRECCIONES VERSAAI")
    print("=" * 50)
    
    # Obtener token
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    print(f"✅ Token obtenido")
    
    # Probar chatbots
    chatbots_ok, chatbots = test_chatbots_fixed(token)
    
    # Probar chat
    chat_ok = test_chat_fixed(token, chatbots)
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"✅ Chatbots: {'FUNCIONAL' if chatbots_ok else 'ERROR'}")
    print(f"✅ Chat: {'FUNCIONAL' if chat_ok else 'ERROR'}")
    
    if chatbots_ok and chat_ok:
        print("\n🎉 ¡TODAS LAS CORRECCIONES FUNCIONAN!")
    else:
        print("\n⚠️ Algunas correcciones necesitan más trabajo")

if __name__ == "__main__":
    main()
