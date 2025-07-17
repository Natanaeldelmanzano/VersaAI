#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from src.core.database import get_db, engine
from src.models.user import User, UserRole
from src.models.organization import Organization
from src.services.auth_service import AuthService
from datetime import datetime

def create_test_user_with_organization():
    """Create a test user with an organization for testing chatbot creation"""
    
    # Create database session and auth service
    db = next(get_db())
    auth_service = AuthService()
    
    try:
        # First, create an organization if it doesn't exist
        org = db.query(Organization).filter(Organization.name == "Test Organization").first()
        if not org:
            print("Creating test organization...")
            org = Organization(
                name="Test Organization",
                slug="test-organization",
                description="Test organization for development",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(org)
            db.commit()
            db.refresh(org)
            print(f"✅ Created organization: {org.name} (ID: {org.id})")
        else:
            print(f"✅ Using existing organization: {org.name} (ID: {org.id})")
        
        # Check if user already exists (by email or username)
        existing_user = db.query(User).filter(
            (User.email == "testuser@versaai.com") | (User.username == "testuser")
        ).first()
        if existing_user:
            print("Updating existing test user...")
            existing_user.organization_id = org.id
            existing_user.email = "testuser@versaai.com"
            existing_user.username = "testuser"
            existing_user.hashed_password = auth_service.get_password_hash("testpassword123")
            db.commit()
            print(f"✅ Updated user: {existing_user.email} (ID: {existing_user.id})")
            print(f"✅ Organization: {org.name} (ID: {org.id})")
            print(f"   - Role: {existing_user.role}")
            return existing_user, org
        else:
            print("Creating new test user...")
            # Create test user with organization
            test_user = User(
                email="testuser@versaai.com",
                username="testuser",
                full_name="Test User",
                hashed_password=auth_service.get_password_hash("testpassword123"),
                is_active=True,
                is_verified=True,
                role=UserRole.ORG_ADMIN,
                organization_id=org.id,
                created_at=datetime.utcnow()
            )
            
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            print(f"✅ Created user: {test_user.email} (ID: {test_user.id})")
            print(f"   - Organization ID: {test_user.organization_id}")
            print(f"   - Role: {test_user.role}")
        
        print("\n🎯 Test credentials:")
        print("   Email: testuser@versaai.com")
        print("   Password: testpassword123")
        print(f"   Organization ID: {org.id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user_with_organization()