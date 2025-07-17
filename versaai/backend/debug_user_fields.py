#!/usr/bin/env python3
"""
Script para depurar específicamente los campos del usuario después del registro
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.auth_service import auth_service
from src.models.user import User
from src.schemas.user import UserRegistrationResponse

def debug_user_creation():
    """Depurar la creación de usuario paso a paso"""
    
    print("🔧 Debug de Creación de Usuario")
    print("=" * 50)
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Datos de prueba únicos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        email = f"debug_fields_{timestamp}@test.com"
        username = f"debug_fields_{timestamp}"
        password = "testpassword123"
        full_name = "Debug Fields User"
        
        print(f"📝 Datos de prueba:")
        print(f"   Email: {email}")
        print(f"   Username: {username}")
        print(f"   Full Name: {full_name}")
        print()
        
        # 1. Limpiar usuario existente si existe
        print("🗑️ Limpiando usuario existente...")
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print(f"   ✅ Usuario existente eliminado (ID: {existing_user.id})")
        else:
            print("   ℹ️ No hay usuario existente")
        print()
        
        # 2. Registrar usuario usando el servicio
        print("👤 Registrando usuario con auth_service...")
        user = auth_service.register_user(
            db=db,
            email=email,
            password=password,
            username=username,
            full_name=full_name
        )
        
        if not user:
            print("❌ Error: auth_service.register_user devolvió None")
            return False
        
        print(f"   ✅ Usuario registrado con ID: {user.id}")
        print()
        
        # 3. Verificar campos ANTES del refresh
        print("🔍 Campos ANTES del refresh:")
        print(f"   user.id: {user.id} (tipo: {type(user.id)})")
        print(f"   user.email: {user.email} (tipo: {type(user.email)})")
        print(f"   user.username: {user.username} (tipo: {type(user.username)})")
        print(f"   user.created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"   user.updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        print(f"   user.is_active: {user.is_active} (tipo: {type(user.is_active)})")
        print(f"   user.role: {user.role} (tipo: {type(user.role)})")
        print()
        
        # 4. Hacer refresh
        print("🔄 Haciendo db.refresh(user)...")
        db.refresh(user)
        print("   ✅ Refresh completado")
        print()
        
        # 5. Verificar campos DESPUÉS del refresh
        print("🔍 Campos DESPUÉS del refresh:")
        print(f"   user.id: {user.id} (tipo: {type(user.id)})")
        print(f"   user.email: {user.email} (tipo: {type(user.email)})")
        print(f"   user.username: {user.username} (tipo: {type(user.username)})")
        print(f"   user.created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"   user.updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        print(f"   user.is_active: {user.is_active} (tipo: {type(user.is_active)})")
        print(f"   user.role: {user.role} (tipo: {type(user.role)})")
        print()
        
        # 6. Verificar valores None específicamente
        print("❓ Verificación de valores None:")
        print(f"   created_at is None: {user.created_at is None}")
        print(f"   updated_at is None: {user.updated_at is None}")
        print()
        
        # 7. Construir response_data como en el endpoint
        print("📋 Construyendo response_data...")
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
        
        print("   📄 response_data:")
        for key, value in response_data.items():
            print(f"      {key}: {value} (tipo: {type(value)})")
        print()
        
        # 8. Intentar crear UserRegistrationResponse
        print("🏗️ Creando UserRegistrationResponse...")
        try:
            response = UserRegistrationResponse(**response_data)
            print("   ✅ UserRegistrationResponse creado exitosamente")
            print(f"   📄 Response:")
            print(f"      id: {response.id}")
            print(f"      email: {response.email}")
            print(f"      username: {response.username}")
            print(f"      created_at: {response.created_at}")
            print(f"      updated_at: {response.updated_at}")
            
        except Exception as e:
            print(f"   ❌ Error creando UserRegistrationResponse: {e}")
            print(f"   📄 Tipo de error: {type(e)}")
            return False
        
        print()
        
        # 9. Limpiar usuario de prueba
        print("🗑️ Limpiando usuario de prueba...")
        db.delete(user)
        db.commit()
        print("   ✅ Usuario eliminado")
        
        print()
        print("🎉 Debug completado exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante el debug: {e}")
        print(f"📄 Tipo de error: {type(e)}")
        db.rollback()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    success = debug_user_creation()
    sys.exit(0 if success else 1)