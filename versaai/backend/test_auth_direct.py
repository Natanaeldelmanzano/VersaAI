#!/usr/bin/env python3
"""
Script para probar autenticación directamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.auth_service import AuthService
from src.core.database import get_db
from src.models.user import User
from sqlalchemy.orm import Session
from src.core.config import settings

def test_direct_auth():
    print("🔍 PRUEBA DIRECTA DE AUTENTICACIÓN")
    print("=" * 50)
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Obtener sesión de base de datos
    db_gen = get_db()
    db: Session = next(db_gen)
    
    try:
        # Buscar usuario demo
        user = db.query(User).filter(User.email == "demo@versaai.com").first()
        if user:
            print(f"✅ Usuario encontrado: {user.email}")
            print(f"   ID: {user.id}")
            print(f"   Username: {user.username}")
            print(f"   Activo: {user.is_active}")
            print(f"   Hash: {user.hashed_password[:50]}...")
            
            # Probar autenticación con AuthService
            auth_service = AuthService()
            authenticated_user = auth_service.authenticate_user(db, "demo@versaai.com", "demo123")
            
            if authenticated_user:
                print("✅ Autenticación exitosa con AuthService")
                return True
            else:
                print("❌ Autenticación falló con AuthService")
                return False
        else:
            print("❌ Usuario demo@versaai.com no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_direct_auth()