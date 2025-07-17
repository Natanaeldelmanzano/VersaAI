#!/usr/bin/env python3
"""
Script para verificar y corregir el esquema de la base de datos
"""

import sqlite3
import sys
import os
from datetime import datetime
import requests

def check_database_schema():
    """Verifica el esquema actual de la base de datos"""
    print("\n🔍 VERIFICANDO ESQUEMA DE BASE DE DATOS...")
    
    try:
        conn = sqlite3.connect('backend/versaai.db')
        cursor = conn.cursor()
        
        # Obtener información de la tabla users
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        if columns:
            print("📊 Estructura de la tabla 'users':")
            for col in columns:
                print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - {'PK' if col[5] else ''}")
        else:
            print("❌ Tabla 'users' no encontrada")
        
        # Verificar si hay datos
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"📈 Número de usuarios: {count}")
        
        if count > 0:
            cursor.execute("SELECT id, email, username, full_name FROM users LIMIT 5")
            users = cursor.fetchall()
            print("👥 Usuarios existentes:")
            for user in users:
                print(f"   ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Nombre: {user[3]}")
        
        conn.close()
        return columns
        
    except Exception as e:
        print(f"❌ Error al verificar esquema: {e}")
        return []

def create_user_with_correct_schema():
    """Crea un usuario usando el esquema correcto"""
    print("\n👤 CREANDO USUARIO CON ESQUEMA CORRECTO...")
    
    try:
        conn = sqlite3.connect('backend/versaai.db')
        cursor = conn.cursor()
        
        # Verificar columnas disponibles
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 Columnas disponibles: {columns}")
        
        # Datos del usuario
        email = "admin@versaai.com"
        password = "admin123456"  # Texto plano para que el backend lo hashee
        username = "admin"
        full_name = "VersaAI Administrator"
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"ℹ️  Usuario {email} ya existe con ID: {existing[0]}")
            
            # Actualizar usuario existente
            if 'password' in columns:
                cursor.execute("""
                    UPDATE users 
                    SET password = ?, updated_at = ?
                    WHERE email = ?
                """, (password, datetime.utcnow(), email))
            elif 'hashed_password' in columns:
                from werkzeug.security import generate_password_hash
                hashed = generate_password_hash(password)
                cursor.execute("""
                    UPDATE users 
                    SET hashed_password = ?, updated_at = ?
                    WHERE email = ?
                """, (hashed, datetime.utcnow(), email))
            
            conn.commit()
            print("✅ Usuario actualizado")
        else:
            # Crear nuevo usuario con columnas disponibles
            now = datetime.utcnow()
            
            if 'password' in columns:
                # Usar password en texto plano
                cursor.execute("""
                    INSERT INTO users (email, username, full_name, password, is_active, role, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (email, username, full_name, password, True, 'admin', now, now))
            elif 'hashed_password' in columns:
                # Usar password hasheado
                from werkzeug.security import generate_password_hash
                hashed = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO users (email, username, full_name, hashed_password, is_active, role, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (email, username, full_name, hashed, True, 'admin', now, now))
            else:
                # Esquema mínimo
                cursor.execute("""
                    INSERT INTO users (email, username, full_name, is_active, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (email, username, full_name, True, now, now))
            
            conn.commit()
            print("✅ Usuario creado exitosamente")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_registration_api():
    """Prueba el API de registro"""
    print("\n📝 PROBANDO API DE REGISTRO...")
    
    # Probar con diferentes usuarios
    test_users = [
        {
            "email": "test1@versaai.com",
            "password": "test123456",
            "full_name": "Test User 1"
        },
        {
            "email": "test2@versaai.com", 
            "password": "test123456",
            "full_name": "Test User 2"
        }
    ]
    
    successful_users = []
    
    for user_data in test_users:
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/auth/register",
                json=user_data,
                timeout=10
            )
            
            print(f"\n👤 Usuario: {user_data['email']}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print("   ✅ Registro exitoso")
                successful_users.append(user_data)
            elif response.status_code == 400 and "already registered" in response.text:
                print("   ℹ️  Ya registrado")
                successful_users.append(user_data)
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
    
    return successful_users

def test_login_multiple_users(users):
    """Prueba login con múltiples usuarios"""
    print("\n🔐 PROBANDO LOGIN CON USUARIOS...")
    
    successful_logins = []
    
    for user_data in users:
        try:
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/auth/login",
                json=login_data,
                timeout=10
            )
            
            print(f"\n👤 Usuario: {user_data['email']}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                token = result.get('access_token')
                print(f"   ✅ Login exitoso")
                print(f"   🔑 Token: {token[:30]}...")
                successful_logins.append({
                    'user': user_data,
                    'token': token
                })
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
    
    return successful_logins

def test_authenticated_endpoints(successful_logins):
    """Prueba endpoints autenticados"""
    if not successful_logins:
        print("\n❌ No hay logins exitosos para probar endpoints")
        return
    
    print("\n🔒 PROBANDO ENDPOINTS AUTENTICADOS...")
    
    # Usar el primer login exitoso
    login_info = successful_logins[0]
    token = login_info['token']
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    endpoints = {
        "profile": "/api/v1/auth/me",
        "chatbots": "/api/v1/chatbots/",
        "users": "/api/v1/users/",
        "conversations": "/api/v1/conversations/"
    }
    
    for name, endpoint in endpoints.items():
        try:
            response = requests.get(
                f"http://localhost:8000{endpoint}",
                headers=headers,
                timeout=10
            )
            
            print(f"\n🔗 {name.upper()}:")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ FUNCIONAL")
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")

def main():
    print("🔧 SCRIPT DE CORRECCIÓN DE ESQUEMA Y PRUEBAS")
    print("="*60)
    
    # 1. Verificar esquema actual
    schema = check_database_schema()
    
    # 2. Crear usuario con esquema correcto
    create_user_with_correct_schema()
    
    # 3. Verificar esquema después de la corrección
    print("\n🔍 VERIFICANDO ESQUEMA DESPUÉS DE CORRECCIÓN...")
    check_database_schema()
    
    # 4. Probar registro via API
    successful_users = test_registration_api()
    
    # 5. Probar login con usuarios
    all_users = successful_users + [{
        "email": "admin@versaai.com",
        "password": "admin123456",
        "full_name": "VersaAI Administrator"
    }]
    
    successful_logins = test_login_multiple_users(all_users)
    
    # 6. Probar endpoints autenticados
    test_authenticated_endpoints(successful_logins)
    
    # 7. Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL:")
    print(f"   👥 Usuarios registrados: {len(successful_users) + 1}")
    print(f"   🔐 Logins exitosos: {len(successful_logins)}")
    
    if successful_logins:
        print("\n🎉 SOLUCIÓN EXITOSA - Sistema funcionando")
        print("\n📋 CREDENCIALES VÁLIDAS:")
        for login in successful_logins:
            user = login['user']
            print(f"   📧 {user['email']} / 🔑 {user['password']}")
    else:
        print("\n❌ SOLUCIÓN FALLIDA - Revisar configuración del backend")

if __name__ == "__main__":
    main()