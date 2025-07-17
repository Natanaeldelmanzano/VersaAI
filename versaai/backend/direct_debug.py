#!/usr/bin/env python3
"""
Script directo de depuración
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Deshabilitar completamente logging de SQLAlchemy
import logging
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)

from src.core.database import get_db
from src.models.user import User
from datetime import datetime

def direct_debug():
    """Depuración directa"""
    print("🔍 Depuración directa - Solo resultados")
    
    db = next(get_db())
    
    try:
        # Crear usuario directamente
        current_time = datetime.utcnow()
        
        user = User(
            email="direct_test@test.com",
            username="direct_test",
            full_name="Direct Test",
            hashed_password="test",
            created_at=current_time,
            updated_at=current_time
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"\n📊 Usuario creado:")
        print(f"created_at: {user.created_at} | tipo: {type(user.created_at)}")
        print(f"updated_at: {user.updated_at} | tipo: {type(user.updated_at)}")
        
        # Verificar si son None
        print(f"\n🔍 Verificación de None:")
        print(f"created_at is None: {user.created_at is None}")
        print(f"updated_at is None: {user.updated_at is None}")
        
        # Probar esquema
        from src.schemas.user import UserRegistrationResponse
        
        print(f"\n🧪 Probando esquema Pydantic...")
        try:
            response = UserRegistrationResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                role=user.role,
                organization_id=user.organization_id,
                is_verified=user.is_verified,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            print(f"✅ ÉXITO! Esquema creado correctamente")
            print(f"Response updated_at: {response.updated_at}")
        except Exception as e:
            print(f"❌ ERROR en esquema: {str(e)}")
            print(f"Detalles del error:")
            print(f"  - updated_at valor: {repr(user.updated_at)}")
            print(f"  - updated_at tipo: {type(user.updated_at)}")
            
            # Intentar con from_orm
            print(f"\n🔄 Probando with from_orm...")
            try:
                response = UserRegistrationResponse.from_orm(user)
                print(f"✅ from_orm ÉXITO!")
            except Exception as e2:
                print(f"❌ from_orm también falló: {str(e2)}")
        
        # Limpiar
        db.delete(user)
        db.commit()
        print(f"\n🗑️ Usuario eliminado")
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    direct_debug()