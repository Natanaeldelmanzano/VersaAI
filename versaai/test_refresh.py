import requests
import json

# Test refresh token endpoint
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJhZG1pbkB2ZXJzYWFpLmNvbSIsInJvbGUiOiJ1c2VyIiwib3JnX2lkIjpudWxsLCJleHAiOjE3NTI5MDE1MTksInR5cGUiOiJyZWZyZXNoIn0.bolO6X5RffrkIGdGjhKRqOPEej5s3zdCG-nrM9TKDNY"

response = requests.post(
    'http://localhost:8000/api/v1/auth/refresh',
    json={'refresh_token': refresh_token}
)

print(f'Status Code: {response.status_code}')
print(f'Response: {json.dumps(response.json(), indent=2)}')