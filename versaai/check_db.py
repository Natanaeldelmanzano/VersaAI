#!/usr/bin/env python3
"""
Script para verificar la base de datos y usuarios
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from core.config import settings
from models.user import User
from services.auth_service import AuthService

def check_database():
    print("🔍 Verificando base de datos...")
    
    # Crear conexión a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # 1. Verificar si existen usuarios
        print("\n1. Verificando usuarios en la base de datos...")
        users = db.query(User).all()
        print(f"📊 Total de usuarios: {len(users)}")
        
        for user in users:
            print(f"   👤 ID: {user.id}, Email: {user.email}, Username: {user.username}")
            print(f"      Activo: {user.is_active}, Creado: {user.created_at}")
            print(f"      Hash: {user.hashed_password[:50]}...")
        
        # 2. Buscar usuario específico
        print("\n2. Buscando usuario test@versaai.com...")
        test_user = db.query(User).filter(User.email == "test@versaai.com").first()
        
        if test_user:
            print("✅ Usuario encontrado")
            print(f"   📧 Email: {test_user.email}")
            print(f"   👤 Username: {test_user.username}")
            print(f"   🔒 Hash: {test_user.hashed_password}")
            print(f"   ✅ Activo: {test_user.is_active}")
            
            # 3. Probar verificación de contraseña
            print("\n3. Probando verificación de contraseña...")
            test_passwords = ["test123456", "password", "123456"]
            
            for pwd in test_passwords:
                is_valid = auth_service.verify_password(pwd, test_user.hashed_password)
                print(f"   🔑 Contraseña '{pwd}': {'✅ VÁLIDA' if is_valid else '❌ INVÁLIDA'}")
                
            # 4. Crear nueva contraseña hash para comparar
            print("\n4. Creando nuevo hash para 'test123456'...")
            new_hash = auth_service.get_password_hash("test123456")
            print(f"   🔒 Nuevo hash: {new_hash}")
            
            is_valid_new = auth_service.verify_password("test123456", new_hash)
            print(f"   ✅ Verificación del nuevo hash: {'VÁLIDA' if is_valid_new else 'INVÁLIDA'}")
            
        else:
            print("❌ Usuario no encontrado")
            
            # Crear usuario con contraseña conocida
            print("\n🔧 Creando usuario de prueba...")
            new_user = auth_service.register_user(
                db=db,
                email="test2@versaai.com",
                password="test123456",
                username="test2",
                full_name="Usuario de Prueba 2"
            )
            
            if new_user:
                print("✅ Usuario creado exitosamente")
                print(f"   📧 Email: {new_user.email}")
                print(f"   🔒 Hash: {new_user.hashed_password}")
                
                # Probar autenticación inmediatamente
                auth_result = auth_service.authenticate_user(db, "test2@versaai.com", "test123456")
                print(f"   🔐 Autenticación: {'✅ EXITOSA' if auth_result else '❌ FALLIDA'}")
            else:
                print("❌ Error creando usuario")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 VersaAI - Verificación de Base de Datos")
    print("=" * 60)
    
    check_database()
    
    print("\n" + "=" * 60)
    print("🎯 Verificación completada")