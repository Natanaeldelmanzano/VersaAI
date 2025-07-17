#!/usr/bin/env python3
"""
Script principal para iniciar el sistema completo de VersaAI en modo demo
Conecta la documentación multi-usuario con el backend y frontend
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Muestra el banner principal del sistema"""
    print("\n" + "="*80)
    print("🚀 VersaAI - Sistema Completo Demo Multi-Usuario")
    print("="*80)
    print("📋 Este script inicia el sistema completo con documentación integrada")
    print("📚 Basado en: INSTRUCCIONES_MULTI_USUARIO.md y demo-mode-documentation.html")
    print("="*80)

def check_documentation():
    """Verifica que la documentación esté disponible"""
    base_path = Path(__file__).parent / "versaai"
    
    docs = {
        "INSTRUCCIONES_MULTI_USUARIO.md": base_path / "INSTRUCCIONES_MULTI_USUARIO.md",
        "demo-mode-documentation.html": base_path / "demo-mode-documentation.html"
    }
    
    print("📚 Verificando documentación disponible:")
    for name, path in docs.items():
        if path.exists():
            print(f"   ✅ {name} - Disponible")
        else:
            print(f"   ❌ {name} - No encontrado en {path}")
    
    return all(path.exists() for path in docs.values())

def show_demo_credentials():
    """Muestra las credenciales de los usuarios demo"""
    print("\n🔐 CREDENCIALES DE USUARIOS DEMO:")
    print("-" * 50)
    
    users = [
        ("🔴 Super Administrador", "superadmin@versaai.com", "super123456", "Acceso completo al sistema"),
        ("🟠 Admin de Organización", "admin@versaai.com", "admin123456", "Gestión de organización y usuarios"),
        ("🟢 Usuario Estándar", "user@versaai.com", "user123456", "Acceso a funciones básicas"),
        ("🔵 Visualizador", "viewer@versaai.com", "viewer123456", "Solo lectura"),
        ("🟡 Usuario Demo", "demo@versaai.com", "demo123456", "Usuario adicional")
    ]
    
    for role, email, password, description in users:
        print(f"{role}")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Contraseña: {password}")
        print(f"   📝 {description}")
        print()

def show_access_urls():
    """Muestra las URLs de acceso al sistema"""
    print("🌐 URLS DE ACCESO:")
    print("-" * 30)
    print("   🎯 Frontend Principal: http://localhost:3000")
    print("   🔧 Backend API: http://localhost:8000")
    print("   📚 Documentación API: http://localhost:8000/api/docs")
    print("   📖 ReDoc API: http://localhost:8000/api/redoc")
    print()

def show_features():
    """Muestra las características principales del sistema"""
    print("⚡ CARACTERÍSTICAS PRINCIPALES:")
    print("-" * 40)
    print("   🔄 Cambio de roles en tiempo real con RoleSwitcher")
    print("   👥 Sistema completo de gestión de usuarios")
    print("   🔐 Autenticación JWT real con diferentes permisos")
    print("   📊 Dashboard adaptativo según rol")
    print("   🛡️ Sistema granular de permisos")
    print("   🤖 Gestión de chatbots empresariales")
    print("   💬 Sistema de conversaciones")
    print("   📈 Analíticas y métricas")
    print()

def start_backend():
    """Inicia el servidor backend"""
    print("🚀 Iniciando servidor backend...")
    backend_path = Path(__file__).parent / "versaai" / "backend"
    
    if not backend_path.exists():
        print(f"❌ No se encontró el directorio backend en {backend_path}")
        return False
    
    try:
        # Cambiar al directorio del backend
        os.chdir(backend_path)
        
        # Ejecutar el servidor
        subprocess.Popen([
            sys.executable, "start_server.py"
        ])
        
        print("✅ Servidor backend iniciado en http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Error al iniciar backend: {e}")
        return False

def start_frontend():
    """Inicia el servidor frontend"""
    print("🎨 Iniciando servidor frontend...")
    frontend_path = Path(__file__).parent / "versaai" / "frontend"
    
    if not frontend_path.exists():
        print(f"❌ No se encontró el directorio frontend en {frontend_path}")
        return False
    
    try:
        # Cambiar al directorio del frontend
        os.chdir(frontend_path)
        
        # Ejecutar el servidor
        subprocess.Popen([
            "npm", "run", "dev"
        ])
        
        print("✅ Servidor frontend iniciado en http://localhost:3000")
        return True
    except Exception as e:
        print(f"❌ Error al iniciar frontend: {e}")
        return False

def open_documentation():
    """Abre la documentación en el navegador"""
    print("📖 Abriendo documentación...")
    
    base_path = Path(__file__).parent / "versaai"
    demo_doc = base_path / "demo-mode-documentation.html"
    
    if demo_doc.exists():
        try:
            webbrowser.open(f"file://{demo_doc.absolute()}")
            print("✅ Documentación abierta en el navegador")
        except Exception as e:
            print(f"❌ Error al abrir documentación: {e}")
    else:
        print("❌ Archivo de documentación no encontrado")

def main():
    """Función principal"""
    print_banner()
    
    # Verificar documentación
    if not check_documentation():
        print("⚠️  Algunos archivos de documentación no están disponibles")
        print("   El sistema funcionará, pero la documentación puede estar incompleta")
    
    print("\n🔧 CONFIGURACIÓN DEL SISTEMA:")
    print("-" * 40)
    
    # Mostrar información del sistema
    show_demo_credentials()
    show_access_urls()
    show_features()
    
    print("🚀 INICIANDO SERVICIOS:")
    print("-" * 30)
    
    # Preguntar si iniciar servicios
    response = input("¿Desea iniciar el backend y frontend automáticamente? (s/n): ")
    
    if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        # Iniciar backend
        if start_backend():
            print("⏳ Esperando que el backend se inicie...")
            time.sleep(3)
        
        # Iniciar frontend
        if start_frontend():
            print("⏳ Esperando que el frontend se inicie...")
            time.sleep(5)
        
        # Abrir documentación
        doc_response = input("\n¿Desea abrir la documentación en el navegador? (s/n): ")
        if doc_response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            open_documentation()
        
        # Abrir aplicación
        app_response = input("¿Desea abrir la aplicación en el navegador? (s/n): ")
        if app_response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            time.sleep(2)
            try:
                webbrowser.open("http://localhost:3000")
                print("✅ Aplicación abierta en el navegador")
            except Exception as e:
                print(f"❌ Error al abrir aplicación: {e}")
    
    print("\n" + "="*80)
    print("🎉 SISTEMA DEMO MULTI-USUARIO LISTO")
    print("="*80)
    print("📋 Para usar el sistema:")
    print("   1. Accede a http://localhost:3000")
    print("   2. Inicia sesión con cualquiera de las credenciales mostradas")
    print("   3. Usa el RoleSwitcher para cambiar entre roles")
    print("   4. Explora las diferentes funcionalidades según el rol")
    print("\n📚 Consulta la documentación para más detalles:")
    print("   📄 INSTRUCCIONES_MULTI_USUARIO.md")
    print("   🌐 demo-mode-documentation.html")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)