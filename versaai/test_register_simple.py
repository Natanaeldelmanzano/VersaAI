#!/usr/bin/env python3

import requests
import json

def test_register_endpoint():
    """Test the register endpoint with a simple request"""
    
    url = "http://localhost:8000/api/v1/auth/register"
    
    data = {
        "email": "simple@test.com",
        "password": "testpass123",
        "username": "simpleuser",
        "full_name": "Simple Test User"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Testing registration endpoint: {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response JSON: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
        if response.status_code == 200:
            print("\n✅ Registration successful!")
        else:
            print(f"\n❌ Registration failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_register_endpoint()