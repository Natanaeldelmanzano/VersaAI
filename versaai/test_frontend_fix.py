#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar si la corrección del frontend funciona correctamente
"""

import requests
import time
import sys

def test_frontend_availability():
    """Verifica si el frontend está disponible"""
    try:
        print("🌐 Verificando disponibilidad del frontend...")
        response = requests.get('http://localhost:3000/', timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend disponible en http://localhost:3000/")
            print(f"📄 Tamaño de respuesta: {len(response.text)} caracteres")
            
            # Verificar si la página contiene contenido esperado
            if 'VersaAI' in response.text:
                print("✅ La página contiene el título 'VersaAI'")
            else:
                print("⚠️ La página no contiene el título 'VersaAI'")
                
            if '<div id="app">' in response.text:
                print("✅ La página contiene el div principal de Vue")
            else:
                print("❌ La página no contiene el div principal de Vue")
                
            if len(response.text) < 1000:
                print("⚠️ La página parece muy pequeña, posible problema de carga")
                print("📝 Contenido de la página:")
                print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            else:
                print("✅ La página tiene un tamaño normal")
                
            return True
        else:
            print(f"❌ Frontend no disponible. Código de estado: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al frontend en http://localhost:3000/")
        return False
    except Exception as e:
        print(f"❌ Error al verificar frontend: {e}")
        return False

def test_backend_availability():
    """Verifica si el backend está disponible"""
    try:
        print("\n🔧 Verificando disponibilidad del backend...")
        response = requests.get('http://localhost:8000/api/v1/health', timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend disponible en http://localhost:8000/")
            return True
        else:
            print(f"❌ Backend no disponible. Código de estado: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend en http://localhost:8000/")
        return False
    except Exception as e:
        print(f"❌ Error al verificar backend: {e}")
        return False

def main():
    print("🔍 DIAGNÓSTICO DE CORRECCIÓN DEL FRONTEND")
    print("=" * 50)
    
    # Verificar backend
    backend_ok = test_backend_availability()
    
    # Verificar frontend
    frontend_ok = test_frontend_availability()
    
    print("\n📊 RESUMEN:")
    print(f"Backend: {'✅ OK' if backend_ok else '❌ ERROR'}")
    print(f"Frontend: {'✅ OK' if frontend_ok else '❌ ERROR'}")
    
    if frontend_ok and backend_ok:
        print("\n🎉 ¡Todo parece estar funcionando correctamente!")
        print("\n📝 INSTRUCCIONES PARA VERIFICAR:")
        print("1. Abre http://localhost:3000/ en tu navegador")
        print("2. Verifica que la página principal se carga correctamente")
        print("3. Abre las herramientas de desarrollador (F12)")
        print("4. Revisa la consola para ver si hay errores de JavaScript")
        print("5. Si ves errores, compártelos para más diagnóstico")
    else:
        print("\n⚠️ Hay problemas que necesitan ser resueltos")
        if not backend_ok:
            print("- El backend no está funcionando")
        if not frontend_ok:
            print("- El frontend no está funcionando correctamente")
    
    return 0 if (frontend_ok and backend_ok) else 1

if __name__ == '__main__':
    sys.exit(main())