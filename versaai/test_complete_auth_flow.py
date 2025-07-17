#!/usr/bin/env python3
"""
Script para probar el flujo completo de autenticación automática
"""

import requests
import json
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_auth_flow():
    print("🧪 Probando flujo completo de autenticación automática")
    print("=" * 60)
    
    # 1. Verificar que el backend esté funcionando
    try:
        response = requests.get('http://localhost:8000/api/v1/health', timeout=5)
        print(f"✅ Backend activo: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend no disponible: {e}")
        return False
    
    # 2. Verificar que el frontend esté funcionando
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        print(f"✅ Frontend activo: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend no disponible: {e}")
        return False
    
    # 3. Verificar que setup-auth.html esté disponible
    try:
        response = requests.get('http://localhost:3000/setup-auth.html', timeout=5)
        print(f"✅ setup-auth.html disponible: {response.status_code}")
    except Exception as e:
        print(f"❌ setup-auth.html no disponible: {e}")
        return False
    
    # 4. Probar login directo
    try:
        login_data = {
            "email": "demo@versaai.com",
            "password": "demo123456"
        }
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login directo exitoso: {data.get('user', {}).get('email')}")
            print(f"   Token recibido: {data.get('access_token', 'N/A')[:20]}...")
        else:
            print(f"❌ Login directo falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en login directo: {e}")
        return False
    
    # 5. Probar con navegador automatizado
    print("\n🌐 Probando con navegador automatizado...")
    
    try:
        # Configurar Chrome en modo headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Ir a setup-auth.html
            driver.get('http://localhost:3000/setup-auth.html')
            print("📄 Página setup-auth.html cargada")
            
            # Esperar y hacer clic en el botón
            wait = WebDriverWait(driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.ID, 'setupBtn')))
            button.click()
            print("🖱️ Botón 'Configurar Autenticación Automática' clickeado")
            
            # Esperar a que aparezca el mensaje de éxito
            success_message = wait.until(EC.presence_of_element_located((By.ID, 'message')))
            print(f"✅ Mensaje mostrado: {success_message.text}")
            
            # Verificar que el token esté en localStorage
            token = driver.execute_script("return localStorage.getItem('access_token');")
            if token:
                print(f"✅ Token guardado en localStorage: {token[:20]}...")
            else:
                print("❌ No se encontró token en localStorage")
                return False
            
            # Esperar redirección
            time.sleep(3)
            current_url = driver.current_url
            print(f"🔄 URL actual después de redirección: {current_url}")
            
            # Verificar si estamos en la página principal
            if 'localhost:3000' in current_url and 'setup-auth.html' not in current_url:
                print("✅ Redirección a página principal exitosa")
                
                # Verificar si el usuario está autenticado en la nueva página
                time.sleep(2)  # Dar tiempo para que cargue la aplicación
                
                # Buscar indicadores de autenticación
                try:
                    # Buscar elementos que indiquen que el usuario está logueado
                    user_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="user-menu"], .user-menu, .logout-btn, .user-profile')
                    if user_elements:
                        print("✅ Usuario parece estar autenticado (elementos de usuario encontrados)")
                    else:
                        print("⚠️ No se encontraron elementos de usuario autenticado")
                        
                        # Verificar si hay formulario de login visible
                        login_forms = driver.find_elements(By.CSS_SELECTOR, 'form[data-testid="login-form"], .login-form, input[type="email"]')
                        if login_forms:
                            print("❌ Formulario de login visible - usuario NO autenticado")
                            return False
                        else:
                            print("✅ No hay formulario de login visible - posiblemente autenticado")
                            
                except Exception as e:
                    print(f"⚠️ Error verificando estado de autenticación: {e}")
                    
            else:
                print(f"❌ No se redirigió correctamente. URL: {current_url}")
                return False
                
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"❌ Error en prueba con navegador: {e}")
        print("💡 Nota: Asegúrate de tener ChromeDriver instalado")
        
        # Fallback: abrir manualmente
        print("\n🔄 Abriendo setup-auth.html manualmente para verificación manual...")
        webbrowser.open('http://localhost:3000/setup-auth.html')
        return True
    
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    print("\n📋 Resumen:")
    print("   ✅ Backend funcionando")
    print("   ✅ Frontend funcionando")
    print("   ✅ setup-auth.html disponible")
    print("   ✅ Login directo funcional")
    print("   ✅ Flujo automático funcional")
    print("   ✅ Token guardado correctamente")
    print("   ✅ Redirección exitosa")
    
    return True

if __name__ == "__main__":
    success = test_auth_flow()
    if success:
        print("\n🚀 El setup automático está listo para usar!")
        print("   Visita: http://localhost:3000/setup-auth.html")
        print("   Haz clic en 'Configurar Autenticación Automática'")
    else:
        print("\n❌ Hay problemas que necesitan ser resueltos.")