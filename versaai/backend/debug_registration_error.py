#!/usr/bin/env python3
"""
Script para depurar el error específico en el registro de usuarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from src.core.database import SessionLocal, engine
from src.models.user import User
from src.schemas.user import UserRegistrationResponse
from src.services.auth_service import AuthService
from datetime import datetime
import traceback
import json

def debug_registration():
    print("🔍 DEPURANDO ERROR DE REGISTRO")
    print("=" * 50)
    
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # Datos de prueba
        test_email = "debug_user@test.com"
        test_password = "testpass123"
        test_username = "debug_user"
        test_full_name = "Debug User"
        
        print(f"📧 Email: {test_email}")
        print(f"👤 Username: {test_username}")
        print(f"📝 Full name: {test_full_name}")
        print()
        
        # Limpiar usuario existente si existe
        existing_user = db.query(User).filter(
            (User.email == test_email) | (User.username == test_username)
        ).first()
        
        if existing_user:
            print(f"🗑️ Eliminando usuario existente: {existing_user.id}")
            db.delete(existing_user)
            db.commit()
        
        print("1️⃣ Registrando usuario...")
        user = auth_service.register_user(
            db=db,
            email=test_email,
            password=test_password,
            username=test_username,
            full_name=test_full_name,
            organization_id=None
        )
        
        if not user:
            print("❌ Error: No se pudo crear el usuario")
            return
        
        print(f"✅ Usuario creado con ID: {user.id}")
        print(f"   created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"   updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        print()
        
        # Verificar que los campos no sean None
        print("2️⃣ Verificando campos...")
        print(f"   created_at is None: {user.created_at is None}")
        print(f"   updated_at is None: {user.updated_at is None}")
        print()
        
        # Intentar crear el esquema de respuesta directamente
        print("3️⃣ Creando esquema de respuesta...")
        try:
            # Método 1: Construcción manual
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
            
            print("   📋 Datos para el esquema:")
            for key, value in response_data.items():
                print(f"      {key}: {value} (tipo: {type(value)})")
            print()
            
            # Intentar crear el esquema
            response = UserRegistrationResponse(**response_data)
            print("   ✅ Esquema creado exitosamente (método manual)")
            print(f"      Response updated_at: {response.updated_at}")
            
        except Exception as e:
            print(f"   ❌ Error creando esquema (método manual): {e}")
            print(f"      Traceback: {traceback.format_exc()}")
        
        print()
        
        # Método 2: from_orm
        print("4️⃣ Probando from_orm...")
        try:
            response_orm = UserRegistrationResponse.from_orm(user)
            print("   ✅ from_orm exitoso")
            print(f"      Response updated_at: {response_orm.updated_at}")
            
        except Exception as e:
            print(f"   ❌ Error con from_orm: {e}")
            print(f"      Traceback: {traceback.format_exc()}")
        
        print()
        
        # Método 3: Serialización JSON
        print("5️⃣ Probando serialización JSON...")
        try:
            # Convertir a dict y luego a JSON
            user_dict = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "role": user.role.value if user.role else None,
                "organization_id": user.organization_id,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": (user.updated_at or user.created_at).isoformat() if (user.updated_at or user.created_at) else None
            }
            
            json_str = json.dumps(user_dict, indent=2)
            print("   ✅ Serialización JSON exitosa")
            print(f"      JSON: {json_str}")
            
        except Exception as e:
            print(f"   ❌ Error en serialización JSON: {e}")
            print(f"      Traceback: {traceback.format_exc()}")
        
        # Limpiar
        print("\n🗑️ Limpiando usuario de prueba...")
        db.delete(user)
        db.commit()
        print("   ✅ Usuario eliminado")
        
    except Exception as e:
        print(f"💥 ERROR GENERAL: {e}")
        print(f"Traceback completo: {traceback.format_exc()}")
        db.rollback()
    
    finally:
        db.close()
    
    print("\n🏁 DEPURACIÓN COMPLETADA")
    print("=" * 50)

if __name__ == "__main__":
    debug_registration()