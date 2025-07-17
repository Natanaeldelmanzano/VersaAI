import requests
import json
import traceback

def test_chatbots_endpoint():
    base_url = "http://localhost:8000"
    
    # Login first
    login_data = {
        "email": "admin@versaai.com",
        "password": "admin123"
    }
    
    try:
        # Login
        login_response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✅ Login successful")
        
        # Test chatbots endpoint with detailed error handling
        print("\n🔍 Testing chatbots endpoint...")
        
        chatbots_response = requests.get(
            f"{base_url}/api/v1/chatbots/",
            headers=headers
        )
        
        print(f"Status Code: {chatbots_response.status_code}")
        print(f"Headers: {dict(chatbots_response.headers)}")
        print(f"Response Text: {chatbots_response.text}")
        
        if chatbots_response.status_code == 200:
            print("✅ Chatbots endpoint working!")
            data = chatbots_response.json()
            print(f"Response data: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Chatbots endpoint failed: {chatbots_response.status_code}")
            try:
                error_data = chatbots_response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw error response: {chatbots_response.text}")
        
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_chatbots_endpoint()