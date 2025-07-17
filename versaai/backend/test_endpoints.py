#!/usr/bin/env python3
"""
Script para probar los endpoints corregidos
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Prueba el endpoint de salud"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def get_auth_token():
    """Obtiene token de autenticación"""
    try:
        # Datos de prueba para login
        login_data = {
            "email": "admin@versaai.com",
            "password": "admin123"
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data, headers=headers)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Login successful, token obtained")
            return token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_user_profile(token):
    """Prueba el endpoint de perfil de usuario"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User profile: {response.status_code}")
            print(f"   - Email: {user_data.get('email')}")
            print(f"   - Preferences: {user_data.get('preferences')}")
            print(f"   - Login count: {user_data.get('login_count')}")
            return True
        else:
            print(f"❌ User profile failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ User profile error: {e}")
        return False

def test_chatbots(token):
    """Prueba el endpoint de chatbots"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/chatbots", headers=headers)
        
        if response.status_code == 200:
            chatbots_data = response.json()
            print(f"✅ Chatbots endpoint: {response.status_code}")
            print(f"   - Total chatbots: {chatbots_data.get('total', 0)}")
            print(f"   - Page: {chatbots_data.get('page', 1)}")
            print(f"   - Per page: {chatbots_data.get('per_page', 10)}")
            
            chatbots = chatbots_data.get('chatbots', [])
            if chatbots:
                print(f"   - First chatbot: {chatbots[0].get('name', 'N/A')}")
                print(f"   - Has stats: {'total_conversations' in chatbots[0]}")
            
            return True
        else:
            print(f"❌ Chatbots failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chatbots error: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Iniciando pruebas de endpoints...\n")
    
    # Prueba de salud
    if not test_health():
        print("💥 Servidor no disponible")
        return
    
    print()
    
    # Obtener token
    token = get_auth_token()
    if not token:
        print("💥 No se pudo obtener token de autenticación")
        return
    
    print()
    
    # Probar perfil de usuario
    user_success = test_user_profile(token)
    
    print()
    
    # Probar chatbots
    chatbots_success = test_chatbots(token)
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   - Perfil de usuario: {'✅ CORREGIDO' if user_success else '❌ FALLA'}")
    print(f"   - Endpoint chatbots: {'✅ CORREGIDO' if chatbots_success else '❌ FALLA'}")
    
    if user_success and chatbots_success:
        print("\n🎉 ¡Todas las correcciones funcionan correctamente!")
    else:
        print("\n⚠️ Algunas correcciones necesitan más trabajo")

if __name__ == "__main__":
    main()