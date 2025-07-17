#!/usr/bin/env python3
import requests
import json

def test_create_chatbot():
    base_url = "http://localhost:8000/api/v1"
    
    # Login first
    login_data = {
        "email": "testuser@versaai.com",
        "password": "testpassword123"
    }
    
    print("🔐 Logging in...")
    login_response = requests.post(f"{base_url}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    print("✅ Login successful")
    
    # Create chatbot
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    chatbot_data = {
        "name": "Test Chatbot",
        "description": "A test chatbot created to verify the fix",
        "chatbot_type": "general",
        "is_active": True
    }
    
    print("\n🤖 Creating chatbot...")
    create_response = requests.post(f"{base_url}/chatbots/", json=chatbot_data, headers=headers)
    
    print(f"Status Code: {create_response.status_code}")
    print(f"Response: {json.dumps(create_response.json(), indent=2)}")
    
    if create_response.status_code == 201:
        print("✅ Chatbot created successfully!")
        chatbot_id = create_response.json()["id"]
        
        # Test getting the chatbot
        print(f"\n📖 Getting chatbot {chatbot_id}...")
        get_response = requests.get(f"{base_url}/chatbots/{chatbot_id}", headers=headers)
        print(f"Status Code: {get_response.status_code}")
        print(f"Response: {json.dumps(get_response.json(), indent=2)}")
        
        if get_response.status_code == 200:
            print("✅ Chatbot retrieved successfully!")
        else:
            print("❌ Failed to retrieve chatbot")
    else:
        print("❌ Failed to create chatbot")

if __name__ == "__main__":
    test_create_chatbot()