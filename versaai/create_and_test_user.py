#!/usr/bin/env python3
"""
Script para crear un usuario único y probar el login
"""

import requests
import json
from datetime import datetime
import time

def create_unique_user_and_test():
    """Crea un usuario único y prueba el login"""
    base_url = "http://localhost:8000"
    
    # Crear email único con timestamp
    timestamp = str(int(time.time()))
    unique_email = f"testuser_{timestamp}@versaai.com"
    password = "testpass123"
    
    print("=== CREANDO USUARIO ÚNICO Y PROBANDO LOGIN ===")
    print(f"Fecha: {datetime.now()}")
    print(f"Email único: {unique_email}")
    print("\n" + "="*50)
    
    # 1. Crear usuario
    print("\n1. Creando usuario...")
    user_data = {
        "email": unique_email,
        "password": password,
        "full_name": "Usuario de Prueba",
        "username": f"testuser_{timestamp}"
    }
    
    try:
        register_response = requests.post(
            f"{base_url}/api/v1/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status Code: {register_response.status_code}")
        
        if register_response.status_code == 201:
            print("   ✅ Usuario creado exitosamente!")
            response_data = register_response.json()
            print(f"   Usuario ID: {response_data.get('id', 'N/A')}")
            print(f"   Email: {response_data.get('email', 'N/A')}")
            print(f"   Nombre: {response_data.get('full_name', 'N/A')}")
        else:
            print(f"   ❌ Error al crear usuario: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en la petición de registro: {e}")
        return False
    
    # 2. Probar login inmediatamente
    print("\n2. Probando login con el usuario recién creado...")
    
    login_data = {
        "email": unique_email,
        "password": password
    }
    
    try:
        login_response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status Code: {login_response.status_code}")
        
        if login_response.status_code == 200:
            response_data = login_response.json()
            print("   ✅ Login exitoso!")
            print(f"   Access Token: {response_data.get('access_token', 'N/A')[:30]}...")
            print(f"   Token Type: {response_data.get('token_type', 'N/A')}")
            
            # 3. Verificar token con /me
            print("\n3. Verificando token con endpoint /me...")
            token = response_data.get('access_token')
            if token:
                me_response = requests.get(
                    f"{base_url}/api/v1/auth/me",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5
                )
                
                print(f"   Status /me: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    user_info = me_response.json()
                    print("   ✅ Token válido!")
                    print(f"   Usuario autenticado: {user_info.get('email', 'N/A')}")
                    print(f"   Nombre: {user_info.get('full_name', 'N/A')}")
                    print(f"   Rol: {user_info.get('role', 'N/A')}")
                    print(f"   ID: {user_info.get('id', 'N/A')}")
                    
                    print("\n" + "="*50)
                    print("🎉 SISTEMA DE LOGIN FUNCIONANDO CORRECTAMENTE")
                    print("\n📋 CREDENCIALES PARA USAR EN EL FRONTEND:")
                    print(f"Email: {unique_email}")
                    print(f"Password: {password}")
                    print("\n✅ Puedes usar estas credenciales para probar el login en la interfaz web")
                    return True
                else:
                    print(f"   ❌ Token inválido - Response: {me_response.text}")
                    return False
        else:
            print(f"   ❌ Login falló - Response: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en la petición de login: {e}")
        return False
    
    return False

if __name__ == "__main__":
    success = create_unique_user_and_test()
    
    if not success:
        print("\n" + "="*50)
        print("❌ HUBO PROBLEMAS CON EL SISTEMA DE AUTENTICACIÓN")
        print("\nVerifica:")
        print("1. Que el servidor backend esté funcionando")
        print("2. Que la base de datos esté conectada")
        print("3. Los logs del servidor para más detalles")
    else:
        print("\n" + "="*50)
        print("✅ DIAGNÓSTICO COMPLETADO - SISTEMA FUNCIONANDO")