#!/usr/bin/env python3
"""
Script para verificar usuarios en la base de datos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.models.user import User
from src.services.auth_service import AuthService

def main():
    print("🔍 Verificando usuarios en la base de datos...")
    
    # Crear conexión
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # Buscar todos los usuarios
        users = db.query(User).all()
        print(f"📊 Total usuarios: {len(users)}")
        
        for user in users:
            print(f"\n👤 Usuario: {user.email}")
            print(f"   ID: {user.id}")
            print(f"   Username: {user.username}")
            print(f"   Activo: {user.is_active}")
            print(f"   Hash: {user.hashed_password[:50]}...")
            
            # Probar contraseñas comunes
            test_passwords = ["test123456", "password", "123456", "admin"]
            for pwd in test_passwords:
                is_valid = auth_service.verify_password(pwd, user.hashed_password)
                if is_valid:
                    print(f"   ✅ Contraseña encontrada: '{pwd}'")
                    break
            else:
                print(f"   ❌ Ninguna contraseña de prueba funciona")
        
        # Crear usuario de prueba con contraseña conocida
        print("\n🔧 Creando usuario de prueba...")
        test_email = "demo@versaai.com"
        test_password = "demo123456"
        
        # Verificar si ya existe
        existing = db.query(User).filter(User.email == test_email).first()
        if existing:
            print(f"ℹ️ Usuario {test_email} ya existe")
            # Actualizar contraseña
            existing.hashed_password = auth_service.get_password_hash(test_password)
            db.commit()
            print(f"🔄 Contraseña actualizada para {test_email}")
        else:
            # Crear nuevo usuario
            new_user = auth_service.register_user(
                db=db,
                email=test_email,
                password=test_password,
                username="demo",
                full_name="Usuario Demo"
            )
            if new_user:
                print(f"✅ Usuario {test_email} creado exitosamente")
            else:
                print(f"❌ Error creando usuario {test_email}")
        
        # Probar autenticación
        print(f"\n🔐 Probando autenticación con {test_email}...")
        auth_result = auth_service.authenticate_user(db, test_email, test_password)
        if auth_result:
            print("✅ Autenticación exitosa")
            print(f"👤 Usuario autenticado: {auth_result.email}")
        else:
            print("❌ Autenticación fallida")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()