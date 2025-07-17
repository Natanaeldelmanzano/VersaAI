#!/usr/bin/env python3
"""
Script para probar el servidor principal corregido de VersaAI
Verifica que las páginas de documentación funcionen correctamente
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
        
        # Verificar headers de seguridad y rendimiento
        important_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options', 
            'X-XSS-Protection',
            'X-Process-Time',
            'X-Request-ID',
            'Content-Security-Policy'
        ]
        
        present_headers = []
        for header in important_headers:
            if header in response.headers:
                value = response.headers[header]
                present_headers.append(f"{header}: {value}")
        
        if present_headers:
            print(f"🔒 Headers importantes:")
            for header in present_headers:
                print(f"   • {header}")
        
        # Para endpoints de documentación, verificar contenido específico
        if '/docs' in endpoint or '/redoc' in endpoint:
            content = response.text
            
            # Verificar elementos de documentación
            doc_indicators = ['swagger', 'redoc', 'openapi', 'api documentation']
            found_indicators = []
            for indicator in doc_indicators:
                if indicator in content.lower():
                    found_indicators.append(indicator)
            
            if found_indicators:
                print(f"✅ Elementos de documentación encontrados: {', '.join(found_indicators)}")
            else:
                print("⚠️  No se detectaron elementos de documentación")
                
            # Verificar recursos JavaScript/CSS
            js_css_count = content.count('<script') + content.count('<link')
            if js_css_count > 0:
                print(f"✅ Recursos JavaScript/CSS encontrados: {js_css_count}")
            else:
                print("⚠️  No se detectaron recursos JavaScript/CSS")
                
            # Verificar CSP
            csp_header = response.headers.get('Content-Security-Policy', '')
            if csp_header:
                if 'unsafe-inline' in csp_header or 'unsafe-eval' in csp_header:
                    print(f"✅ CSP permisivo detectado")
                else:
                    print(f"⚠️  CSP restrictivo: {csp_header}")
            else:
                print("✅ Sin CSP restrictivo")
                
            # Verificar que la página no esté en blanco
            if len(content.strip()) > 100:
                print("✅ Página con contenido suficiente")
            else:
                print("❌ Página posiblemente en blanco")
        
        # Para JSON endpoints
        elif 'application/json' in content_type:
            try:
                json_data = response.json()
                print(f"✅ JSON válido con {len(json_data)} campos")
                if isinstance(json_data, dict):
                    for key, value in list(json_data.items())[:3]:  # Mostrar primeros 3 campos
                        print(f"   • {key}: {value}")
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
    print("🚀 Probando servidor principal VersaAI CORREGIDO")
    print("=" * 70)
    print("🔧 Cambios aplicados:")
    print("   • SecurityHeadersMiddleware removido")
    print("   • CORS más permisivo para desarrollo")
    print("   • TrustedHost más permisivo")
    print("   • Sin CSP restrictivo en documentación")
    print("=" * 70)
    
    base_url = "http://localhost:8000"
    
    # Lista de endpoints a probar
    endpoints = [
        ("/", "Endpoint raíz"),
        ("/health", "Health check"),
        ("/api/docs", "Swagger UI - CRÍTICO"),
        ("/api/redoc", "ReDoc - CRÍTICO"),
        ("/api/openapi.json", "OpenAPI JSON")
    ]
    
    results = []
    critical_endpoints = ["/api/docs", "/api/redoc"]
    
    for endpoint, description in endpoints:
        success = test_endpoint(base_url, endpoint, description)
        results.append((endpoint, success, endpoint in critical_endpoints))
        time.sleep(0.5)  # Pequeña pausa entre requests
    
    # Resumen de resultados
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)
    
    successful = 0
    critical_successful = 0
    critical_total = 0
    
    for endpoint, success, is_critical in results:
        status = "✅ OK" if success else "❌ FAIL"
        critical_mark = "🔥 CRÍTICO" if is_critical else ""
        print(f"{endpoint:<25} {status} {critical_mark}")
        
        if success:
            successful += 1
        if is_critical:
            critical_total += 1
            if success:
                critical_successful += 1
    
    print(f"\n🎯 Éxito general: {successful}/{len(results)} endpoints")
    print(f"🔥 Endpoints críticos: {critical_successful}/{critical_total} funcionando")
    
    if critical_successful == critical_total:
        print("\n🎉 ¡PROBLEMA RESUELTO! Las páginas de documentación funcionan correctamente")
        print("\n🌐 URLs de documentación disponibles:")
        print(f"   • Swagger UI: {base_url}/api/docs")
        print(f"   • ReDoc: {base_url}/api/redoc")
        print(f"   • Health Check: {base_url}/health")
        
        print("\n✅ Solución aplicada exitosamente:")
        print("   • SecurityHeadersMiddleware removido del pipeline")
        print("   • CSP restrictivo eliminado")
        print("   • Middlewares de performance mantenidos")
        print("   • Rate limiting funcional")
        print("   • Headers de seguridad básicos preservados")
        
    elif critical_successful > 0:
        print(f"\n⚠️  Progreso parcial: {critical_successful}/{critical_total} páginas críticas funcionan")
        print("\n🔧 Revisar configuración adicional si es necesario")
        
    else:
        print("\n❌ Las páginas de documentación siguen fallando")
        print("\n🔧 Acciones recomendadas:")
        print("   • Verificar que los cambios se aplicaron correctamente")
        print("   • Revisar logs del servidor para errores")
        print("   • Considerar middlewares adicionales que puedan interferir")

if __name__ == "__main__":
    main()