#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Completely disable all SQLAlchemy logging
import logging
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.orm').setLevel(logging.CRITICAL)

# Disable all other loggers
logging.getLogger().setLevel(logging.CRITICAL)

from sqlalchemy.orm import Session
from backend.src.core.database import get_db
from backend.src.models.user import User
from backend.src.schemas.user import UserRegistrationResponse
from backend.src.services.auth_service import AuthService
from datetime import datetime

def test_registration():
    """Test registration process without logs"""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        print("\n" + "="*50)
        print("TESTING REGISTRATION PROCESS")
        print("="*50)
        
        # Initialize auth service
        auth_service = AuthService()
        
        # Test data
        email = "final@test.com"
        password = "testpass123"
        username = "finaluser"
        full_name = "Final Test User"
        
        print(f"\n1. Test Data:")
        print(f"   Email: {email}")
        print(f"   Username: {username}")
        
        # Delete existing user if exists (silently)
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            print(f"\n2. Deleting existing user...")
            db.delete(existing_user)
            db.commit()
        else:
            print(f"\n2. No existing user found")
        
        # Register user
        print(f"\n3. Creating new user...")
        user = auth_service.register_user(
            db=db,
            email=email,
            password=password,
            username=username,
            full_name=full_name,
            organization_id=None
        )
        
        if not user:
            print("   ❌ FAILED: User registration returned None")
            return False
        
        print(f"   ✅ SUCCESS: User created with ID {user.id}")
        
        # Refresh user from database
        print(f"\n4. Refreshing user from database...")
        db.refresh(user)
        
        # Check timestamps
        print(f"\n5. Checking timestamps:")
        print(f"   created_at: {user.created_at}")
        print(f"   created_at type: {type(user.created_at)}")
        print(f"   updated_at: {user.updated_at}")
        print(f"   updated_at type: {type(user.updated_at)}")
        
        if user.updated_at is None:
            print(f"   ⚠️  WARNING: updated_at is None!")
            return False
        else:
            print(f"   ✅ Both timestamps are valid")
        
        # Test UserRegistrationResponse creation
        print(f"\n6. Testing UserRegistrationResponse creation...")
        
        try:
            response = UserRegistrationResponse.model_validate(user, from_attributes=True)
            print(f"   ✅ SUCCESS: UserRegistrationResponse created")
            print(f"   Response ID: {response.id}")
            print(f"   Response email: {response.email}")
            print(f"   Response updated_at: {response.updated_at}")
            
            # Test JSON serialization
            print(f"\n7. Testing JSON serialization...")
            response_dict = response.model_dump()
            print(f"   ✅ SUCCESS: Response serialized to dict")
            print(f"   Dict keys: {list(response_dict.keys())}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ FAILED: UserRegistrationResponse creation failed")
            print(f"   Error: {e}")
            print(f"   Error type: {type(e)}")
            return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print(f"Error type: {type(e)}")
        return False
    
    finally:
        # Clean up
        try:
            test_user = db.query(User).filter(User.email == email).first()
            if test_user:
                db.delete(test_user)
                db.commit()
                print(f"\n8. ✅ Cleaned up test user")
        except:
            print(f"\n8. ⚠️  Could not clean up test user")
        
        db.close()
        print(f"\n" + "="*50)

if __name__ == "__main__":
    success = test_registration()
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The registration process works correctly.")
    else:
        print("\n💥 TESTS FAILED!")
        print("There are issues with the registration process.")
    print("\n" + "="*50)