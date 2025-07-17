#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlalchemy.orm import Session
from backend.src.core.database import SessionLocal, engine
from backend.src.models.user import User
from backend.src.services.auth_service import auth_service
from datetime import datetime

def debug_user_creation():
    """Debug user creation to see what's happening with updated_at"""
    db = SessionLocal()
    
    try:
        # Create a test user
        print("Creating test user...")
        user = auth_service.register_user(
            db=db,
            email="debug@test.com",
            password="testpass123",
            username="debuguser",
            full_name="Debug User"
        )
        
        if user:
            print(f"User created successfully:")
            print(f"  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Username: {user.username}")
            print(f"  Created at: {user.created_at}")
            print(f"  Updated at: {user.updated_at}")
            print(f"  Updated at type: {type(user.updated_at)}")
            print(f"  Updated at is None: {user.updated_at is None}")
            
            # Try to create the response schema
            from backend.src.schemas.user import UserRegistrationResponse
            
            print("\nTrying to create UserRegistrationResponse...")
            try:
                response = UserRegistrationResponse.model_validate(user, from_attributes=True)
                print(f"Response created successfully: {response}")
            except Exception as e:
                print(f"Error creating response: {e}")
                print(f"Error type: {type(e)}")
                
            # Clean up - delete the test user
            db.delete(user)
            db.commit()
            print("\nTest user deleted.")
        else:
            print("Failed to create user")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    debug_user_creation()