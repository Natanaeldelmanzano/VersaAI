#!/usr/bin/env python3

import requests
import json
from datetime import datetime
import random
import string

def generate_unique_email():
    """Generate a unique email for testing"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"test_{timestamp}_{random_suffix}@example.com"

def test_registration_endpoint():
    """Test the registration endpoint with unique data"""
    
    # Generate unique test data
    email = generate_unique_email()
    username = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    url = "http://localhost:8000/api/v1/auth/register"
    data = {
        "email": email,
        "password": "testpass123",
        "username": username,
        "full_name": "Unique Test User"
    }
    
    print(f"Testing registration endpoint: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print()
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2, default=str)}")
        except:
            print(f"Response Text: {response.text}")
        
        print()
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            
            # Check if response has expected fields
            if 'id' in response_json:
                print(f"   User ID: {response_json['id']}")
            if 'email' in response_json:
                print(f"   Email: {response_json['email']}")
            if 'username' in response_json:
                print(f"   Username: {response_json['username']}")
            if 'created_at' in response_json:
                print(f"   Created at: {response_json['created_at']}")
            if 'updated_at' in response_json:
                print(f"   Updated at: {response_json['updated_at']}")
            
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Is it running on http://localhost:8000?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING REGISTRATION ENDPOINT WITH UNIQUE DATA")
    print("=" * 60)
    print()
    
    success = test_registration_endpoint()
    
    print()
    print("=" * 60)
    if success:
        print("🎉 ENDPOINT TEST PASSED!")
    else:
        print("💥 ENDPOINT TEST FAILED!")
    print("=" * 60)