#!/usr/bin/env python3
"""
Script para simular exactamente el endpoint de registro
y encontrar por qué updated_at es None
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

def simulate_register_endpoint():
    print("🎭 Simulación EXACTA del endpoint de registro")
    print("=" * 60)
    
    # Datos de prueba
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    email = f"endpoint_sim_{timestamp}@test.com"
    password = "testpassword123"
    full_name = "Endpoint Simulation User"
    
    print(f"📝 Datos de prueba:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Full Name: {full_name}")
    print()
    
    # Obtener sesión de DB
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Limpiar usuario existente
        print("🗑️ Limpiando usuario existente...")
        existing = db.query(User).filter(
            (User.email == email) | (User.username == email.split('@')[0])
        ).first()
        if existing:
            db.delete(existing)
            db.commit()
            print("   ✅ Usuario existente eliminado")
        else:
            print("   ℹ️ No hay usuario existente")
        print()
        
        # SIMULAR EXACTAMENTE EL ENDPOINT
        print("🎯 SIMULANDO ENDPOINT EXACTO...")
        print("-" * 40)
        
        # Generate username from email if not provided
        username = email.split('@')[0]
        print(f"📛 Username generado: {username}")
        
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            print("❌ Usuario ya existe")
            return
        else:
            print("✅ Usuario no existe, procediendo...")
        
        # Register user with individual parameters
        print("👤 Llamando auth_service.register_user...")
        user = auth_service.register_user(
            db=db,
            email=email,
            password=password,
            username=username,
            full_name=full_name,
            organization_id=None  # Will be handled later
        )
        
        if not user:
            print("❌ Failed to register user")
            return
        
        print(f"   ✅ Usuario registrado con ID: {user.id}")
        
        # Verificar campos ANTES del refresh
        print("\n🔍 Campos ANTES del refresh:")
        print(f"   user.id: {user.id} (tipo: {type(user.id)})")
        print(f"   user.email: {user.email} (tipo: {type(user.email)})")
        print(f"   user.username: {user.username} (tipo: {type(user.username)})")
        print(f"   user.created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"   user.updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        print(f"   user.is_active: {user.is_active} (tipo: {type(user.is_active)})")
        print(f"   user.role: {user.role} (tipo: {type(user.role)})")
        
        # The auth_service.register_user already commits, so just refresh
        print("\n🔄 Haciendo db.refresh(user)...")
        db.refresh(user)
        print("   ✅ Refresh completado")
        
        # Verificar campos DESPUÉS del refresh
        print("\n🔍 Campos DESPUÉS del refresh:")
        print(f"   user.id: {user.id} (tipo: {type(user.id)})")
        print(f"   user.email: {user.email} (tipo: {type(user.email)})")
        print(f"   user.username: {user.username} (tipo: {type(user.username)})")
        print(f"   user.created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"   user.updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        print(f"   user.is_active: {user.is_active} (tipo: {type(user.is_active)})")
        print(f"   user.role: {user.role} (tipo: {type(user.role)})")
        
        # Verificación de valores None
        print("\n❓ Verificación de valores None:")
        print(f"   created_at is None: {user.created_at is None}")
        print(f"   updated_at is None: {user.updated_at is None}")
        
        # Create response data manually to ensure all fields are properly set
        print("\n📋 Construyendo response_data EXACTAMENTE como el endpoint...")
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
            "updated_at": user.updated_at or user.created_at  # ESTA ES LA LÍNEA PROBLEMÁTICA
        }
        
        print("   📄 response_data:")
        for key, value in response_data.items():
            print(f"      {key}: {value} (tipo: {type(value)})")
        
        # Intentar crear UserRegistrationResponse
        print("\n🏗️ Creando UserRegistrationResponse...")
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
            print(f"   🔍 Tipo de error: {type(e)}")
            import traceback
            print(f"   📋 Traceback completo:")
            traceback.print_exc()
        
        # Limpiar usuario de prueba
        print("\n🗑️ Limpiando usuario de prueba...")
        db.delete(user)
        db.commit()
        print("   ✅ Usuario eliminado")
        
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    print("\n🎉 Simulación completada!")

if __name__ == "__main__":
    simulate_register_endpoint()