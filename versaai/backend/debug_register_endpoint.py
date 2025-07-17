#!/usr/bin/env python3
"""
Script para depurar específicamente el endpoint de registro
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_register_endpoint_detailed():
    """Prueba detallada del endpoint de registro"""
    
    # Datos de prueba únicos
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_user = {
        "email": f"debug_{timestamp}@test.com",
        "password": "testpassword123",
        "full_name": "Debug User",
        "username": f"debug_{timestamp}"
    }
    
    print(f"🧪 Probando registro con datos:")
    print(f"   Email: {test_user['email']}")
    print(f"   Username: {test_user['username']}")
    print(f"   Full Name: {test_user['full_name']}")
    print()
    
    try:
        print("📡 Enviando request al endpoint...")
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=test_user,
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 201:
            print("✅ Registro exitoso!")
            data = response.json()
            print("📄 Respuesta completa:")
            print(json.dumps(data, indent=2, default=str))
            
            # Verificar campos específicos
            print("\n🔍 Verificación de campos:")
            print(f"   ID: {data.get('id', 'MISSING')}")
            print(f"   Email: {data.get('email', 'MISSING')}")
            print(f"   Username: {data.get('username', 'MISSING')}")
            print(f"   Created At: {data.get('created_at', 'MISSING')}")
            print(f"   Updated At: {data.get('updated_at', 'MISSING')}")
            
            return True
            
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(f"📄 Respuesta de error:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
            
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_health_first():
    """Verificar que el backend esté funcionando"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend funcionando correctamente")
            return True
        else:
            print(f"❌ Backend respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend no responde: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 Debug del Endpoint de Registro")
    print("=" * 50)
    print()
    
    # 1. Verificar backend
    print("1️⃣ Verificando backend...")
    if not test_health_first():
        print("💥 Backend no está funcionando. Saliendo.")
        return False
    print()
    
    # 2. Probar registro
    print("2️⃣ Probando endpoint de registro...")
    success = test_register_endpoint_detailed()
    
    print()
    if success:
        print("🎉 Debug completado exitosamente!")
    else:
        print("💥 Se encontraron errores en el registro")
    
    return success

if __name__ == "__main__":
    main()