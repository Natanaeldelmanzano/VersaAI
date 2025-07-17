#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Disable SQLAlchemy logging
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

from sqlalchemy.orm import Session
from backend.src.core.database import get_db
from backend.src.models.user import User
from backend.src.schemas.user import UserRegistrationResponse
from backend.src.services.auth_service import AuthService
from datetime import datetime

def debug_registration():
    """Simple debug of registration process"""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        print("=== Registration Debug ===")
        
        # Initialize auth service
        auth_service = AuthService()
        
        # Test data
        email = "simple@debug.com"
        password = "testpass123"
        username = "simpleuser"
        full_name = "Simple Debug User"
        
        # Delete existing user if exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            print(f"Deleting existing user: {existing_user.email}")
            db.delete(existing_user)
            db.commit()
        
        # Register user
        print(f"Creating user: {email}")
        user = auth_service.register_user(
            db=db,
            email=email,
            password=password,
            username=username,
            full_name=full_name,
            organization_id=None
        )
        
        if not user:
            print("❌ User registration failed!")
            return False
        
        print(f"✅ User created: ID={user.id}")
        
        # Refresh user from database
        db.refresh(user)
        
        # Print key attributes
        print(f"\nUser attributes:")
        print(f"  created_at: {user.created_at} (type: {type(user.created_at)})")
        print(f"  updated_at: {user.updated_at} (type: {type(user.updated_at)})")
        
        # Check if updated_at is None
        if user.updated_at is None:
            print(f"\n⚠️  WARNING: updated_at is None!")
        else:
            print(f"\n✅ updated_at has value")
        
        # Try to create UserRegistrationResponse
        print(f"\nTesting UserRegistrationResponse.model_validate...")
        
        try:
            response = UserRegistrationResponse.model_validate(user, from_attributes=True)
            print(f"✅ UserRegistrationResponse created successfully!")
            print(f"  Response updated_at: {response.updated_at}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating UserRegistrationResponse: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    finally:
        # Clean up
        try:
            test_user = db.query(User).filter(User.email == email).first()
            if test_user:
                db.delete(test_user)
                db.commit()
                print(f"\n🧹 Cleaned up test user")
        except:
            pass
        
        db.close()

if __name__ == "__main__":
    success = debug_registration()
    if success:
        print("\n🎉 Debug completed successfully!")
    else:
        print("\n💥 Debug found issues!")