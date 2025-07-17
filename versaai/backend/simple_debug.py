#!/usr/bin/env python3
"""
Script simple de depuración para timestamps
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import get_db
from src.models.user import User
from src.services.auth_service import auth_service
from datetime import datetime

def simple_debug():
    """Depuración simple"""
    print("🔍 Depuración simple de timestamps...")
    
    db = next(get_db())
    
    try:
        # Crear usuario directamente
        current_time = datetime.utcnow()
        print(f"Tiempo actual: {current_time}")
        
        user = User(
            email="simple_test@test.com",
            username="simple_test",
            full_name="Simple Test",
            hashed_password="test",
            created_at=current_time,
            updated_at=current_time
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"Usuario creado:")
        print(f"  ID: {user.id}")
        print(f"  created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"  updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        
        # Probar esquema
        from src.schemas.user import UserRegistrationResponse
        
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
            "updated_at": user.updated_at
        }
        
        print(f"\nDatos para esquema:")
        for key, value in response_data.items():
            print(f"  {key}: {value} (tipo: {type(value)})")
        
        try:
            response = UserRegistrationResponse(**response_data)
            print(f"\n✅ Esquema creado exitosamente!")
            print(f"Response updated_at: {response.updated_at}")
        except Exception as e:
            print(f"\n❌ Error creando esquema: {e}")
        
        # Limpiar
        db.delete(user)
        db.commit()
        print("\n✅ Usuario eliminado")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    simple_debug()