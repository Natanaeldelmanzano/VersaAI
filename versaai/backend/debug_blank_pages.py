#!/usr/bin/env python3
"""
Script para diagnosticar en detalle por qué las páginas de documentación se ven en blanco
"""

import requests
import re
from urllib.parse import urljoin

def analyze_html_content(url, content):
    """Analizar el contenido HTML en detalle"""
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DETALLADO: {url}")
    print(f"{'='*60}")
    
    # Verificar longitud
    print(f"📏 Longitud del contenido: {len(content)} caracteres")
    
    # Verificar estructura HTML básica
    has_html = bool(re.search(r'<html[^>]*>', content, re.IGNORECASE))
    has_head = bool(re.search(r'<head[^>]*>', content, re.IGNORECASE))
    has_body = bool(re.search(r'<body[^>]*>', content, re.IGNORECASE))
    
    print(f"🏗️  Estructura HTML:")
    print(f"   - Tiene <html>: {'✅' if has_html else '❌'}")
    print(f"   - Tiene <head>: {'✅' if has_head else '❌'}")
    print(f"   - Tiene <body>: {'✅' if has_body else '❌'}")
    
    # Verificar scripts
    scripts = re.findall(r'<script[^>]*src=["\']([^"\'>]+)["\'][^>]*>', content, re.IGNORECASE)
    inline_scripts = re.findall(r'<script[^>]*>([^<]+)</script>', content, re.IGNORECASE | re.DOTALL)
    
    print(f"\n📜 Scripts encontrados:")
    print(f"   - Scripts externos: {len(scripts)}")
    for i, script in enumerate(scripts[:5]):  # Mostrar solo los primeros 5
        print(f"     {i+1}. {script}")
    if len(scripts) > 5:
        print(f"     ... y {len(scripts) - 5} más")
    
    print(f"   - Scripts inline: {len(inline_scripts)}")
    
    # Verificar CSS
    css_links = re.findall(r'<link[^>]*href=["\']([^"\'>]+)["\'][^>]*rel=["\']stylesheet["\'][^>]*>', content, re.IGNORECASE)
    css_links += re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\'>]+)["\'][^>]*>', content, re.IGNORECASE)
    
    print(f"\n🎨 CSS encontrado:")
    print(f"   - Hojas de estilo externas: {len(css_links)}")
    for i, css in enumerate(css_links[:3]):  # Mostrar solo las primeras 3
        print(f"     {i+1}. {css}")
    if len(css_links) > 3:
        print(f"     ... y {len(css_links) - 3} más")
    
    # Verificar contenido del body
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
    if body_match:
        body_content = body_match.group(1).strip()
        print(f"\n📄 Contenido del body:")
        print(f"   - Longitud: {len(body_content)} caracteres")
        
        # Verificar si hay divs principales
        main_divs = re.findall(r'<div[^>]*id=["\']([^"\'>]+)["\'][^>]*>', body_content, re.IGNORECASE)
        print(f"   - Divs con ID: {len(main_divs)}")
        for div_id in main_divs[:5]:
            print(f"     - #{div_id}")
        
        # Mostrar una muestra del contenido del body
        if len(body_content) > 0:
            sample = body_content[:200].replace('\n', ' ').replace('\r', '')
            print(f"   - Muestra: {sample}...")
        else:
            print(f"   - ⚠️  BODY VACÍO")
    else:
        print(f"\n❌ No se encontró contenido del body")
    
    # Verificar errores comunes
    print(f"\n🔍 Verificación de errores:")
    
    # Verificar si hay mensajes de error
    error_patterns = [
        r'error',
        r'failed',
        r'not found',
        r'404',
        r'500',
        r'exception'
    ]
    
    for pattern in error_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"   - ⚠️  Posible error encontrado: '{pattern}'")
    
    # Verificar si es una página de Swagger/ReDoc válida
    swagger_indicators = [
        r'swagger',
        r'openapi',
        r'redoc',
        r'api-docs'
    ]
    
    swagger_found = False
    for indicator in swagger_indicators:
        if re.search(indicator, content, re.IGNORECASE):
            swagger_found = True
            print(f"   - ✅ Indicador de documentación encontrado: '{indicator}'")
    
    if not swagger_found:
        print(f"   - ❌ No se encontraron indicadores de documentación API")
    
    return {
        'length': len(content),
        'has_html': has_html,
        'has_head': has_head,
        'has_body': has_body,
        'scripts_count': len(scripts),
        'css_count': len(css_links),
        'swagger_found': swagger_found
    }

