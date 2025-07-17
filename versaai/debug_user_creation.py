#!/usr/bin/env python3
"""
Script para debuggear y crear usuarios en VersaAI
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime

def check_database_users():
    """Verifica usuarios existentes en la base de datos"""
    print("\n🔍 VERIFICANDO USUARIOS EN BASE DE DATOS...")
    
    try:
        # Conectar a la base de datos SQLite
        engine = create_engine('sqlite:///backend/versaai.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Consultar usuarios
        result = session.execute(text("SELECT id, email, username, full_name, is_active, created_at FROM users"))
        users = result.fetchall()
        
        if users:
            print(f"📊 Encontrados {len(users)} usuarios:")
            for user in users:
                print(f"   ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Nombre: {user[3]}, Activo: {user[4]}")
        else:
            print("❌ No se encontraron usuarios en la base de datos")
        
        session.close()
        return users
        
    except Exception as e:
        print(f"❌ Error al verificar base de datos: {e}")
        return []

def create_user_direct():
    """Crea un usuario directamente en la base de datos"""
    print("\n👤 CREANDO USUARIO DIRECTAMENTE EN BD...")
    
    try:
        from werkzeug.security import generate_password_hash
        from sqlalchemy import create_engine, text
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine('sqlite:///backend/versaai.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Datos del usuario
        email = "admin@versaai.com"
        password = "admin123456"
        username = "admin"
        full_name = "VersaAI Administrator"
        
        # Hash de la contraseña
        password_hash = generate_password_hash(password)
        
        # Verificar si el usuario ya existe
        existing = session.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email}).fetchone()
        
        if existing:
            print(f"ℹ️  Usuario {email} ya existe con ID: {existing[0]}")
            # Actualizar contraseña
            session.execute(text("""
                UPDATE users 
                SET password_hash = :password_hash, updated_at = :updated_at
                WHERE email = :email
            """), {
                "password_hash": password_hash,
                "updated_at": datetime.utcnow(),
                "email": email
            })
            session.commit()
            print("✅ Contraseña actualizada")
        else:
            # Crear nuevo usuario
            session.execute(text("""
                INSERT INTO users (email, username, full_name, password_hash, is_active, role, created_at, updated_at)
                VALUES (:email, :username, :full_name, :password_hash, :is_active, :role, :created_at, :updated_at)
            """), {
                "email": email,
                "username": username,
                "full_name": full_name,
                "password_hash": password_hash,
                "is_active": True,
                "role": "admin",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            session.commit()
            print("✅ Usuario creado exitosamente")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_login_with_created_user():
    """Prueba el login con el usuario creado"""
    print("\n🔐 PROBANDO LOGIN CON USUARIO CREADO...")
    
    login_data = {
        "email": "admin@versaai.com",
        "password": "admin123456"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login exitoso")
            print(f"   Token: {result.get('access_token', 'N/A')[:50]}...")
            return result.get('access_token')
        else:
            print("❌ Login falló")
            return None
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_register_endpoint():
    """Prueba el endpoint de registro"""
    print("\n📝 PROBANDO ENDPOINT DE REGISTRO...")
    
    register_data = {
        "email": "test@versaai.com",
        "password": "test123456",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/register",
            json=register_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Registro exitoso")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("ℹ️  Usuario ya registrado")
            return True
        else:
            print("❌ Registro falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return False

def main():
    print("🔧 SCRIPT DE DEBUG Y CREACIÓN DE USUARIOS")
    print("="*50)
    
    # 1. Verificar usuarios existentes
    users = check_database_users()
    
    # 2. Crear usuario directamente si es necesario
    if not users:
        print("\n⚠️  No hay usuarios, creando uno...")
        create_user_direct()
    else:
        print("\n🔄 Actualizando contraseña del usuario existente...")
        create_user_direct()
    
    # 3. Verificar usuarios después de la creación
    print("\n🔍 VERIFICANDO USUARIOS DESPUÉS DE LA CREACIÓN...")
    check_database_users()
    
    # 4. Probar registro via API
    test_register_endpoint()
    
    # 5. Probar login
    token = test_login_with_created_user()
    
    if token:
        print("\n🎉 SOLUCIÓN EXITOSA - Usuario creado y login funcional")
        print(f"\n📋 CREDENCIALES DE PRUEBA:")
        print(f"   Email: admin@versaai.com")
        print(f"   Password: admin123456")
    else:
        print("\n❌ SOLUCIÓN FALLIDA - Revisar configuración")

if __name__ == "__main__":
    main()