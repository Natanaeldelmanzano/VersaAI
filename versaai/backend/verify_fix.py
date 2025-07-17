#!/usr/bin/env python3
"""
Script de verificación final para confirmar que el problema del updated_at se ha resuelto
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from src.main import app
from src.core.database import get_db
from src.models.user import User
from src.schemas.user import UserRegistrationResponse
from datetime import datetime
import json

def test_updated_at_fix():
    """
    Verifica que el problema del updated_at siendo None se ha resuelto
    """
    print("🔍 Verificando la corrección del problema updated_at...")
    
    client = TestClient(app)
    
    # Datos de prueba con timestamp para evitar conflictos
    import time
    timestamp = int(time.time())
    test_user_data = {
        "email": f"test_fix_{timestamp}@versaai.com",
        "password": "testpassword123",
        "full_name": "Test Fix User"
    }
    
    print(f"📝 Registrando usuario: {test_user_data['email']}")
    
    # Realizar registro
    response = client.post("/api/v1/auth/register", json=test_user_data)
    
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code in [200, 201]:
        response_data = response.json()
        print("✅ Registro exitoso!")
        print(f"📋 Respuesta completa: {json.dumps(response_data, indent=2, default=str)}")
        
        # Verificar que updated_at no es None
        updated_at = response_data.get('updated_at')
        if updated_at is not None:
            print(f"✅ updated_at tiene valor: {updated_at}")
            print("🎉 PROBLEMA RESUELTO: updated_at ya no es None")
            return True
        else:
            print("❌ ERROR: updated_at sigue siendo None")
            return False
    else:
        print(f"❌ Error en el registro: {response.status_code}")
        print(f"📋 Respuesta de error: {response.text}")
        return False

def test_schema_from_orm():
    """
    Verifica que el método from_orm del esquema funciona correctamente
    """
    print("\n🔍 Verificando el método from_orm del esquema...")
    
    # Simular un objeto de usuario con updated_at None
    class MockUser:
        def __init__(self):
            self.id = 1
            self.email = "test@example.com"
            self.username = "testuser"
            self.full_name = "Test User"
            self.is_active = True
            self.role = "user"
            self.organization_id = None
            self.is_verified = False
            self.created_at = datetime.utcnow()
            self.updated_at = None  # Esto es lo que causaba el problema
    
    mock_user = MockUser()
    print(f"📝 Usuario mock creado con updated_at = {mock_user.updated_at}")
    
    try:
        # Usar el método from_orm
        response_schema = UserRegistrationResponse.from_orm(mock_user)
        print(f"✅ Esquema creado exitosamente")
        print(f"📋 updated_at en el esquema: {response_schema.updated_at}")
        
        if response_schema.updated_at is not None:
            print("✅ El método from_orm maneja correctamente updated_at = None")
            return True
        else:
            print("❌ ERROR: El método from_orm no maneja updated_at = None")
            return False
            
    except Exception as e:
        print(f"❌ ERROR al crear el esquema: {str(e)}")
        return False

def main():
    print("🚀 Iniciando verificación final del fix...\n")
    
    # Test 1: Verificar el endpoint real
    endpoint_test = test_updated_at_fix()
    
    # Test 2: Verificar el método from_orm
    schema_test = test_schema_from_orm()
    
    print("\n📊 RESUMEN DE VERIFICACIÓN:")
    print(f"   Endpoint de registro: {'✅ PASÓ' if endpoint_test else '❌ FALLÓ'}")
    print(f"   Método from_orm: {'✅ PASÓ' if schema_test else '❌ FALLÓ'}")
    
    if endpoint_test and schema_test:
        print("\n🎉 ¡ÉXITO! El problema del updated_at se ha resuelto completamente.")
        print("   - El endpoint de registro funciona correctamente")
        print("   - El método from_orm maneja updated_at = None apropiadamente")
        print("   - Los tests están pasando")
        return True
    else:
        print("\n❌ Aún hay problemas que resolver.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)