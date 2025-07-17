#!/usr/bin/env python3

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

def test_user_organization():
    print("🔐 Logging in...")
    
    # Login
    login_data = {
        "email": "testuser@versaai.com",
        "password": "testpassword123"
    }
    
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token_data = login_response.json()
    access_token = token_data["access_token"]
    print("✅ Login successful")
    
    # Get current user info
    print("\n👤 Getting current user info...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    user_response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=headers
    )
    
    if user_response.status_code == 200:
        user_data = user_response.json()
        print(f"✅ User info retrieved:")
        print(f"   - ID: {user_data.get('id')}")
        print(f"   - Email: {user_data.get('email')}")
        print(f"   - Organization ID: {user_data.get('organization_id')}")
        print(f"   - Role: {user_data.get('role')}")
        
        if user_data.get('organization_id') is None:
            print("\n⚠️  WARNING: User has no organization assigned!")
            print("   This is likely causing the chatbot creation to fail.")
        else:
            print(f"\n✅ User has organization ID: {user_data.get('organization_id')}")
    else:
        print(f"❌ Failed to get user info: {user_response.status_code}")
        print(f"Response: {user_response.text}")

if __name__ == "__main__":
    test_user_organization()