#!/usr/bin/env python3
"""
Script para crear usuarios de demostración con diferentes roles
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.models.user import User, UserRole
from src.models.organization import Organization
from src.services.auth_service import AuthService
from datetime import datetime

def create_demo_users():
    print("🚀 Creando usuarios de demostración con diferentes roles...")
    
    # Crear conexión
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # Crear organización de demostración si no existe
        demo_org = db.query(Organization).filter(Organization.name == "Demo Organization").first()
        if not demo_org:
            demo_org = Organization(
                name="Demo Organization",
                slug="demo-organization",
                description="Organización de demostración para VersaAI",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(demo_org)
            db.commit()
            db.refresh(demo_org)
            print(f"✅ Organización creada: {demo_org.name}")
        
        # Lista de usuarios de demostración
        demo_users = [
            {
                "email": "superadmin@versaai.com",
                "password": "super123456",
                "username": "superadmin",
                "full_name": "Super Administrador",
                "role": UserRole.SUPER_ADMIN,
                "organization_id": None  # Super admin no pertenece a una organización específica
            },
            {
                "email": "admin@versaai.com",
                "password": "admin123456",
                "username": "admin",
                "full_name": "Administrador de Organización",
                "role": UserRole.ORG_ADMIN,
                "organization_id": demo_org.id
            },
            {
                "email": "user@versaai.com",
                "password": "user123456",
                "username": "user",
                "full_name": "Usuario Regular",
                "role": UserRole.USER,
                "organization_id": demo_org.id
            },
            {
                "email": "viewer@versaai.com",
                "password": "viewer123456",
                "username": "viewer",
                "full_name": "Usuario Visualizador",
                "role": UserRole.VIEWER,
                "organization_id": demo_org.id
            },
            {
                "email": "demo@versaai.com",
                "password": "demo123456",
                "username": "demo",
                "full_name": "Usuario Demo",
                "role": UserRole.USER,
                "organization_id": demo_org.id
            }
        ]
        
        created_users = []
        
        for user_data in demo_users:
            # Verificar si el usuario ya existe
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            
            if existing_user:
                # Actualizar usuario existente
                existing_user.hashed_password = auth_service.get_password_hash(user_data["password"])
                existing_user.role = user_data["role"]
                existing_user.organization_id = user_data["organization_id"]
                existing_user.is_active = True
                existing_user.is_verified = True
                existing_user.updated_at = datetime.utcnow()
                
                db.commit()
                created_users.append(existing_user)
                print(f"🔄 Usuario actualizado: {user_data['email']} - Rol: {user_data['role'].value}")
            else:
                # Crear nuevo usuario
                new_user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    full_name=user_data["full_name"],
                    hashed_password=auth_service.get_password_hash(user_data["password"]),
                    role=user_data["role"],
                    organization_id=user_data["organization_id"],
                    is_active=True,
                    is_verified=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                created_users.append(new_user)
                print(f"✅ Usuario creado: {user_data['email']} - Rol: {user_data['role'].value}")
        
        print(f"\n🎉 Proceso completado! {len(created_users)} usuarios configurados.")
        
        # Mostrar resumen de credenciales
        print("\n📋 CREDENCIALES DE ACCESO:")
        print("=" * 50)
        for user_data in demo_users:
            print(f"👤 {user_data['full_name']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Contraseña: {user_data['password']}")
            print(f"   Rol: {user_data['role'].value}")
            print()
        
        # Probar autenticación de cada usuario
        print("🔐 VERIFICANDO AUTENTICACIÓN:")
        print("=" * 50)
        for user_data in demo_users:
            auth_result = auth_service.authenticate_user(db, user_data["email"], user_data["password"])
            if auth_result:
                print(f"✅ {user_data['email']} - Autenticación exitosa")
            else:
                print(f"❌ {user_data['email']} - Autenticación fallida")
        
        return created_users
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return []
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_users()