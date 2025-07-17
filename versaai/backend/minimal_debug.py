#!/usr/bin/env python3
"""
Script mínimo de depuración
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Deshabilitar logging de SQLAlchemy
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

from src.core.database import get_db
from src.models.user import User
from datetime import datetime

def minimal_debug():
    """Depuración mínima"""
    print("🔍 Depuración mínima...")
    
    db = next(get_db())
    
    try:
        # Crear usuario directamente
        current_time = datetime.utcnow()
        
        user = User(
            email="minimal_test@test.com",
            username="minimal_test",
            full_name="Minimal Test",
            hashed_password="test",
            created_at=current_time,
            updated_at=current_time
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"\n📊 Resultados:")
        print(f"created_at: {user.created_at} (tipo: {type(user.created_at)})")
        print(f"updated_at: {user.updated_at} (tipo: {type(user.updated_at)})")
        
        # Probar esquema
        from src.schemas.user import UserRegistrationResponse
        
        print(f"\n🧪 Probando esquema...")
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
            print(f"✅ Esquema OK! updated_at: {response.updated_at}")
        except Exception as e:
            print(f"❌ Error en esquema: {e}")
            print(f"Tipo de updated_at: {type(user.updated_at)}")
            print(f"Valor de updated_at: {repr(user.updated_at)}")
        
        # Limpiar
        db.delete(user)
        db.commit()
        print("\n🗑️ Usuario eliminado")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    minimal_debug()