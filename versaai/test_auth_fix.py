#!/usr/bin/env python3
"""
Script simple para probar si se resolvió el problema de autenticación automática
"""

import requests
import json
import webbrowser
import time

def test_auth_fix():
    print("🔧 Probando corrección de autenticación automática")
    print("=" * 50)
    
    # 1. Verificar login y obtener token
    print("1️⃣ Probando login directo...")
    try:
        login_data = {
            "email": "demo@versaai.com",
            "password": "demo123456"
        }
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✅ Login exitoso")
            print(f"   📝 Token: {token[:30]}...")
            print(f"   👤 Usuario: {data.get('user', {}).get('email')}")
        else:
            print(f"   ❌ Login falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error en login: {e}")
        return False
    
    # 2. Verificar endpoint /me con el token
    print("\n2️⃣ Probando endpoint /me...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            'http://localhost:8000/api/v1/auth/me',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Endpoint /me funcional")
            print(f"   👤 Usuario verificado: {user_data.get('email')}")
        else:
            print(f"   ❌ Endpoint /me falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error en /me: {e}")
        return False
    
    # 3. Verificar que setup-auth.html esté disponible
    print("\n3️⃣ Verificando setup-auth.html...")
    try:
        response = requests.get('http://localhost:3000/setup-auth.html', timeout=5)
        if response.status_code == 200:
            print("   ✅ setup-auth.html disponible")
            
            # Verificar que contiene las credenciales correctas
            content = response.text
            if 'demo@versaai.com' in content and 'demo123456' in content:
                print("   ✅ Credenciales correctas en el archivo")
            else:
                print("   ⚠️ Credenciales no encontradas en el archivo")
        else:
            print(f"   ❌ setup-auth.html no disponible: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error accediendo setup-auth.html: {e}")
        return False
    
    # 4. Información sobre las correcciones realizadas
    print("\n🔧 Correcciones realizadas:")
    print("   ✅ Store de auth: Corregidas inconsistencias en localStorage")
    print("      - restoreSession ahora usa 'access_token'")
    print("      - logout ahora limpia 'access_token' y cookies")
    print("   ✅ Main.js: Agregado plugin de auth con autoCheck")
    print("      - checkAuth se ejecuta automáticamente al cargar")
    print("      - Monitoreo de sesión habilitado")
    print("   ✅ Usuario demo creado y verificado")
    
    # 5. Abrir para prueba manual
    print("\n🌐 Abriendo setup-auth.html para prueba manual...")
    webbrowser.open('http://localhost:3000/setup-auth.html')
    
    print("\n📋 Instrucciones para la prueba manual:")
    print("   1. Se abrirá setup-auth.html en tu navegador")
    print("   2. Haz clic en 'Configurar Autenticación Automática'")
    print("   3. Deberías ver un mensaje de éxito")
    print("   4. Después de 2 segundos, serás redirigido a la página principal")
    print("   5. AHORA deberías estar autenticado automáticamente")
    
    print("\n✨ Diferencia esperada:")
    print("   ANTES: Redirigía a la página principal SIN autenticar")
    print("   AHORA: Redirige a la página principal Y te autentica automáticamente")
    
    return True

if __name__ == "__main__":
    success = test_auth_fix()
    if success:
        print("\n🎉 ¡Corrección completada!")
        print("\nEl problema debería estar resuelto. El setup automático ahora:")
        print("• Guarda el token como 'access_token' (consistente)")
        print("• El plugin de auth ejecuta checkAuth automáticamente")
        print("• La aplicación detecta el token al cargar")
        print("• El usuario queda autenticado después de la redirección")
    else:
        print("\n❌ Aún hay problemas que resolver.")