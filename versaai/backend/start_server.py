#!/usr/bin/env python3
"""
Script para iniciar el servidor FastAPI de VersaAI
Inicia el backend con modo demo multi-usuario integrado
"""

import sys
import os
import subprocess

# Agregar el directorio actual al PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_demo_info():
    """Muestra información sobre el modo demo multi-usuario"""
    print("\n" + "="*60)
    print("🚀 VersaAI Backend - Modo Demo Multi-Usuario")
    print("="*60)
    print("📋 Usuarios demo disponibles:")
    print("   🔴 Super Admin: superadmin@versaai.com / super123456")
    print("   🟠 Org Admin:   admin@versaai.com / admin123456")
    print("   🟢 Usuario:     user@versaai.com / user123456")
    print("   🔵 Viewer:      viewer@versaai.com / viewer123456")
    print("   🟡 Demo:        demo@versaai.com / demo123456")
    print("\n📚 Documentación:")
    print("   📄 INSTRUCCIONES_MULTI_USUARIO.md")
    print("   🌐 demo-mode-documentation.html")
    print("\n🌐 URLs de acceso:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
    print("   API Docs: http://localhost:8000/api/docs")
    print("="*60)
    print("🎯 El sistema creará automáticamente los usuarios demo al iniciar")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        # Mostrar información del modo demo
        print_demo_info()
        
        # Ejecutar uvicorn con el módulo correcto
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
        print("📋 Los usuarios demo permanecen en la base de datos para el próximo inicio")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)