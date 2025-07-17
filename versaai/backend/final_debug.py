#!/usr/bin/env python3
"""
Script final de depuración - Sin logging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Deshabilitar TODO el logging
import logging
logging.disable(logging.CRITICAL)

from src.core.database import get_db
from src.models.user import User
from datetime import datetime

def final_debug():
    """Depuración final sin logging"""
    print("🔍 DEPURACIÓN FINAL - RESULTADOS ÚNICAMENTE")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        # Crear usuario directamente
        current_time = datetime.utcnow()
        print(f"⏰ Tiempo actual: {current_time}")
        
        user = User(
            email="final_test@test.com",
            username="final_test",
            full_name="Final Test",
            hashed_password="test",
            created_at=current_time,
            updated_at=current_time
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"\n📊 USUARIO CREADO:")
        print(f"   ID: {user.id}")
        print(f"   created_at: {user.created_at}")
        print(f"   updated_at: {user.updated_at}")
        print(f"   created_at tipo: {type(user.created_at)}")
        print(f"   updated_at tipo: {type(user.updated_at)}")
        
        print(f"\n🔍 VERIFICACIÓN DE NONE:")
        print(f"   created_at is None: {user.created_at is None}")
        print(f"   updated_at is None: {user.updated_at is None}")
        
        # Probar esquema Pydantic
        from src.schemas.user import UserRegistrationResponse
        
        print(f"\n🧪 PROBANDO ESQUEMA PYDANTIC:")
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
            print(f"   ✅ ÉXITO! Esquema creado correctamente")
            print(f"   Response updated_at: {response.updated_at}")
            print(f"   Response updated_at tipo: {type(response.updated_at)}")
        except Exception as e:
            print(f"   ❌ ERROR en esquema: {str(e)}")
            print(f"   Valor updated_at: {repr(user.updated_at)}")
            print(f"   Tipo updated_at: {type(user.updated_at)}")
            
            # Intentar con from_orm
            print(f"\n🔄 PROBANDO CON from_orm:")
            try:
                response = UserRegistrationResponse.from_orm(user)
                print(f"   ✅ from_orm ÉXITO!")
                print(f"   Response updated_at: {response.updated_at}")
            except Exception as e2:
                print(f"   ❌ from_orm también falló: {str(e2)}")
        
        # Limpiar
        db.delete(user)
        db.commit()
        print(f"\n🗑️ Usuario eliminado")
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
        
    print("=" * 50)
    print("🏁 DEPURACIÓN COMPLETADA")

if __name__ == "__main__":
    final_debug()