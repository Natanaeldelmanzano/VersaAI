#!/usr/bin/env python3
"""
Script de prueba para verificar la integración del frontend con el servidor temporal
"""

import requests
import json
from datetime import datetime

# Configuración del servidor temporal
BASE_URL = "http://localhost:8001"

def test_health():
    """Prueba el endpoint de health"""
    print("\n=== Probando Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Prueba el endpoint de login"""
    print("\n=== Probando Login ===")
    try:
        data = {
            "email": "test@example.com",
            "password": "test123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Access Token: {result.get('access_token', 'N/A')[:50]}...")
        print(f"Refresh Token: {result.get('refresh_token', 'N/A')[:50]}...")
        print(f"Token Type: {result.get('token_type', 'N/A')}")
        return response.status_code == 200, result
    except Exception as e:
        print(f"Error: {e}")
        return False, None

def test_refresh(refresh_token):
    """Prueba el endpoint de refresh"""
    print("\n=== Probando Refresh Token ===")
    try:
        data = {
            "refresh_token": refresh_token
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/refresh", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"New Access Token: {result.get('access_token', 'N/A')[:50]}...")
        print(f"New Refresh Token: {result.get('refresh_token', 'N/A')[:50]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_verify_token(access_token):
    """Prueba el endpoint de verificación de token"""
    print("\n=== Probando Verify Token ===")
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/verify-token", headers=headers)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Valid: {result.get('valid', 'N/A')}")
        print(f"User: {result.get('user', 'N/A')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_simple_endpoint():
    """Prueba el endpoint simple"""
    print("\n=== Probando Test Simple ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/test-simple")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de integración del servidor temporal")
    print(f"Servidor: {BASE_URL}")
    print(f"Timestamp: {datetime.now()}")
    
    # Prueba 1: Health Check
    health_ok = test_health()
    
    if not health_ok:
        print("❌ El servidor no está disponible. Verifica que esté ejecutándose.")
        return
    
    # Prueba 2: Login
    login_ok, login_result = test_login()
    
    if not login_ok:
        print("❌ Error en el login")
        return
    
    # Prueba 3: Refresh Token
    refresh_token = login_result.get('refresh_token')
    refresh_ok = test_refresh(refresh_token)
    
    # Prueba 4: Verify Token
    access_token = login_result.get('access_token')
    verify_ok = test_verify_token(access_token)
    
    # Prueba 5: Endpoint Simple
    simple_ok = test_simple_endpoint()
    
    # Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Health Check: {'OK' if health_ok else 'FAIL'}")
    print(f"✅ Login: {'OK' if login_ok else 'FAIL'}")
    print(f"✅ Refresh Token: {'OK' if refresh_ok else 'FAIL'}")
    print(f"✅ Verify Token: {'OK' if verify_ok else 'FAIL'}")
    print(f"✅ Test Simple: {'OK' if simple_ok else 'FAIL'}")
    
    all_ok = all([health_ok, login_ok, refresh_ok, verify_ok, simple_ok])
    
    if all_ok:
        print("\n🎉 ¡Todas las pruebas pasaron! El servidor temporal está listo para el frontend.")
        print("\n📝 Configuración para el frontend:")
        print(f"   - URL Base: {BASE_URL}")
        print(f"   - Endpoints disponibles:")
        print(f"     * GET  /health")
        print(f"     * POST /api/v1/auth/login")
        print(f"     * POST /api/v1/auth/refresh")
        print(f"     * POST /api/v1/auth/verify-token")
        print(f"     * GET  /api/v1/auth/test-simple")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los logs del servidor.")

if __name__ == "__main__":
    main()