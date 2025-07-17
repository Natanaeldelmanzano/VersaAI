import requests

# Test the temporary refresh endpoint
print("=== Testing Temporary Refresh Endpoint ===")
response = requests.post("http://localhost:8000/api/v1/auth/refresh-temp")
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

# Test the main refresh endpoint with minimal data
print("\n=== Testing Main Refresh Endpoint ===")
data = {"refresh_token": "dummy_token"}
response = requests.post("http://localhost:8000/api/v1/auth/refresh", json=data)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print(f"Response: {response.json()}")
else:
    print(f"Error: {response.text}")