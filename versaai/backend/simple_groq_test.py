#!/usr/bin/env python3

import requests
import json

def test_groq_integration():
    base_url = "http://localhost:8000"
    
    print("=== Testing Groq Integration ===")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Server is running - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Server connection failed: {e}")
        return
    
    # Test 2: Login as demo user
    login_data = {
        "username": "demo@versaai.com",
        "password": "demo123456"
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/v1/auth/login", data=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            print("✓ Login successful")
            headers = {"Authorization": f"Bearer {token}"}
        else:
            print(f"✗ Login failed: {login_response.status_code}")
            return
    except Exception as e:
        print(f"✗ Login error: {e}")
        return
    
    # Test 3: Create a chatbot with Groq
    chatbot_data = {
        "name": "Groq Test Bot",
        "description": "Testing Groq integration",
        "ai_settings": {
            "model_name": "mixtral-8x7b-32768",
            "temperature": 0.7,
            "max_tokens": 1000,
            "system_prompt": "You are a helpful AI assistant powered by Groq."
        }
    }
    
    try:
        chatbot_response = requests.post(
            f"{base_url}/api/v1/chatbots/", 
            json=chatbot_data, 
            headers=headers
        )
        if chatbot_response.status_code == 201:
            chatbot = chatbot_response.json()
            chatbot_id = chatbot["id"]
            print(f"✓ Chatbot created with ID: {chatbot_id}")
            print(f"  Model: {chatbot['ai_settings']['model_name']}")
        else:
            print(f"✗ Chatbot creation failed: {chatbot_response.status_code}")
            print(f"  Response: {chatbot_response.text}")
            return
    except Exception as e:
        print(f"✗ Chatbot creation error: {e}")
        return
    
    # Test 4: Send a message to test Groq
    message_data = {
        "content": "Hello! Can you tell me what AI model you are using?"
    }
    
    try:
        message_response = requests.post(
            f"{base_url}/api/v1/chatbots/{chatbot_id}/messages", 
            json=message_data, 
            headers=headers
        )
        if message_response.status_code == 200:
            response_data = message_response.json()
            print("✓ Message sent successfully")
            print(f"  AI Response: {response_data.get('response', 'No response')}")
        else:
            print(f"✗ Message failed: {message_response.status_code}")
            print(f"  Response: {message_response.text}")
    except Exception as e:
        print(f"✗ Message error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_groq_integration()