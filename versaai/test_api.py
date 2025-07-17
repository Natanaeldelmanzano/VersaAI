import requests
import json

# Test registration endpoint
import time
url = "http://localhost:8000/api/v1/auth/register"
data = {
    "email": f"test{int(time.time())}@versaai.com",
    "password": "testpass123",
    "full_name": "Test User"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'response'):
        print(f"Response text: {e.response.text}")