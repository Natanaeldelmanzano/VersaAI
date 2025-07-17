#!/usr/bin/env python3
"""
Script de depuración para verificar la creación de usuarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import get_db
from src.models.user import User
from src.services.auth_service import auth_service
from datetime import datetime
import json

def debug_user_creation():
    """Depurar la creación de usuarios"""
    print("🔍 Depurando creación de usuarios...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Datos de prueba
        test_email = f"debug_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.com"
        test_username = f"debug_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_password = "test123456"
        test_full_name = "Debug User"
        
        print(f"📧 Email: {test_email}")
        print(f"👤 Username: {test_username}")
        
        # Crear usuario usando el servicio
        print("\n1️⃣ Creando usuario con auth_service...")
        user = auth_service.register_user(
            db=db,
            email=test_email,
            password=test_password,
            username=test_username,
            full_name=test_full_name
        )
        
        if not user:
            print("❌ Error: No se pudo crear el usuario")
            return
        
        print(f"✅ Usuario creado con ID: {user.id}")
        
        # Verificar campos de tiempo
        print("\n2️⃣ Verificando campos de tiempo...")
        print(f"created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        
        # Refrescar desde la base de datos
        print("\n3️⃣ Refrescando desde la base de datos...")
        db.refresh(user)
        print(f"created_at después de refresh: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"updated_at después de refresh: {user.updated_at} (tipo: {type(user.updated_at)})")
        
        # Intentar crear el esquema de respuesta
        print("\n4️⃣ Probando esquema de respuesta...")
        try:
            from src.schemas.user import UserRegistrationResponse
            
            # Método 1: from_orm
            print("Probando from_orm...")
            try:
                response1 = UserRegistrationResponse.from_orm(user)
                print(f"✅ from_orm exitoso: {response1.updated_at}")
            except Exception as e:
                print(f"❌ from_orm falló: {e}")
            
            # Método 2: construcción manual
            print("Probando construcción manual...")
            try:
                response_data = {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "role": user.role,
                    "organization_id": user.organization_id,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at or user.created_at
                }
                response2 = UserRegistrationResponse(**response_data)
                print(f"✅ Construcción manual exitosa: {response2.updated_at}")
            except Exception as e:
                print(f"❌ Construcción manual falló: {e}")
                
        except Exception as e:
            print(f"❌ Error importando esquema: {e}")
        
        # Limpiar - eliminar usuario de prueba
        print("\n5️⃣ Limpiando usuario de prueba...")
        db.delete(user)
        db.commit()
        print("✅ Usuario de prueba eliminado")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    debug_user_creation()