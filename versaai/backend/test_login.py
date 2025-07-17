#!/usr/bin/env python3
import requests
import json

def test_login():
    base_url = "http://localhost:8000"
    
    # Test data
    login_data = {
        "email": "admin@versaai.com",
        "password": "admin123"  # Assuming this is the password
    }
    
    try:
        # Test login endpoint
        print("Testing login endpoint...")
        response = requests.post(
            f"{base_url}/api/v1/auth/login/json",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print("✅ Login successful!")
                token = data["access_token"]
                
                # Test protected endpoint
                print("\nTesting protected endpoint...")
                headers = {"Authorization": f"Bearer {token}"}
                me_response = requests.get(f"{base_url}/api/v1/auth/me", headers=headers)
                
                print(f"Me endpoint status: {me_response.status_code}")
                print(f"Me endpoint response: {me_response.text}")
                
                if me_response.status_code == 200:
                    print("✅ Authentication system working correctly!")
                else:
                    print("❌ Protected endpoint failed")
            else:
                print("❌ No access token in response")
        else:
            print("❌ Login failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure FastAPI is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()