def test_resource_loading(base_url, scripts, css_links):
    """Probar si los recursos externos se cargan correctamente"""
    print(f"\n🔗 PROBANDO CARGA DE RECURSOS EXTERNOS")
    print(f"{'='*60}")
    
    failed_resources = []
    
    # Probar scripts
    print(f"\n📜 Probando scripts ({len(scripts)} encontrados):")
    for i, script in enumerate(scripts[:5]):  # Probar solo los primeros 5
        try:
            if script.startswith('http'):
                url = script
            else:
                url = urljoin(base_url, script)
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {script} - OK ({len(response.content)} bytes)")
            else:
                print(f"   ❌ {script} - Error {response.status_code}")
                failed_resources.append(script)
        except Exception as e:
            print(f"   ❌ {script} - Error: {str(e)}")
            failed_resources.append(script)
    
    # Probar CSS
    print(f"\n🎨 Probando CSS ({len(css_links)} encontrados):")
    for i, css in enumerate(css_links[:3]):  # Probar solo los primeros 3
        try:
            if css.startswith('http'):
                url = css
            else:
                url = urljoin(base_url, css)
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {css} - OK ({len(response.content)} bytes)")
            else:
                print(f"   ❌ {css} - Error {response.status_code}")
                failed_resources.append(css)
        except Exception as e:
            print(f"   ❌ {css} - Error: {str(e)}")
            failed_resources.append(css)
    
    return failed_resources

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO AVANZADO DE PÁGINAS EN BLANCO")
    print("="*60)
    
    base_url = "http://localhost:8000"
    
    urls_to_test = [
        f"{base_url}/api/docs",
        f"{base_url}/api/redoc"
    ]
    
    all_results = {}
    
    for url in urls_to_test:
        try:
            print(f"\n🌐 Probando: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                results = analyze_html_content(url, content)
                all_results[url] = results
                
                # Extraer recursos para probar
                scripts = re.findall(r'<script[^>]*src=["\']([^"\'>]+)["\'][^>]*>', content, re.IGNORECASE)
                css_links = re.findall(r'<link[^>]*href=["\']([^"\'>]+)["\'][^>]*rel=["\']stylesheet["\'][^>]*>', content, re.IGNORECASE)
                css_links += re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\'>]+)["\'][^>]*>', content, re.IGNORECASE)
                
                if scripts or css_links:
                    failed_resources = test_resource_loading(base_url, scripts, css_links)
                    all_results[url]['failed_resources'] = failed_resources
                
            else:
                print(f"❌ Error {response.status_code} al acceder a {url}")
                
        except Exception as e:
            print(f"❌ Error al probar {url}: {str(e)}")
    
    # Resumen final
    print(f"\n📊 RESUMEN FINAL DEL DIAGNÓSTICO")
    print(f"{'='*60}")
    
    for url, results in all_results.items():
        print(f"\n🔗 {url}:")
        print(f"   - Longitud: {results['length']} caracteres")
        print(f"   - HTML válido: {'✅' if results['has_html'] else '❌'}")
        print(f"   - Scripts: {results['scripts_count']}")
        print(f"   - CSS: {results['css_count']}")
        print(f"   - Documentación API: {'✅' if results['swagger_found'] else '❌'}")
        
        if 'failed_resources' in results and results['failed_resources']:
            print(f"   - ⚠️  Recursos fallidos: {len(results['failed_resources'])}")
            for resource in results['failed_resources'][:3]:
                print(f"     - {resource}")
    
    print(f"\n💡 POSIBLES CAUSAS DE PÁGINAS EN BLANCO:")
    print(f"1. Recursos JavaScript/CSS no se cargan (verificar arriba)")
    print(f"2. FastAPI no sirve correctamente los assets estáticos")
    print(f"3. Problemas de Content Security Policy (CSP)")
    print(f"4. JavaScript bloqueado por el navegador")
    print(f"5. Extensiones del navegador interfiriendo")
    print(f"6. Caché del navegador corrupto")
    
    print(f"\n🛠️  SOLUCIONES RECOMENDADAS:")
    print(f"1. Abrir DevTools (F12) y verificar errores en Console")
    print(f"2. Verificar la pestaña Network para recursos fallidos")
    print(f"3. Probar en modo incógnito")
    print(f"4. Limpiar caché del navegador")
    print(f"5. Verificar configuración de FastAPI para servir assets")
    print(f"6. Probar con otro navegador")

if __name__ == "__main__":
    main()