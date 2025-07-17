#!/usr/bin/env python3
"""
Script para probar el setup automático de autenticación
"""

import requests
import json
import webbrowser
import time
from datetime import datetime

def test_setup_auth_flow():
    """Prueba completa del flujo de setup automático"""
    print("🧪 PROBANDO SETUP AUTOMÁTICO DE AUTENTICACIÓN")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    base_url = "http://localhost:8000"
    frontend_url = "http://localhost:3000"
    
    # 1. Verificar que el backend esté activo
    print("\n1️⃣ Verificando backend...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend activo")
        else:
            print(f"❌ Backend responde con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend no disponible: {e}")
        return False
    
    # 2. Verificar que el frontend esté activo
    print("\n2️⃣ Verificando frontend...")
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend activo")
        else:
            print(f"❌ Frontend responde con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend no disponible: {e}")
        return False
    
    # 3. Verificar que el archivo setup-auth.html esté disponible
    print("\n3️⃣ Verificando setup-auth.html...")
    setup_url = f"{frontend_url}/setup-auth.html"
    try:
        response = requests.get(setup_url, timeout=5)
        if response.status_code == 200:
            print("✅ setup-auth.html disponible")
            print(f"   URL: {setup_url}")
        else:
            print(f"❌ setup-auth.html no disponible (código: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error accediendo a setup-auth.html: {e}")
        return False
    
    # 4. Probar el endpoint de login directamente
    print("\n4️⃣ Probando endpoint de login...")
    login_data = {
        "email": "demo@versaai.com",
        "password": "demo123456"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login exitoso")
            print(f"   Token generado: {data['access_token'][:50]}...")
            print(f"   Usuario: {data['user']['email']}")
            
            # 5. Probar endpoint /me
            print("\n5️⃣ Probando endpoint /me...")
            me_response = requests.get(
                f"{base_url}/api/v1/auth/me",
                headers={"Authorization": f"Bearer {data['access_token']}"},
                timeout=5
            )
            
            if me_response.status_code == 200:
                user_data = me_response.json()
                print("✅ Endpoint /me funciona")
                print(f"   Usuario: {user_data['email']}")
                print(f"   Nombre: {user_data['full_name']}")
            else:
                print(f"❌ Endpoint /me falló: {me_response.status_code}")
                return False
                
        else:
            print(f"❌ Login falló: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False
    
    # 6. Abrir setup-auth.html en el navegador
    print("\n6️⃣ Abriendo setup-auth.html en el navegador...")
    try:
        webbrowser.open(setup_url)
        print("✅ Navegador abierto")
        print(f"   URL: {setup_url}")
    except Exception as e:
        print(f"⚠️ No se pudo abrir el navegador: {e}")
        print(f"   Abre manualmente: {setup_url}")
    
    print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("\n📋 INSTRUCCIONES:")
    print("1. Se ha abierto setup-auth.html en tu navegador")
    print("2. Haz clic en 'Configurar Autenticación Automática'")
    print("3. Deberías ver el mensaje de éxito")
    print("4. Serás redirigido automáticamente a la aplicación")
    
    return True

if __name__ == "__main__":
    success = test_setup_auth_flow()
    if success:
        print("\n✅ Setup automático listo para usar")
    else:
        print("\n❌ Hay problemas que resolver antes de usar el setup automático")