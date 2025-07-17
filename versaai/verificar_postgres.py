#!/usr/bin/env python3
"""
Script simple para verificar PostgreSQL y continuar con el desarrollo
"""

import os
import subprocess
import sys
from pathlib import Path

def print_header(title):
    """Imprime un encabezado formateado"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def check_docker_postgres():
    """Verifica si PostgreSQL está ejecutándose en Docker"""
    print_header("VERIFICACIÓN DE POSTGRESQL EN DOCKER")
    
    try:
        # Verificar contenedores Docker
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if result.returncode == 0:
            containers = result.stdout
            print("📦 Contenedores Docker activos:")
            print(containers)
            
            if "postgres" in containers.lower():
                print("✅ PostgreSQL encontrado en Docker")
                return True
            else:
                print("❌ PostgreSQL no encontrado en contenedores activos")
                return False
        else:
            print("❌ Error ejecutando docker ps")
            return False
    except FileNotFoundError:
        print("❌ Docker no está instalado o no está en PATH")
        return False
    except Exception as e:
        print(f"❌ Error verificando Docker: {e}")
        return False

def check_env_file():
    """Verifica el archivo .env"""
    print_header("VERIFICACIÓN DE ARCHIVO .ENV")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Archivo .env encontrado")
        
        # Leer variables importantes
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        important_vars = ["GROQ_API_KEY", "SECRET_KEY", "DATABASE_URL"]
        for var in important_vars:
            if f"{var}=" in content and not f"{var}=\n" in content:
                print(f"✅ {var}: Configurada")
            else:
                print(f"⚠️  {var}: No configurada o vacía")
        
        return True
    else:
        print("❌ Archivo .env no encontrado")
        return False

def check_backend_status():
    """Verifica el estado del backend"""
    print_header("VERIFICACIÓN DEL BACKEND")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend activo en puerto 8000")
            print(f"📊 Respuesta: {response.json()}")
            return True
        else:
            print(f"⚠️  Backend responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend no está ejecutándose en puerto 8000")
        return False
    except ImportError:
        print("⚠️  Módulo requests no disponible")
        return False
    except Exception as e:
        print(f"❌ Error verificando backend: {e}")
        return False

def check_frontend_status():
    """Verifica el estado del frontend"""
    print_header("VERIFICACIÓN DEL FRONTEND")
    
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend activo en puerto 3000")
            return True
        else:
            print(f"⚠️  Frontend responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend no está ejecutándose en puerto 3000")
        return False
    except ImportError:
        print("⚠️  Módulo requests no disponible")
        return False
    except Exception as e:
        print(f"❌ Error verificando frontend: {e}")
        return False

def show_next_steps():
    """Muestra los próximos pasos del desarrollo"""
    print_header("PRÓXIMOS PASOS DEL DESARROLLO")
    
    print("🎯 Acciones Inmediatas:")
    print("   1. ✅ PostgreSQL configurado en Docker")
    print("   2. 🔄 Verificar conexión de base de datos")
    print("   3. 🔄 Implementar sistema de autenticación")
    print("   4. 🔄 Crear endpoints de usuarios")
    print("   5. 🔄 Integrar frontend con backend")
    
    print("\n📋 Comandos útiles:")
    print("   # Iniciar servicios Docker")
    print("   docker-compose up -d")
    
    print("   # Verificar logs de PostgreSQL")
    print("   docker logs <postgres_container_id>")
    
    print("   # Ejecutar migraciones")
    print("   cd backend && alembic upgrade head")
    
    print("   # Probar endpoints")
    print("   curl http://localhost:8000/api/health")
    
    print("\n🌐 URLs importantes:")
    print("   📖 API Docs: http://localhost:8000/docs")
    print("   🌐 Frontend: http://localhost:3000")
    print("   ⚡ Health Check: http://localhost:8000/api/health")

def main():
    """Función principal"""
    print("🚀 VersaAI - Verificación Rápida del Sistema")
    print("Continuando con el plan de desarrollo...")
    
    # Verificaciones básicas
    postgres_ok = check_docker_postgres()
    env_ok = check_env_file()
    backend_ok = check_backend_status()
    frontend_ok = check_frontend_status()
    
    # Mostrar próximos pasos
    show_next_steps()
    
    # Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DEL ESTADO:")
    print(f"   🗄️  PostgreSQL: {'✅ OK' if postgres_ok else '❌ Revisar'}")
    print(f"   ⚙️  Configuración: {'✅ OK' if env_ok else '❌ Revisar'}")
    print(f"   🔧 Backend: {'✅ OK' if backend_ok else '❌ Revisar'}")
    print(f"   🎨 Frontend: {'✅ OK' if frontend_ok else '❌ Revisar'}")
    
    if postgres_ok and env_ok:
        print("\n🎉 ¡Sistema listo para continuar el desarrollo!")
        print("📝 Consulta el PLAN_ACCIONES_DESARROLLO.md para los siguientes pasos")
    else:
        print("\n⚠️  Algunos componentes necesitan atención")
        print("🔧 Revisa las configuraciones antes de continuar")
    
    print("="*50)

if __name__ == "__main__":
    main()