#!/usr/bin/env python3
"""
Script para probar la autenticación del backend
"""

import requests
import json
import sys

# Configuración
BASE_URL = "http://localhost:8000/api/v1"

def test_auth():
    print("🔐 Probando autenticación del backend...")
    
    # Datos de prueba
    test_user = {
        "email": "test@versaai.com",
        "password": "test123456",
        "full_name": "Usuario de Prueba"
    }
    
    # 1. Intentar registrar usuario
    print("\n1. Intentando registrar usuario...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print("✅ Usuario registrado exitosamente")
            print(f"📄 Respuesta: {response.json()}")
        elif response.status_code == 400 and "already registered" in response.text:
            print("ℹ️ Usuario ya existe, continuando con login...")
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión en registro: {e}")
        return False
    
    # 2. Intentar login
    print("\n2. Intentando login...")
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
            print("✅ Login exitoso")
            token_data = response.json()
            print(f"🔑 Token obtenido: {token_data['access_token'][:50]}...")
            
            # 3. Probar endpoint protegido
            print("\n3. Probando endpoint protegido (/auth/me)...")
            headers = {
                "Authorization": f"Bearer {token_data['access_token']}",
                "Content-Type": "application/json"
            }
            
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            
            if me_response.status_code == 200:
                print("✅ Endpoint protegido funciona correctamente")
                user_info = me_response.json()
                print(f"👤 Usuario: {user_info.get('email', 'N/A')}")
                print(f"📧 Email: {user_info.get('email', 'N/A')}")
                return True
            else:
                print(f"❌ Error en endpoint protegido: {me_response.status_code}")
                print(f"📄 Respuesta: {me_response.text}")
                return False
                
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión en login: {e}")
        return False

if __name__ == "__main__":
    print("🚀 VersaAI - Test de Autenticación")
    print("=" * 50)
    
    success = test_auth()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡Autenticación funcionando correctamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Usar este token en el frontend")
        print("   2. Probar el chat con autenticación")
        print("   3. Verificar persistencia de conversaciones")
    else:
        print("❌ Problemas con la autenticación")
        print("\n🔧 Revisar:")
        print("   1. Backend ejecutándose en puerto 8000")
        print("   2. Base de datos PostgreSQL")
        print("   3. Configuración de autenticación")
    
    sys.exit(0 if success else 1)