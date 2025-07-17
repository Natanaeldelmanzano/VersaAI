#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlalchemy.orm import Session
from backend.src.core.database import get_db
from backend.src.models.user import User
from backend.src.schemas.user import UserRegistrationResponse
from backend.src.services.auth_service import AuthService
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_registration_process():
    """Debug the complete registration process step by step"""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        print("=== Starting Registration Debug ===")
        
        # Initialize auth service
        auth_service = AuthService()
        
        # Test data
        email = "debug@test.com"
        password = "testpass123"
        username = "debuguser"
        full_name = "Debug Test User"
        
        print(f"\n1. Creating user with data:")
        print(f"   Email: {email}")
        print(f"   Username: {username}")
        print(f"   Full Name: {full_name}")
        
        # Delete existing user if exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            print(f"\n2. Deleting existing user: {existing_user.email}")
            db.delete(existing_user)
            db.commit()
        
        # Register user
        print(f"\n3. Calling auth_service.register_user...")
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
        
        print(f"✅ User created successfully!")
        
        # Refresh user from database
        print(f"\n4. Refreshing user from database...")
        db.refresh(user)
        
        # Print user attributes
        print(f"\n5. User object attributes:")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Full Name: {user.full_name}")
        print(f"   Created At: {user.created_at} (type: {type(user.created_at)})")
        print(f"   Updated At: {user.updated_at} (type: {type(user.updated_at)})")
        print(f"   Is Active: {user.is_active}")
        print(f"   Role: {user.role}")
        print(f"   Organization ID: {user.organization_id}")
        print(f"   Is Verified: {user.is_verified}")
        
        # Check if updated_at is None
        if user.updated_at is None:
            print(f"\n⚠️  WARNING: updated_at is None!")
        else:
            print(f"\n✅ updated_at has value: {user.updated_at}")
        
        # Try to create UserRegistrationResponse
        print(f"\n6. Creating UserRegistrationResponse...")
        
        try:
            # First, let's try to create the response manually
            response_data = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "role": user.role,
                "organization_id": user.organization_id,
                "is_verified": user.is_verified,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
            
            print(f"\n7. Response data dictionary:")
            for key, value in response_data.items():
                print(f"   {key}: {value} (type: {type(value)})")
            
            # Try model_validate
            print(f"\n8. Attempting UserRegistrationResponse.model_validate...")
            response = UserRegistrationResponse.model_validate(user, from_attributes=True)
            print(f"✅ UserRegistrationResponse created successfully!")
            print(f"   Response: {response}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating UserRegistrationResponse: {e}")
            print(f"   Error type: {type(e)}")
            
            # Try creating response with dict
            print(f"\n9. Attempting UserRegistrationResponse with dict...")
            try:
                response = UserRegistrationResponse(**response_data)
                print(f"✅ UserRegistrationResponse created with dict!")
                print(f"   Response: {response}")
            except Exception as e2:
                print(f"❌ Error creating UserRegistrationResponse with dict: {e2}")
            
            return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        try:
            test_user = db.query(User).filter(User.email == "debug@test.com").first()
            if test_user:
                db.delete(test_user)
                db.commit()
                print(f"\n🧹 Cleaned up test user")
        except:
            pass
        
        db.close()

if __name__ == "__main__":
    success = debug_registration_process()
    if success:
        print("\n🎉 Debug completed successfully!")
    else:
        print("\n💥 Debug found issues!")