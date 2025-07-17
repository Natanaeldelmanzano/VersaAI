#!/usr/bin/env python3
"""
Script simple para verificar el estado del sistema VersaAI
"""

import requests
import sys

def verificar_backend():
    """Verifica si el backend está activo"""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend activo en puerto 8000")
            return True
        else:
            print(f"❌ Backend responde con código: {response.status_code}")
            return False
    except:
        print("❌ Backend no disponible")
        return False

def verificar_frontend():
    """Verifica si el frontend está activo"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend activo en puerto 3000")
            return True
        else:
            print(f"❌ Frontend responde con código: {response.status_code}")
            return False
    except:
        print("❌ Frontend no disponible")
        return False

def main():
    print("🚀 VersaAI - Estado del Sistema")
    print("=" * 40)
    
    backend_ok = verificar_backend()
    frontend_ok = verificar_frontend()
    
    print("\n📋 Próximas acciones:")
    if backend_ok and frontend_ok:
        print("1. ✅ Sistema base funcionando")
        print("2. 🔧 Implementar CRUD de usuarios")
        print("3. 🏢 Sistema de organizaciones")
        print("4. 🤖 Motor de chatbots")
        print("5. 💬 Interface de chat")
    else:
        if not backend_ok:
            print("1. ❌ Iniciar backend: cd backend && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        if not frontend_ok:
            print("2. ❌ Iniciar frontend: cd frontend && npm run dev")
    
    print("\n🌐 URLs:")
    print("   📖 API Docs: http://localhost:8000/docs")
    print("   🌐 Frontend: http://localhost:3000")
    print("   ⚡ Health: http://localhost:8000/api/health")

if __name__ == "__main__":
    main()