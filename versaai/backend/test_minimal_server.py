#!/usr/bin/env python3
"""
Script para probar el servidor minimal de VersaAI
Prueba conectividad y contenido de endpoints clave
"""

import requests
import time
from urllib.parse import urljoin

def test_endpoint(base_url, endpoint, description):
    """Prueba un endpoint específico"""
    url = urljoin(base_url, endpoint)
    print(f"\n🔍 Probando {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Status: {response.status_code}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        # Verificar headers importantes
        content_type = response.headers.get('content-type', 'N/A')
        print(f"📄 Content-Type: {content_type}")
        
        # Para endpoints de documentación, verificar contenido específico
        if '/docs' in endpoint or '/redoc' in endpoint:
            content = response.text
            if 'swagger' in content.lower() or 'redoc' in content.lower() or 'openapi' in content.lower():
                print("✅ Contiene elementos de documentación API")
            else:
                print("⚠️  No se detectaron elementos de documentación")
                
            # Verificar si hay scripts/CSS
            if '<script' in content or '<link' in content:
                print("✅ Contiene recursos JavaScript/CSS")
            else:
                print("⚠️  No se detectaron recursos JavaScript/CSS")
        
        # Para JSON endpoints
        elif 'application/json' in content_type:
            try:
                json_data = response.json()
                print(f"✅ JSON válido con {len(json_data)} campos")
            except:
                print("⚠️  Respuesta no es JSON válido")
        
        return True
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 Iniciando pruebas del servidor minimal VersaAI")
    print("=" * 60)
    
    base_url = "http://localhost:8002"
    
    # Lista de endpoints a probar
    endpoints = [
        ("/", "Endpoint raíz"),
        ("/health", "Health check"),
        ("/api/docs", "Swagger UI"),
        ("/api/redoc", "ReDoc"),
        ("/api/openapi.json", "OpenAPI JSON")
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        success = test_endpoint(base_url, endpoint, description)
        results.append((endpoint, success))
        time.sleep(0.5)  # Pequeña pausa entre requests
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    successful = 0
    for endpoint, success in results:
        status = "✅ OK" if success else "❌ FAIL"
        print(f"{endpoint:<20} {status}")
        if success:
            successful += 1
    
    print(f"\n🎯 Éxito: {successful}/{len(results)} endpoints")
    
    if successful == len(results):
        print("\n🎉 ¡Todos los endpoints funcionan correctamente!")
        print("\n🌐 URLs disponibles:")
        print(f"   • Swagger UI: {base_url}/api/docs")
        print(f"   • ReDoc: {base_url}/api/redoc")
        print(f"   • Health: {base_url}/health")
    else:
        print(f"\n⚠️  {len(results) - successful} endpoints fallaron")
        print("\n🔧 Recomendaciones:")
        print("   • Verificar que el servidor esté ejecutándose")
        print("   • Revisar logs del servidor para errores")
        print("   • Verificar configuración de middlewares")

if __name__ == "__main__":
    main()