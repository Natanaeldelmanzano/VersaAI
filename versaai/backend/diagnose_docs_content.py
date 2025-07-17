#!/usr/bin/env python3
"""
Script para diagnosticar el contenido de las páginas de documentación del backend
Verifica si las páginas de Swagger UI, ReDoc y OpenAPI JSON tienen contenido válido
"""

import requests
import json
import re

def check_url_content(url, description):
    """Verifica el contenido de una URL específica"""
    print(f"\n{'='*60}")
    print(f"Verificando: {description}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'No especificado')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content = response.text
            print(f"Longitud del contenido: {len(content)} caracteres")
            
            # Verificar si es HTML
            if 'text/html' in response.headers.get('content-type', ''):
                # Buscar título usando regex
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else 'Sin título'
                print(f"Título de la página: {title}")
                
                # Verificar elementos específicos de Swagger/ReDoc
                swagger_matches = re.findall(r'(swagger|redoc)', content, re.IGNORECASE)
                print(f"Referencias a Swagger/ReDoc: {len(swagger_matches)}")
                
                # Verificar scripts
                script_matches = re.findall(r'<script[^>]*>', content, re.IGNORECASE)
                print(f"Tags <script> encontrados: {len(script_matches)}")
                
                # Verificar CSS
                css_matches = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', content, re.IGNORECASE)
                print(f"Enlaces CSS encontrados: {len(css_matches)}")
                
                # Buscar el contenido del body
                body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
                if body_match:
                    body_content = body_match.group(1)
                    # Remover tags HTML para obtener solo texto
                    body_text = re.sub(r'<[^>]+>', '', body_content).strip()
                    print(f"\nPrimeros 300 caracteres del body (sin HTML):")
                    print(f"'{body_text[:300]}{'...' if len(body_text) > 300 else ''}")
                    
                    # Verificar si el body está prácticamente vacío
                    if len(body_text.strip()) < 10:
                        print("⚠️  PROBLEMA: El body está prácticamente vacío")
                else:
                    print("\nNo se encontró elemento <body> o está malformado")
                
                # Verificar si hay divs con IDs específicos de Swagger/ReDoc
                swagger_div = re.search(r'<div[^>]*id=["\']swagger-ui["\'][^>]*>', content, re.IGNORECASE)
                redoc_div = re.search(r'<div[^>]*id=["\']redoc["\'][^>]*>', content, re.IGNORECASE)
                
                if swagger_div:
                    print("✅ Encontrado div#swagger-ui")
                if redoc_div:
                    print("✅ Encontrado div#redoc")
                    
                if not swagger_div and not redoc_div and 'swagger' in url:
                    print("⚠️  PROBLEMA: No se encontraron divs específicos de Swagger UI")
                if not redoc_div and 'redoc' in url:
                    print("⚠️  PROBLEMA: No se encontraron divs específicos de ReDoc")
                    
            # Verificar si es JSON
            elif 'application/json' in response.headers.get('content-type', ''):
                try:
                    json_data = json.loads(content)
                    print(f"JSON válido con {len(json_data)} elementos principales")
                    if 'openapi' in json_data:
                        print(f"Versión OpenAPI: {json_data.get('openapi')}")
                    if 'info' in json_data:
                        info = json_data.get('info', {})
                        print(f"Título API: {info.get('title')}")
                        print(f"Versión API: {info.get('version')}")
                    if 'paths' in json_data:
                        print(f"Número de endpoints: {len(json_data.get('paths', {}))}")
                except json.JSONDecodeError as e:
                    print(f"❌ Error al parsear JSON: {e}")
                    print(f"Primeros 500 caracteres: {content[:500]}")
            
            # Para cualquier tipo de contenido, verificar si está vacío o solo espacios
            if not content.strip():
                print("❌ PROBLEMA CRÍTICO: El contenido está completamente vacío")
            elif len(content.strip()) < 100:
                print(f"⚠️  PROBLEMA: Contenido muy corto: '{content.strip()}'")
            else:
                print("✅ Contenido tiene longitud adecuada")
                
            # Mostrar una muestra del contenido HTML
            if 'text/html' in response.headers.get('content-type', ''):
                print(f"\nPrimeros 200 caracteres del HTML:")
                print(f"'{content[:200]}{'...' if len(content) > 200 else ''}")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - El servidor no está disponible")
    except requests.exceptions.Timeout:
        print("❌ Timeout - El servidor no responde")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO DE CONTENIDO DE DOCUMENTACIÓN DEL BACKEND")
    print("Verificando el contenido real de las páginas de documentación...")
    
    # URLs a verificar
    urls_to_check = [
        ("http://localhost:8000/api/docs", "Swagger UI"),
        ("http://localhost:8000/api/redoc", "ReDoc"),
        ("http://localhost:8000/openapi.json", "OpenAPI JSON Schema"),
        ("http://localhost:8000/", "Root Endpoint"),
        ("http://localhost:8000/api/health/", "Health Check")
    ]
    
    for url, description in urls_to_check:
        check_url_content(url, description)
    
    print(f"\n{'='*60}")
    print("RESUMEN DEL DIAGNÓSTICO")
    print(f"{'='*60}")
    print("Si las páginas muestran contenido válido pero se ven en blanco en el navegador,")
    print("el problema podría ser:")
    print("1. JavaScript bloqueado o con errores")
    print("2. CSS no cargando correctamente")
    print("3. Problemas de CORS")
    print("4. Extensiones del navegador interfiriendo")
    print("5. Caché del navegador corrupto")
    print("6. FastAPI no sirviendo correctamente los assets estáticos")
    print("\nSoluciones sugeridas:")
    print("- Abrir herramientas de desarrollador (F12) y verificar errores en Console")
    print("- Verificar la pestaña Network para ver qué recursos fallan al cargar")
    print("- Limpiar caché del navegador (Ctrl+Shift+Delete)")
    print("- Probar en modo incógnito")
    print("- Probar en otro navegador")
    print("- Verificar configuración de CORS en el backend")
    print("- Reiniciar el servidor backend")

if __name__ == "__main__":
    main()