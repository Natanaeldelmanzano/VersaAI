#!/usr/bin/env python3
"""
Script para probar el servidor simplificado
"""

import requests
import time

def test_simple_server():
    """Probar el servidor simplificado"""
    print("🔍 PROBANDO SERVIDOR SIMPLIFICADO")
    print("="*50)
    
    base_url = "http://localhost:8001"
    
    # Probar endpoints
    endpoints = [
        "/",
        "/health",
        "/test",
        "/api/docs",
        "/api/redoc",
        "/openapi.json"
    ]
    
    success_count = 0
    total_count = len(endpoints)
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n🌐 Probando: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Status: {response.status_code} OK")
                print(f"   📏 Content-Length: {len(response.content)} bytes")
                print(f"   🕒 Response Time: {response.elapsed.total_seconds():.3f}s")
                
                # Verificar content-type
                content_type = response.headers.get('content-type', 'unknown')
                print(f"   📋 Content-Type: {content_type}")
                
                # Para endpoints de documentación, verificar contenido HTML
                if endpoint in ["/api/docs", "/api/redoc"]:
                    if 'text/html' in content_type and len(response.content) > 1000:
                        print(f"   ✅ Documentación HTML válida")
                    else:
                        print(f"   ⚠️  Posible problema con documentación")
                
                # Para OpenAPI JSON, verificar JSON válido
                elif endpoint == "/openapi.json":
                    if 'application/json' in content_type:
                        try:
                            json_data = response.json()
                            print(f"   ✅ JSON válido con {len(json_data)} campos")
                        except:
                            print(f"   ⚠️  JSON inválido")
                    else:
                        print(f"   ⚠️  Content-Type no es JSON")
                
                success_count += 1
                
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Connection Error: {str(e)}")
        except requests.exceptions.Timeout as e:
            print(f"   ⏰ Timeout Error: {str(e)}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        time.sleep(0.5)
    
    print(f"\n📊 RESUMEN DEL SERVIDOR SIMPLIFICADO:")
    print(f"   ✅ Exitosos: {success_count}/{total_count}")
    print(f"   ❌ Fallidos: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print(f"\n🎉 ¡SERVIDOR SIMPLIFICADO FUNCIONA PERFECTAMENTE!")
        print(f"   El problema está en los middlewares del servidor principal.")
        print(f"   Recomendación: Revisar y deshabilitar middlewares uno por uno.")
    elif success_count > 0:
        print(f"\n⚠️  SERVIDOR SIMPLIFICADO FUNCIONA PARCIALMENTE")
        print(f"   Algunos endpoints funcionan, otros no.")
    else:
        print(f"\n❌ SERVIDOR SIMPLIFICADO NO FUNCIONA")
        print(f"   El problema es más profundo (red, firewall, etc.)")
    
    return success_count == total_count

if __name__ == "__main__":
    # Esperar un poco para que el servidor se inicie
    print("⏳ Esperando 2 segundos para que el servidor se inicie...")
    time.sleep(2)
    
    test_simple_server()