#!/usr/bin/env python3
"""
Demo setup utilities for VersaAI multi-user system
Automatically creates demo users with different roles during backend startup
"""

import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

from ..core.config import settings
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.organization import Organization
from ..services.auth_service import AuthService

logger = logging.getLogger(__name__)

async def initialize_demo_users():
    """
    Initialize demo users for multi-user system
    Creates users with different roles as specified in INSTRUCCIONES_MULTI_USUARIO.md
    """
    logger.info("🚀 Initializing demo users for multi-user system...")
    
    # Create database session
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    auth_service = AuthService()
    
    try:
        # Create demo organization if it doesn't exist
        demo_org = db.query(Organization).filter(Organization.name == "Demo Organization").first()
        if not demo_org:
            demo_org = Organization(
                name="Demo Organization",
                slug="demo-organization",
                description="Organización de demostración para VersaAI - Sistema Multi-Usuario",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(demo_org)
            db.commit()
            db.refresh(demo_org)
            logger.info(f"✅ Demo organization created: {demo_org.name}")
        
        # Demo users configuration as per INSTRUCCIONES_MULTI_USUARIO.md
        demo_users_config = [
            {
                "email": "superadmin@versaai.com",
                "password": "super123456",
                "username": "superadmin",
                "full_name": "Super Administrador",
                "role": UserRole.SUPER_ADMIN,
                "organization_id": None,  # Super admin doesn't belong to specific org
                "description": "Acceso completo al sistema, configuración del sistema, gestión de usuarios y organizaciones"
            },
            {
                "email": "admin@versaai.com",
                "password": "admin123456",
                "username": "admin",
                "full_name": "Administrador de Organización",
                "role": UserRole.ORG_ADMIN,
                "organization_id": demo_org.id,
                "description": "Gestión de organización, creación de usuarios, visualización de analíticas"
            },
            {
                "email": "user@versaai.com",
                "password": "user123456",
                "username": "user",
                "full_name": "Usuario Estándar",
                "role": UserRole.USER,
                "organization_id": demo_org.id,
                "description": "Acceso a datos propios, creación de conversaciones, gestión de chatbots propios"
            },
            {
                "email": "viewer@versaai.com",
                "password": "viewer123456",
                "username": "viewer",
                "full_name": "Usuario Visualizador",
                "role": UserRole.VIEWER,
                "organization_id": demo_org.id,
                "description": "Solo lectura, visualización de conversaciones y chatbots"
            },
            {
                "email": "demo@versaai.com",
                "password": "demo123456",
                "username": "demo",
                "full_name": "Usuario Demo",
                "role": UserRole.USER,
                "organization_id": demo_org.id,
                "description": "Usuario estándar adicional para demostraciones"
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for user_config in demo_users_config:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_config["email"]).first()
            
            if existing_user:
                # Update existing user
                existing_user.hashed_password = auth_service.get_password_hash(user_config["password"])
                existing_user.role = user_config["role"]
                existing_user.organization_id = user_config["organization_id"]
                existing_user.is_active = True
                existing_user.is_verified = True
                existing_user.updated_at = datetime.utcnow()
                
                db.commit()
                updated_count += 1
                logger.info(f"🔄 Updated demo user: {user_config['email']} - Role: {user_config['role'].value}")
            else:
                # Create new user
                new_user = User(
                    email=user_config["email"],
                    username=user_config["username"],
                    full_name=user_config["full_name"],
                    hashed_password=auth_service.get_password_hash(user_config["password"]),
                    role=user_config["role"],
                    organization_id=user_config["organization_id"],
                    is_active=True,
                    is_verified=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                created_count += 1
                logger.info(f"✅ Created demo user: {user_config['email']} - Role: {user_config['role'].value}")
        
        logger.info(f"🎉 Demo users initialization completed! Created: {created_count}, Updated: {updated_count}")
        
        # Log credentials summary for easy access
        logger.info("📋 DEMO USER CREDENTIALS SUMMARY:")
        logger.info("=" * 50)
        for user_config in demo_users_config:
            logger.info(f"👤 {user_config['full_name']} ({user_config['role'].value})")
            logger.info(f"   📧 Email: {user_config['email']}")
            logger.info(f"   🔑 Password: {user_config['password']}")
            logger.info(f"   📝 {user_config['description']}")
        
        logger.info("=" * 50)
        logger.info("🌐 Access the application at: http://localhost:3000")
        logger.info("📚 Check INSTRUCCIONES_MULTI_USUARIO.md for detailed usage instructions")
        logger.info("📖 Check demo-mode-documentation.html for complete feature overview")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error initializing demo users: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

def get_demo_user_credentials():
    """
    Returns the demo user credentials for reference
    """
    return {
        "super_admin": {"email": "superadmin@versaai.com", "password": "super123456"},
        "org_admin": {"email": "admin@versaai.com", "password": "admin123456"},
        "user": {"email": "user@versaai.com", "password": "user123456"},
        "viewer": {"email": "viewer@versaai.com", "password": "viewer123456"},
        "demo": {"email": "demo@versaai.com", "password": "demo123456"}
    }

def log_demo_mode_info():
    """
    Logs information about demo mode and available features
    """
    logger.info("🎯 VersaAI Multi-User Demo Mode Active")
    logger.info("📋 Available Features:")
    logger.info("   🔄 Role switching with RoleSwitcher component")
    logger.info("   👥 Complete user management system")
    logger.info("   🔐 Real JWT authentication with different permission levels")
    logger.info("   📊 Role-based dashboard access")
    logger.info("   🛡️ Granular permission system")
    logger.info("📚 Documentation available in:")
    logger.info("   📄 INSTRUCCIONES_MULTI_USUARIO.md")
    logger.info("   🌐 demo-mode-documentation.html")