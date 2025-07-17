#!/usr/bin/env python3
"""
Servidor temporal para endpoints de autenticación
Mientras se resuelven los problemas del servidor principal
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import json
from datetime import datetime, timedelta
import jwt
import secrets

app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo

# Configuración temporal
SECRET_KEY = "temp_secret_key_for_development_only"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict, expires_delta: timedelta = None) -> str:
    """Crear un JWT token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error creating token: {e}")
        return f"temp_token_{int(time.time())}"

def verify_token(token: str) -> dict:
    """Verificar un JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
    except Exception:
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "temp_auth_server",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/auth/refresh', methods=['POST'])
def refresh_token():
    """Endpoint de refresh token temporal"""
    try:
        # Obtener datos de la request
        data = request.get_json() if request.is_json else {}
        
        # Para desarrollo, generar tokens válidos para cualquier request
        user_data = {
            "sub": "temp_user_123",
            "email": "temp@example.com",
            "role": "user",
            "username": "temp_user"
        }
        
        # Crear nuevos tokens
        access_token = create_token(user_data)
        refresh_token = create_token(
            {**user_data, "type": "refresh"}, 
            timedelta(days=7)
        )
        
        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
        print(f"[{datetime.now()}] Refresh token generated successfully")
        return jsonify(response)
        
    except Exception as e:
        print(f"[{datetime.now()}] Error in refresh endpoint: {e}")
        return jsonify({
            "detail": "Token refresh failed",
            "error": str(e)
        }), 500

@app.route('/api/v1/auth/verify-token', methods=['POST'])
def verify_token_endpoint():
    """Endpoint de verificación de token"""
    try:
        # Obtener token del header Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"detail": "Missing or invalid authorization header"}), 401
        
        token = auth_header.split(' ')[1]
        
        # Verificar token
        payload = verify_token(token)
        
        if not payload:
            return jsonify({"detail": "Invalid or expired token"}), 401
        
        response = {
            "valid": True,
            "user_id": payload.get("sub", "temp_user_123"),
            "username": payload.get("username", "temp_user"),
            "email": payload.get("email", "temp@example.com"),
            "role": payload.get("role", "user"),
            "is_active": True
        }
        
        print(f"[{datetime.now()}] Token verified successfully")
        return jsonify(response)
        
    except Exception as e:
        print(f"[{datetime.now()}] Error in verify endpoint: {e}")
        return jsonify({
            "detail": "Token verification failed",
            "error": str(e)
        }), 500

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Endpoint de login temporal"""
    try:
        data = request.get_json() if request.is_json else {}
        
        # Para desarrollo, aceptar cualquier credencial
        user_data = {
            "sub": "temp_user_123",
            "email": data.get("email", "temp@example.com"),
            "role": "user",
            "username": data.get("email", "temp@example.com").split('@')[0]
        }
        
        # Crear tokens
        access_token = create_token(user_data)
        refresh_token = create_token(
            {**user_data, "type": "refresh"}, 
            timedelta(days=7)
        )
        
        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": "temp_user_123",
                "email": user_data["email"],
                "username": user_data["username"],
                "role": "user",
                "is_active": True
            }
        }
        
        print(f"[{datetime.now()}] Login successful for {user_data['email']}")
        return jsonify(response)
        
    except Exception as e:
        print(f"[{datetime.now()}] Error in login endpoint: {e}")
        return jsonify({
            "detail": "Login failed",
            "error": str(e)
        }), 500

@app.route('/api/v1/auth/test-simple', methods=['GET'])
def test_simple():
    """Endpoint de prueba simple"""
    return jsonify({
        "message": "Temp auth server is working!",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"detail": "Not Found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"detail": "Internal Server Error"}), 500

if __name__ == '__main__':
    print("=== Servidor Temporal de Autenticación ===")
    print("Puerto: 8001")
    print("Endpoints disponibles:")
    print("  GET  /health")
    print("  POST /api/v1/auth/login")
    print("  POST /api/v1/auth/refresh")
    print("  POST /api/v1/auth/verify-token")
    print("  GET  /api/v1/auth/test-simple")
    print("\nPara usar en el frontend, cambiar la URL base a: http://localhost:8001")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("="*50)
    
    app.run(host='0.0.0.0', port=8001, debug=True)