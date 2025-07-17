import requests
import json

# Test para identificar el problema exacto
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkB2ZXJzYWFpLmNvbSIsInJvbGUiOiJ1c2VyIiwib3JnX2lkIjpudWxsLCJleHAiOjE3NTI5MDE1MTksInR5cGUiOiJyZWZyZXNoIn0.bolO6X5RffrkIGdGjhKRqOPEej5s3zdCG-nrM9TKDNY"

print("=== Testing Refresh Token ===")
response = requests.post(
    'http://localhost:8000/api/v1/auth/refresh',
    json={'refresh_token': refresh_token}
)

print(f'Status Code: {response.status_code}')
print(f'Response: {json.dumps(response.json(), indent=2)}')

if response.status_code == 200:
    # Si el refresh funciona, probar el verify-token
    access_token = response.json().get('access_token')
    print("\n=== Testing Verify Token ===")
    
    verify_response = requests.post(
        'http://localhost:8000/api/v1/auth/verify-token',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    print(f'Verify Status Code: {verify_response.status_code}')
    print(f'Verify Response: {json.dumps(verify_response.json(), indent=2)}')
else:
    print("Refresh failed, cannot test verify-token")