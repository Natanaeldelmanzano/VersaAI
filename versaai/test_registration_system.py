#!/usr/bin/env python3
"""
Script para probar el sistema de registro de usuarios de VersaAI
"""

import requests
import json
from datetime import datetime
import sys

# Configuración
BASE_URL = 'http://localhost:8000/api/v1'

def print_header(title):
    """Imprime un encabezado formateado"""
    print('\n' + '=' * 60)
    print(f'🚀 {title}')
    print('=' * 60)

def print_success(message):
    """Imprime un mensaje de éxito"""
    print(f'✅ {message}')

def print_error(message):
    """Imprime un mensaje de error"""
    print(f'❌ {message}')

def print_info(message):
    """Imprime un mensaje informativo"""
    print(f'ℹ️  {message}')

def test_registration():
    """Prueba el sistema de registro"""
    print_header('PRUEBA DEL SISTEMA DE REGISTRO')
    
    # Generar datos únicos para el usuario
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    user_data = {
        'email': f'test_{timestamp}@versaai.com',
        'password': 'TestPassword123!',
        'full_name': 'Usuario de Prueba VersaAI'
    }
    
    print_info(f'Email: {user_data["email"]}')
    print_info(f'Nombre: {user_data["full_name"]}')
    print_info(f'Password: {user_data["password"]}')
    
    try:
        # Probar registro
        print('\n📝 Registrando usuario...')
        response = requests.post(
            f'{BASE_URL}/auth/register', 
            json=user_data, 
            timeout=10
        )
        
        print(f'Status Code: {response.status_code}')
        
        if response.status_code == 201:
            result = response.json()
            print_success('Registro exitoso!')
            
            # Mostrar información del usuario creado
            # La respuesta contiene los datos del usuario directamente, no en un campo 'user'
            print(f'🆔 User ID: {result.get("id", "N/A")}')
            print(f'📧 Email: {result.get("email", "N/A")}')
            print(f'👤 Nombre: {result.get("full_name", "N/A")}')
            
            # Mostrar tokens
            access_token = result.get('access_token', '')
            refresh_token = result.get('refresh_token', '')
            print(f'🔑 Access Token: {access_token[:50]}...')
            print(f'🔄 Refresh Token: {refresh_token[:50]}...')
            
            return user_data, access_token
            
        else:
            print_error(f'Error en registro: {response.status_code}')
            try:
                error_detail = response.json()
                print(f'Detalle del error: {json.dumps(error_detail, indent=2)}')
            except:
                print(f'Respuesta del servidor: {response.text}')
            return None, None
            
    except requests.exceptions.ConnectionError:
        print_error('No se pudo conectar al servidor. ¿Está el backend ejecutándose?')
        return None, None
    except Exception as e:
        print_error(f'Error inesperado: {str(e)}')
        return None, None

def test_login(user_data):
    """Prueba el sistema de login"""
    print_header('PRUEBA DEL SISTEMA DE LOGIN')
    
    if not user_data:
        print_error('No hay datos de usuario para probar login')
        return None
    
    login_data = {
        'email': user_data['email'],
        'password': user_data['password']
    }
    
    try:
        print('🔐 Iniciando sesión...')
        response = requests.post(
            f'{BASE_URL}/auth/login',
            json=login_data,
            timeout=10
        )
        
        print(f'Status Code: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print_success('Login exitoso!')
            
            access_token = result.get('access_token', '')
            refresh_token = result.get('refresh_token', '')
            print(f'🔑 Access Token: {access_token[:50]}...')
            print(f'🔄 Refresh Token: {refresh_token[:50]}...')
            print(f'⏰ Token Type: {result.get("token_type", "N/A")}')
            
            return access_token
            
        else:
            print_error(f'Error en login: {response.status_code}')
            try:
                error_detail = response.json()
                print(f'Detalle del error: {json.dumps(error_detail, indent=2)}')
            except:
                print(f'Respuesta del servidor: {response.text}')
            return None
            
    except Exception as e:
        print_error(f'Error en login: {str(e)}')
        return None

def test_token_verification(access_token):
    """Prueba la verificación de token"""
    print_header('PRUEBA DE VERIFICACIÓN DE TOKEN')
    
    if not access_token:
        print_error('No hay token para verificar')
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        print('🔍 Verificando token...')
        response = requests.get(
            f'{BASE_URL}/auth/me',
            headers=headers,
            timeout=10
        )
        
        print(f'Status Code: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print_success('Token válido!')
            print(f'🆔 User ID: {result.get("id", "N/A")}')
            print(f'📧 Email: {result.get("email", "N/A")}')
            print(f'👤 Nombre: {result.get("full_name", "N/A")}')
            return True
            
        else:
            print_error(f'Token inválido: {response.status_code}')
            return False
            
    except Exception as e:
        print_error(f'Error en verificación: {str(e)}')
        return False

def main():
    """Función principal"""
    print_header('SISTEMA DE PRUEBAS DE AUTENTICACIÓN VERSAAI')
    
    # Probar registro
    user_data, access_token = test_registration()
    
    login_success = False
    token_verification_success = False
    
    if user_data:
        # Probar login
        login_token = test_login(user_data)
        
        if login_token:
            login_success = True
            # Probar verificación de token
            token_verification_success = test_token_verification(login_token)
    
    print_header('PRUEBAS COMPLETADAS')
    
    # Determinar el estado de cada prueba
    registration_success = user_data is not None and access_token is not None
    
    print(f"\n📊 RESUMEN DE RESULTADOS:")
    print(f"   Registro: {'✅ Exitoso' if registration_success else '❌ Fallido'}")
    print(f"   Login: {'✅ Exitoso' if login_success else '❌ Fallido'}")
    print(f"   Verificación de Token: {'✅ Exitoso' if token_verification_success else '❌ Fallido'}")
    
    if registration_success and login_success and token_verification_success:
        print("\n🎉 ¡SISTEMA DE AUTENTICACIÓN FUNCIONANDO PERFECTAMENTE!")
        print("✅ Todas las pruebas pasaron exitosamente.")
        print("🚀 El sistema de registro de usuarios está operativo.")
        print_info('🎉 ¡VersaAI está listo para usar!')
    else:
        print_error('Hay problemas con el sistema de autenticación.')
        print_info('Revisa los logs del servidor para más detalles.')

if __name__ == '__main__':
    main()