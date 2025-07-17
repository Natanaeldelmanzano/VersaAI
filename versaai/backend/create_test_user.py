#!/usr/bin/env python3
"""
Script para crear un usuario de prueba con credenciales conocidas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.auth_service import AuthService
from src.core.database import get_db
from src.models.user import User
from sqlalchemy.orm import Session
from src.core.config import settings
from src.schemas.user import UserCreate

def create_test_user():
    print("🔧 CREANDO USUARIO DE PRUEBA")
    print("=" * 50)
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Obtener sesión de base de datos
    db_gen = get_db()
    db: Session = next(db_gen)
    
    try:
        # Datos del usuario de prueba
        email = "testlogin@versaai.com"
        password = "testpass123"
        
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"🗑️ Eliminando usuario existente: {email}")
            db.delete(existing_user)
            db.commit()
        
        # Crear nuevo usuario
        auth_service = AuthService()
        new_user = auth_service.register_user(
            db=db,
            email=email,
            password=password,
            username="testlogin",
            full_name="Usuario de Prueba Login"
        )
        
        print(f"✅ Usuario creado: {new_user.email}")
        print(f"   ID: {new_user.id}")
        print(f"   Username: {new_user.username}")
        print(f"   Contraseña: {password}")
        
        # Probar autenticación inmediatamente
        print(f"\n🔐 Probando autenticación...")
        authenticated_user = auth_service.authenticate_user(db, email, password)
        
        if authenticated_user:
            print("✅ Autenticación exitosa")
            return {"email": email, "password": password}
        else:
            print("❌ Autenticación falló")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    result = create_test_user()
    if result:
        print(f"\n🎉 Usuario listo para usar:")
        print(f"   Email: {result['email']}")
        print(f"   Password: {result['password']}")