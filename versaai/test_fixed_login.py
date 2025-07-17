#!/usr/bin/env python3
"""
Prueba del Login Corregido - VersaAI
Verifica que el login funcione con la nueva estructura de respuesta
"""

import requests
import json
from datetime import datetime

def test_fixed_login():
    """Test the fixed login functionality"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 PROBANDO LOGIN CORREGIDO - VERSAAI")
    print("=" * 50)
    
    # Create a unique test user
    timestamp = int(datetime.now().timestamp())
    test_email = f"testfixed_{timestamp}@versaai.com"
    test_password = "testpass123"
    test_name = "Usuario Prueba Corregido"
    
    print(f"📧 Email de prueba: {test_email}")
    print(f"🔑 Contraseña: {test_password}")
    
    # Step 1: Register user
    print("\n1️⃣ REGISTRANDO USUARIO...")
    register_data = {
        "email": test_email,
        "password": test_password,
        "full_name": test_name
    }
    
    try:
        register_response = requests.post(f"{base_url}/auth/register", json=register_data, timeout=10)
        
        if register_response.status_code == 201:
            print("✅ Usuario registrado exitosamente")
            register_data_response = register_response.json()
            print(f"   ID: {register_data_response.get('id')}")
            print(f"   Email: {register_data_response.get('email')}")
            print(f"   Nombre: {register_data_response.get('full_name')}")
        else:
            print(f"❌ Error al registrar usuario: {register_response.status_code}")
            print(f"   Respuesta: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión al registrar: {e}")
        return False
    
    # Step 2: Test login with new response structure
    print("\n2️⃣ PROBANDO LOGIN CON NUEVA ESTRUCTURA...")
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=10)
        
        if login_response.status_code == 200:
            print("✅ Login exitoso")
            login_response_data = login_response.json()
            
            # Check response structure
            print("\n📋 ESTRUCTURA DE RESPUESTA:")
            print(f"   Campos disponibles: {list(login_response_data.keys())}")
            
            # Verify required fields
            required_fields = ['access_token', 'refresh_token', 'token_type', 'user']
            missing_fields = [field for field in required_fields if field not in login_response_data]
            
            if not missing_fields:
                print("✅ Todos los campos requeridos están presentes")
                
                # Check user data structure
                user_data = login_response_data.get('user', {})
                print(f"\n👤 DATOS DEL USUARIO:")
                print(f"   ID: {user_data.get('id')}")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Nombre completo: {user_data.get('full_name')}")
                print(f"   Rol: {user_data.get('role')}")
                print(f"   Activo: {user_data.get('is_active')}")
                print(f"   Verificado: {user_data.get('is_verified')}")
                
                # Check tokens
                access_token = login_response_data.get('access_token')
                refresh_token = login_response_data.get('refresh_token')
                token_type = login_response_data.get('token_type')
                
                print(f"\n🔐 TOKENS:")
                print(f"   Tipo de token: {token_type}")
                print(f"   Access token: {access_token[:20]}...{access_token[-10:] if access_token else 'None'}")
                print(f"   Refresh token: {refresh_token[:20]}...{refresh_token[-10:] if refresh_token else 'None'}")
                
            else:
                print(f"❌ Campos faltantes: {missing_fields}")
                return False
                
        else:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"   Respuesta: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión en login: {e}")
        return False
    
    # Step 3: Test /me endpoint with token
    print("\n3️⃣ VERIFICANDO ENDPOINT /ME...")
    
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        me_response = requests.get(f"{base_url}/auth/me", headers=headers, timeout=10)
        
        if me_response.status_code == 200:
            print("✅ Endpoint /me funciona correctamente")
            me_data = me_response.json()
            print(f"   Usuario autenticado: {me_data.get('email')}")
            print(f"   Nombre: {me_data.get('full_name')}")
            
            # Verify data consistency
            if me_data.get('email') == test_email and me_data.get('full_name') == test_name:
                print("✅ Datos consistentes entre login y /me")
            else:
                print("⚠️ Inconsistencia en datos entre login y /me")
                
        else:
            print(f"❌ Error en /me: {me_response.status_code}")
            print(f"   Respuesta: {me_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión en /me: {e}")
        return False
    
    # Step 4: Frontend compatibility test
    print("\n4️⃣ VERIFICANDO COMPATIBILIDAD CON FRONTEND...")
    
    # Simulate frontend login process
    frontend_expected_fields = ['access_token', 'refresh_token', 'user']
    frontend_user_fields = ['id', 'email', 'full_name', 'role']
    
    frontend_compatible = True
    
    # Check main response fields
    for field in frontend_expected_fields:
        if field not in login_response_data:
            print(f"❌ Campo faltante para frontend: {field}")
            frontend_compatible = False
    
    # Check user fields
    user_data = login_response_data.get('user', {})
    for field in frontend_user_fields:
        if field not in user_data:
            print(f"❌ Campo de usuario faltante: {field}")
            frontend_compatible = False
    
    if frontend_compatible:
        print("✅ Respuesta completamente compatible con frontend")
        print("✅ El frontend podrá procesar correctamente el login")
    else:
        print("❌ Problemas de compatibilidad con frontend detectados")
        return False
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎉 RESUMEN FINAL")
    print("=" * 50)
    print("✅ Usuario creado exitosamente")
    print("✅ Login funciona con nueva estructura")
    print("✅ Tokens generados correctamente")
    print("✅ Endpoint /me funciona")
    print("✅ Compatible con frontend")
    print("\n🚀 EL SISTEMA DE LOGIN ESTÁ COMPLETAMENTE FUNCIONAL")
    
    print("\n📝 CREDENCIALES PARA PRUEBA EN FRONTEND:")
    print(f"   Email: {test_email}")
    print(f"   Contraseña: {test_password}")
    print("\n💡 Ahora puedes usar estas credenciales en el frontend para probar el login")
    
    return True

if __name__ == "__main__":
    success = test_fixed_login()
    if success:
        print("\n🎯 PRUEBA COMPLETADA EXITOSAMENTE")
    else:
        print("\n💥 PRUEBA FALLÓ - REVISAR ERRORES ARRIBA")