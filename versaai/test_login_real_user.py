#!/usr/bin/env python3
"""
Script para probar login con usuarios reales de la base de datos
"""

import requests
import json
from datetime import datetime

def test_login_with_real_users():
    """Prueba el login con usuarios que existen en la base de datos"""
    base_url = "http://localhost:8000"
    
    print("=== PRUEBA DE LOGIN CON USUARIOS REALES ===")
    print(f"Fecha: {datetime.now()}")
    print("\n" + "="*50)
    
    # Lista de usuarios para probar (basado en check_users.py)
    test_users = [
        {
            "email": "test@versaai.com",
            "password": "test123"  # Contraseña común de prueba
        },
        {
            "email": "test1752329958@versaai.com",
            "password": "test123"
        },
        {
            "email": "test_20250712_120310@example.com",
            "password": "test123"
        }
    ]
    
    for i, user_data in enumerate(test_users, 1):
        print(f"\n{i}. Probando login con: {user_data['email']}")
        
        try:
            login_response = requests.post(
                f"{base_url}/api/v1/auth/login",
                json=user_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"   Status Code: {login_response.status_code}")
            
            if login_response.status_code == 200:
                response_data = login_response.json()
                print("   ✅ Login exitoso!")
                print(f"   Access Token: {response_data.get('access_token', 'N/A')[:30]}...")
                print(f"   Token Type: {response_data.get('token_type', 'N/A')}")
                
                # Probar el token con /me
                token = response_data.get('access_token')
                if token:
                    me_response = requests.get(
                        f"{base_url}/api/v1/auth/me",
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=5
                    )
                    if me_response.status_code == 200:
                        user_info = me_response.json()
                        print(f"   Usuario autenticado: {user_info.get('email', 'N/A')}")
                        print(f"   Nombre: {user_info.get('full_name', 'N/A')}")
                        print(f"   Rol: {user_info.get('role', 'N/A')}")
                        
                        # Si encontramos un usuario válido, guardamos las credenciales
                        print("\n🎉 CREDENCIALES VÁLIDAS ENCONTRADAS:")
                        print(f"Email: {user_data['email']}")
                        print(f"Password: {user_data['password']}")
                        return user_data
                    else:
                        print(f"   ❌ Token inválido - Status: {me_response.status_code}")
            elif login_response.status_code == 401:
                print("   ❌ Credenciales inválidas")
                try:
                    error_detail = login_response.json()
                    print(f"   Detalle: {error_detail.get('detail', 'N/A')}")
                except:
                    print(f"   Response: {login_response.text}")
            else:
                print(f"   ❌ Error inesperado - Response: {login_response.text}")
                
        except Exception as e:
            print(f"   ❌ Error en la petición: {e}")
    
    print("\n" + "="*50)
    print("❌ NO SE ENCONTRARON CREDENCIALES VÁLIDAS")
    print("\nPosibles soluciones:")
    print("1. Crear un nuevo usuario de prueba")
    print("2. Verificar las contraseñas en la base de datos")
    print("3. Resetear la contraseña de un usuario existente")
    
    return None

def create_test_user():
    """Crea un usuario de prueba para testing"""
    base_url = "http://localhost:8000"
    
    print("\n=== CREANDO USUARIO DE PRUEBA ===")
    
    user_data = {
        "email": "demo@versaai.com",
        "password": "demo123",
        "full_name": "Usuario Demo",
        "username": "demo"
    }
    
    try:
        register_response = requests.post(
            f"{base_url}/api/v1/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {register_response.status_code}")
        
        if register_response.status_code == 201:
            print("✅ Usuario creado exitosamente!")
            print(f"Email: {user_data['email']}")
            print(f"Password: {user_data['password']}")
            return user_data
        else:
            print(f"❌ Error al crear usuario: {register_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return None

if __name__ == "__main__":
    # Primero intentar con usuarios existentes
    valid_user = test_login_with_real_users()
    
    # Si no funciona, crear un usuario nuevo
    if not valid_user:
        print("\n" + "="*50)
        new_user = create_test_user()
        
        if new_user:
            print("\n=== PROBANDO LOGIN CON USUARIO NUEVO ===")
            try:
                login_response = requests.post(
                    "http://localhost:8000/api/v1/auth/login",
                    json={"email": new_user["email"], "password": new_user["password"]},
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if login_response.status_code == 200:
                    print("✅ Login con usuario nuevo exitoso!")
                    print(f"Usar estas credenciales: {new_user['email']} / {new_user['password']}")
                else:
                    print(f"❌ Login falló: {login_response.text}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")