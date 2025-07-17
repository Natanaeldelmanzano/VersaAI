#!/usr/bin/env python3
"""
Script para probar los endpoints de autenticación del backend
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_health_endpoint():
    """Prueba el endpoint de salud"""
    try:
        # Probar primero el endpoint básico de health
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint funcionando")
            return True
        else:
            print(f"❌ Health endpoint falló: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_register_endpoint():
    """Prueba el endpoint de registro"""
    test_user = {
        "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "password": "testpassword123",
        "full_name": "Usuario de Prueba"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=test_user,
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ Registro de usuario exitoso")
            data = response.json()
            return data.get("access_token"), test_user["email"]
        else:
            print(f"❌ Error en registro: {response.status_code} - {response.text}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en registro: {e}")
        return None, None

def test_login_endpoint(email, password):
    """Prueba el endpoint de login"""
    login_data = {
        "username": email,  # FastAPI OAuth2 usa 'username'
        "password": password
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            data=login_data,  # OAuth2 usa form data
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Login exitoso")
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en login: {e}")
        return None

def test_protected_endpoint(token):
    """Prueba un endpoint protegido"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{API_BASE}/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Endpoint protegido funcionando")
            data = response.json()
            print(f"   Usuario: {data.get('email', 'N/A')}")
            return True
        else:
            print(f"❌ Error en endpoint protegido: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en endpoint protegido: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Probando endpoints de autenticación...\n")
    
    # 1. Probar health endpoint
    print("1️⃣ Probando health endpoint...")
    if not test_health_endpoint():
        print("💥 Backend no está funcionando. Asegúrate de que esté ejecutándose.")
        return False
    
    # 2. Probar registro
    print("\n2️⃣ Probando registro de usuario...")
    token, email = test_register_endpoint()
    if not token:
        print("💥 Error en el registro de usuario")
        return False
    
    # 3. Probar login
    print("\n3️⃣ Probando login...")
    login_token = test_login_endpoint(email, "testpassword123")
    if not login_token:
        print("💥 Error en el login")
        return False
    
    # 4. Probar endpoint protegido
    print("\n4️⃣ Probando endpoint protegido...")
    if not test_protected_endpoint(login_token):
        print("💥 Error en endpoint protegido")
        return False
    
    print("\n🎉 ¡Todos los tests de autenticación pasaron!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)