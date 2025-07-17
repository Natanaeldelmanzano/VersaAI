#!/usr/bin/env python3
"""
Script para verificar el estado de los endpoints de autenticación de VersaAI
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Verificar que el servidor esté funcionando"""
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_register():
    """Probar endpoint de registro"""
    try:
        data = {
            "email": "test@versaai.com",
            "password": "testpass123",
            "full_name": "Test User VersaAI"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        print(f"\n📝 Register Test:")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 201:
            print("   ✅ Registration successful")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("   ⚠️  User already exists (expected)")
            return True
        else:
            print("   ❌ Registration failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Register Test Failed: {e}")
        return False

def test_login():
    """Probar endpoint de login"""
    try:
        data = {
            "email": "test@versaai.com",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        print(f"\n🔐 Login Test:")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Login successful")
            print(f"   Token type: {result.get('token_type')}")
            print(f"   Access token: {result.get('access_token', '')[:50]}...")
            return result.get('access_token')
        else:
            print(f"   ❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Login Test Failed: {e}")
        return None

def test_protected_endpoint(token):
    """Probar endpoint protegido"""
    if not token:
        print("\n🔒 Protected Endpoint Test: Skipped (no token)")
        return False
        
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        
        print(f"\n🔒 Protected Endpoint Test:")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Protected endpoint accessible")
            user_data = response.json()
            print(f"   User: {user_data.get('email', 'N/A')}")
            return True
        else:
            print(f"   ❌ Protected endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Protected Endpoint Test Failed: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 VersaAI Authentication Status Check")
    print("=" * 50)
    
    # Test 1: Health Check
    if not test_health():
        print("\n❌ Server not responding. Please start the backend server.")
        sys.exit(1)
    
    # Test 2: Register
    register_success = test_register()
    
    # Test 3: Login
    token = test_login()
    
    # Test 4: Protected endpoint
    protected_success = test_protected_endpoint(token)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"   Health Check: ✅")
    print(f"   Registration: {'✅' if register_success else '❌'}")
    print(f"   Login: {'✅' if token else '❌'}")
    print(f"   Protected Access: {'✅' if protected_success else '❌'}")
    
    if register_success and token and protected_success:
        print("\n🎉 All authentication tests passed!")
        print("\n📋 Next Steps:")
        print("   1. ✅ Authentication system is working")
        print("   2. 🔄 Continue with frontend integration")
        print("   3. 🧪 Implement comprehensive testing")
        print("   4. 🤖 Start chatbot functionality development")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()