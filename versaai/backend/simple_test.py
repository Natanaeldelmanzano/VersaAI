#!/usr/bin/env python3
"""
Script simple para probar la conectividad del servidor
"""

import requests
import time

def test_basic_connectivity():
    """Probar conectividad básica del servidor"""
    print("🔍 PRUEBA DE CONECTIVIDAD BÁSICA")
    print("="*50)
    
    base_url = "http://localhost:8000"
    
    # Probar endpoints básicos
    endpoints = [
        "/",
        "/health",
        "/api/docs",
        "/api/redoc",
        "/api/openapi.json"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n🌐 Probando: {url}")
        
        try:
            # Usar timeout más corto y headers específicos
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, timeout=5, headers=headers)
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📏 Content-Length: {len(response.content)} bytes")
            print(f"   🕒 Response Time: {response.elapsed.total_seconds():.3f}s")
            
            # Mostrar headers de respuesta importantes
            important_headers = ['content-type', 'content-length', 'server']
            for header in important_headers:
                if header in response.headers:
                    print(f"   📋 {header.title()}: {response.headers[header]}")
            
            # Mostrar una muestra del contenido
            if response.text:
                content_sample = response.text[:200].replace('\n', ' ').replace('\r', '')
                print(f"   📄 Content Sample: {content_sample}...")
            else:
                print(f"   ⚠️  No content received")
                
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Connection Error: {str(e)}")
        except requests.exceptions.Timeout as e:
            print(f"   ⏰ Timeout Error: {str(e)}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request Error: {str(e)}")
        except Exception as e:
            print(f"   ❌ Unexpected Error: {str(e)}")
        
        # Pequeña pausa entre requests
        time.sleep(0.5)
    
    print(f"\n📊 RESUMEN:")
    print(f"Si todos los endpoints fallan con Connection Error,")
    print(f"el problema está en el servidor o la configuración de red.")
    print(f"Si solo /api/docs y /api/redoc fallan, el problema está")
    print(f"en la configuración de FastAPI para la documentación.")

if __name__ == "__main__":
    test_basic_connectivity()