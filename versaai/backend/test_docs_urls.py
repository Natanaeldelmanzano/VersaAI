#!/usr/bin/env python3
"""
Script para probar las URLs de documentación del backend VersaAI
"""

import requests
import json
import sys
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"

def test_url(url, description, expected_content=None):
    """Probar una URL específica"""
    print(f"\n🔍 Probando {description}...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'No especificado')}")
        print(f"Content-Length: {len(response.text)} caracteres")
        
        if response.status_code == 200:
            if expected_content:
                if any(content.lower() in response.text.lower() for content in expected_content):
                    print(f"✅ {description} - Contenido válido encontrado")
                    return True
                else:
                    print(f"⚠️ {description} - Respuesta OK pero contenido inesperado")
                    print(f"Primeros 200 caracteres: {response.text[:200]}...")
                    return False
            else:
                print(f"✅ {description} - Respuesta OK")
                return True
        else:
            print(f"❌ {description} - Error {response.status_code}")
            print(f"Respuesta: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {description} - Error de conexión (servidor no disponible)")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {description} - Timeout")
        return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def test_json_endpoint(url, description):
    """Probar un endpoint que devuelve JSON"""
    print(f"\n🔍 Probando {description}...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'No especificado')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ {description} - JSON válido")
                print(f"Contenido: {json.dumps(data, indent=2)[:300]}...")
                return True
            except json.JSONDecodeError:
                print(f"⚠️ {description} - Respuesta OK pero no es JSON válido")
                print(f"Contenido: {response.text[:200]}...")
                return False
        else:
            print(f"❌ {description} - Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def main():
    print("🚀 Iniciando pruebas de URLs de documentación del backend VersaAI")
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    # Lista de URLs a probar
    tests = [
        # Endpoints básicos
        (f"{BASE_URL}/", "Root endpoint", None, test_json_endpoint),
        (f"{BASE_URL}/health", "Health check", None, test_json_endpoint),
        (f"{BASE_URL}/api/health/", "API Health check", None, test_json_endpoint),
        
        # URLs de documentación
        (f"{BASE_URL}/api/docs", "Swagger UI", ["swagger", "openapi", "redoc"], test_url),
        (f"{BASE_URL}/api/redoc", "ReDoc", ["redoc", "openapi"], test_url),
        (f"{BASE_URL}/openapi.json", "OpenAPI JSON", None, test_json_endpoint),
    ]
    
    results = []
    
    for test_data in tests:
        if len(test_data) == 4:
            url, description, expected_content, test_func = test_data
            if test_func == test_url:
                result = test_func(url, description, expected_content)
            else:
                result = test_func(url, description)
        else:
            url, description, expected_content = test_data
            result = test_url(url, description, expected_content)
        
        results.append((description, result))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for description, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {description}")
        if result:
            passed += 1
    
    print(f"\n📈 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El backend está funcionando correctamente.")
        return 0
    elif passed > 0:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración del servidor.")
        return 1
    else:
        print("🚨 Todas las pruebas fallaron. El servidor puede no estar funcionando.")
        return 2

if __name__ == "__main__":
    sys.exit(main())