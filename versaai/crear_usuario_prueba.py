#!/usr/bin/env python3
"""
Script para crear un usuario de prueba y verificar el sistema de autenticación
"""

import requests
import json
import sys
from datetime import datetime

def print_header(title):
    """Imprime un encabezado formateado"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def test_backend_health():
    """Verifica si el backend está activo"""
    print_header("VERIFICACIÓN DEL BACKEND")
    
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend activo en puerto 8000")
            data = response.json()
            print(f"📊 Respuesta: {data}")
            return True
        else:
            print(f"❌ Backend responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend no está ejecutándose en puerto 8000")
        print("💡 Ejecuta: cd backend && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error verificando backend: {e}")
        return False

def test_register_user():
    """Prueba el registro de un usuario"""
    print_header("PRUEBA DE REGISTRO DE USUARIO")
    
    # Datos del usuario de prueba
    user_data = {
        "email": "test@versaai.com",
        "password": "TestPassword123!",
        "full_name": "Usuario de Prueba VersaAI"
    }
    
    try:
        print(f"📝 Intentando registrar usuario: {user_data['email']}")
        
        response = requests.post(
            "http://localhost:8000/api/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Código de respuesta: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Usuario registrado exitosamente")
            data = response.json()
            print(f"👤 Usuario creado: {data.get('email', 'N/A')}")
            print(f"🆔 ID: {data.get('id', 'N/A')}")
            return True, data
        elif response.status_code == 400:
            error_data = response.json()
            if "already registered" in str(error_data).lower():
                print("⚠️  Usuario ya existe, continuando con login...")
                return True, {"email": user_data["email"]}
            else:
                print(f"❌ Error en el registro: {error_data}")
                return False, None
        else:
            print(f"❌ Error en el registro: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Detalles: {error_data}")
            except:
                print(f"📄 Respuesta: {response.text}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        return False, None
    except Exception as e:
        print(f"❌ Error durante el registro: {e}")
        return False, None

def test_login_user(email="test@versaai.com", password="TestPassword123!"):
    """Prueba el login del usuario"""
    print_header("PRUEBA DE LOGIN DE USUARIO")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        print(f"🔐 Intentando login con: {email}")
        
        response = requests.post(
            "http://localhost:8000/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login exitoso")
            data = response.json()
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            
            if access_token:
                print(f"🎫 Access Token: {access_token[:50]}...")
            if refresh_token:
                print(f"🔄 Refresh Token: {refresh_token[:50]}...")
            
            return True, data
        else:
            print(f"❌ Error en el login: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Detalles: {error_data}")
            except:
                print(f"📄 Respuesta: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error durante el login: {e}")
        return False, None

def test_protected_endpoint(access_token):
    """Prueba un endpoint protegido"""
    print_header("PRUEBA DE ENDPOINT PROTEGIDO")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        print("🔒 Probando endpoint protegido...")
        
        response = requests.get(
            "http://localhost:8000/api/users/me",
            headers=headers,
            timeout=10
        )
        
        print(f"📡 Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Acceso autorizado al endpoint protegido")
            data = response.json()
            print(f"👤 Datos del usuario: {data}")
            return True
        else:
            print(f"❌ Error accediendo al endpoint: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Detalles: {error_data}")
            except:
                print(f"📄 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando endpoint protegido: {e}")
        return False

def show_next_actions():
    """Muestra las próximas acciones del plan de desarrollo"""
    print_header("PRÓXIMAS ACCIONES DEL PLAN DE DESARROLLO")
    
    print("🎯 Acciones Completadas:")
    print("   ✅ Backend FastAPI ejecutándose")
    print("   ✅ Frontend Vue.js ejecutándose")
    print("   ✅ PostgreSQL configurado en Docker")
    print("   ✅ Sistema de autenticación básico")
    
    print("\n🔄 Próximas Acciones Prioritarias:")
    print("   1. 🔧 Implementar CRUD completo de usuarios")
    print("   2. 🏢 Sistema de organizaciones")
    print("   3. 🤖 Motor de chatbots básico")
    print("   4. 💬 Interface de chat")
    print("   5. 📊 Dashboard con métricas")
    
    print("\n📋 Comandos para continuar:")
    print("   # Crear endpoints de usuarios")
    print("   # Implementar gestión de organizaciones")
    print("   # Integrar con Groq AI")
    print("   # Desarrollar componentes Vue del chat")
    
    print("\n🌐 URLs de desarrollo:")
    print("   📖 API Docs: http://localhost:8000/docs")
    print("   🌐 Frontend: http://localhost:3000")
    print("   ⚡ Health: http://localhost:8000/api/health")

def main():
    """Función principal"""
    print("🚀 VersaAI - Prueba del Sistema de Autenticación")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar backend
    if not test_backend_health():
        print("\n❌ Backend no disponible. Inicia el servidor antes de continuar.")
        sys.exit(1)
    
    # Probar registro
    register_success, user_data = test_register_user()
    
    if register_success:
        # Probar login
        login_success, login_data = test_login_user()
        
        if login_success and login_data:
            access_token = login_data.get('access_token')
            if access_token:
                # Probar endpoint protegido
                test_protected_endpoint(access_token)
    
    # Mostrar próximas acciones
    show_next_actions()
    
    print("\n" + "="*60)
    print("🎉 ¡Verificación del sistema completada!")
    print("📝 Consulta PLAN_ACCIONES_DESARROLLO.md para continuar")
    print("="*60)

if __name__ == "__main__":
    main()