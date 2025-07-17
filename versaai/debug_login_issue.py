#!/usr/bin/env python3
"""
Script para diagnosticar problemas de login en VersaAI
"""

import requests
import json
from datetime import datetime

def test_login_endpoint():
    """Prueba el endpoint de login con diferentes escenarios"""
    base_url = "http://localhost:8000"
    
    print("=== DIAGNÓSTICO DE LOGIN - VersaAI ===")
    print(f"Fecha: {datetime.now()}")
    print(f"URL Base: {base_url}")
    print("\n" + "="*50)
    
    # 1. Verificar que el servidor esté activo
    print("\n1. Verificando servidor...")
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Servidor activo - Status: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión al servidor: {e}")
        return
    
    # 2. Verificar documentación de la API
    print("\n2. Verificando documentación API...")
    try:
        docs_response = requests.get(f"{base_url}/api/docs", timeout=5)
        print(f"✅ Documentación disponible - Status: {docs_response.status_code}")
    except Exception as e:
        print(f"⚠️ Documentación no accesible: {e}")
    
    # 3. Probar endpoint de login con usuario de prueba
    print("\n3. Probando login con usuario de prueba...")
    login_data = {
        "email": "test_20250716_031352@versaai.com",
        "password": "test123"
    }
    
    try:
        login_response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {login_response.status_code}")
        print(f"Headers: {dict(login_response.headers)}")
        
        if login_response.status_code == 200:
            response_data = login_response.json()
            print("✅ Login exitoso!")
            print(f"Access Token: {response_data.get('access_token', 'N/A')[:50]}...")
            print(f"Token Type: {response_data.get('token_type', 'N/A')}")
            print(f"User Data: {response_data.get('user', 'N/A')}")
            
            # 4. Probar endpoint /me con el token
            print("\n4. Verificando token con endpoint /me...")
            token = response_data.get('access_token')
            if token:
                me_response = requests.get(
                    f"{base_url}/api/v1/auth/me",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5
                )
                print(f"Status /me: {me_response.status_code}")
                if me_response.status_code == 200:
                    print(f"✅ Token válido - Usuario: {me_response.json()}")
                else:
                    print(f"❌ Token inválido - Response: {me_response.text}")
        else:
            print(f"❌ Login falló - Status: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout en la petición de login")
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión en login")
    except Exception as e:
        print(f"❌ Error inesperado en login: {e}")
    
    # 5. Probar con credenciales incorrectas
    print("\n5. Probando con credenciales incorrectas...")
    wrong_data = {
        "email": "wrong@email.com",
        "password": "wrongpassword"
    }
    
    try:
        wrong_response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=wrong_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"Status con credenciales incorrectas: {wrong_response.status_code}")
        if wrong_response.status_code == 401:
            print("✅ Validación de credenciales funcionando correctamente")
        else:
            print(f"⚠️ Respuesta inesperada: {wrong_response.text}")
    except Exception as e:
        print(f"❌ Error probando credenciales incorrectas: {e}")
    
    # 6. Verificar usuarios existentes
    print("\n6. Verificando usuarios en la base de datos...")
    try:
        # Intentar obtener información de usuarios (si hay endpoint disponible)
        users_response = requests.get(f"{base_url}/api/v1/users", timeout=5)
        print(f"Status usuarios: {users_response.status_code}")
    except Exception as e:
        print(f"⚠️ No se pudo verificar usuarios: {e}")
    
    print("\n" + "="*50)
    print("DIAGNÓSTICO COMPLETADO")
    print("\nSi el login falla, verifica:")
    print("1. Que el usuario existe en la base de datos")
    print("2. Que la contraseña sea correcta")
    print("3. Que el endpoint /api/v1/auth/login esté funcionando")
    print("4. Los logs del servidor backend para más detalles")

if __name__ == "__main__":
    test_login_endpoint()