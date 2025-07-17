#!/usr/bin/env python3
"""
Diagnóstico Completo de Integración VersaAI
Identifica problemas entre Frontend y Backend
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

class VersaAIIntegrationDiagnostic:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.api_base = f"{self.backend_url}/api/v1"
        self.issues = []
        self.recommendations = []
        
    def log_issue(self, category: str, issue: str, severity: str = "ERROR"):
        """Log an issue found during diagnosis"""
        self.issues.append({
            "category": category,
            "issue": issue,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        })
        print(f"[{severity}] {category}: {issue}")
    
    def log_recommendation(self, recommendation: str):
        """Log a recommendation for fixing issues"""
        self.recommendations.append(recommendation)
        print(f"[RECOMENDACIÓN] {recommendation}")
    
    def check_backend_health(self) -> bool:
        """Check if backend is running and healthy"""
        print("\n=== VERIFICANDO SALUD DEL BACKEND ===")
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Backend activo en {self.backend_url}")
                print(f"   Respuesta: {response.json()}")
                return True
            else:
                self.log_issue("BACKEND", f"Backend responde con código {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.log_issue("BACKEND", "Backend no está ejecutándose o no es accesible")
            return False
        except Exception as e:
            self.log_issue("BACKEND", f"Error al conectar con backend: {e}")
            return False
    
    def check_api_documentation(self) -> bool:
        """Check if API documentation is accessible"""
        print("\n=== VERIFICANDO DOCUMENTACIÓN API ===")
        try:
            response = requests.get(f"{self.backend_url}/api/docs", timeout=5)
            if response.status_code == 200:
                print(f"✅ Documentación API accesible en {self.backend_url}/api/docs")
                return True
            else:
                self.log_issue("API_DOCS", f"Documentación API no accesible (código {response.status_code})")
                return False
        except Exception as e:
            self.log_issue("API_DOCS", f"Error al acceder a documentación: {e}")
            return False
    
    def check_cors_configuration(self) -> bool:
        """Check CORS configuration"""
        print("\n=== VERIFICANDO CONFIGURACIÓN CORS ===")
        try:
            # Simulate a preflight request
            headers = {
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type, Authorization'
            }
            response = requests.options(f"{self.api_base}/auth/login", headers=headers, timeout=5)
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
            }
            
            print(f"Headers CORS recibidos:")
            for header, value in cors_headers.items():
                print(f"  {header}: {value}")
            
            # Check if CORS allows frontend origin
            allowed_origin = cors_headers.get('Access-Control-Allow-Origin')
            if allowed_origin == '*' or allowed_origin == 'http://localhost:3000':
                print("✅ CORS configurado correctamente para el frontend")
                return True
            else:
                self.log_issue("CORS", f"CORS no permite origen del frontend. Permitido: {allowed_origin}")
                return False
                
        except Exception as e:
            self.log_issue("CORS", f"Error al verificar CORS: {e}")
            return False
    
    def check_auth_endpoints(self) -> Dict[str, Any]:
        """Check authentication endpoints structure"""
        print("\n=== VERIFICANDO ENDPOINTS DE AUTENTICACIÓN ===")
        
        endpoints_status = {
            'login': False,
            'register': False,
            'me': False
        }
        
        # Test login endpoint structure
        try:
            login_data = {
                "email": "test@example.com",
                "password": "wrongpassword"
            }
            response = requests.post(f"{self.api_base}/auth/login", json=login_data, timeout=5)
            
            if response.status_code == 401:
                print("✅ Endpoint /auth/login responde correctamente a credenciales inválidas")
                endpoints_status['login'] = True
            else:
                self.log_issue("AUTH_ENDPOINT", f"Login endpoint respuesta inesperada: {response.status_code}")
                
        except Exception as e:
            self.log_issue("AUTH_ENDPOINT", f"Error al probar endpoint login: {e}")
        
        # Test register endpoint structure
        try:
            register_data = {
                "email": "test_diagnostic@example.com",
                "password": "testpass123",
                "full_name": "Test User"
            }
            response = requests.post(f"{self.api_base}/auth/register", json=register_data, timeout=5)
            
            if response.status_code in [201, 400]:  # 201 success, 400 if already exists
                print("✅ Endpoint /auth/register responde correctamente")
                endpoints_status['register'] = True
                
                if response.status_code == 201:
                    response_data = response.json()
                    print(f"   Estructura de respuesta de registro: {list(response_data.keys())}")
            else:
                self.log_issue("AUTH_ENDPOINT", f"Register endpoint respuesta inesperada: {response.status_code}")
                
        except Exception as e:
            self.log_issue("AUTH_ENDPOINT", f"Error al probar endpoint register: {e}")
        
        return endpoints_status
    
    def check_frontend_backend_url_mismatch(self) -> bool:
        """Check for URL mismatches between frontend and backend"""
        print("\n=== VERIFICANDO CONCORDANCIA DE URLs ===")
        
        # Expected frontend API URL based on .env
        expected_frontend_api = "http://localhost:8000/api/v1"
        
        print(f"Backend API base: {self.api_base}")
        print(f"Frontend espera: {expected_frontend_api}")
        
        if self.api_base == expected_frontend_api:
            print("✅ URLs del frontend y backend coinciden")
            return True
        else:
            self.log_issue("URL_MISMATCH", "URLs del frontend y backend no coinciden")
            return False
    
    def check_response_structure_compatibility(self) -> bool:
        """Check if backend responses match frontend expectations"""
        print("\n=== VERIFICANDO ESTRUCTURA DE RESPUESTAS ===")
        
        # Create a test user and try to login to check response structure
        try:
            # First, create a test user
            register_data = {
                "email": f"diagnostic_{int(datetime.now().timestamp())}@versaai.com",
                "password": "diagnostic123",
                "full_name": "Diagnostic User"
            }
            
            register_response = requests.post(f"{self.api_base}/auth/register", json=register_data, timeout=5)
            
            if register_response.status_code == 201:
                print("✅ Usuario de prueba creado exitosamente")
                
                # Now try to login with the created user
                login_data = {
                    "email": register_data["email"],
                    "password": register_data["password"]
                }
                
                login_response = requests.post(f"{self.api_base}/auth/login", json=login_data, timeout=5)
                
                if login_response.status_code == 200:
                    login_data_response = login_response.json()
                    print(f"✅ Login exitoso. Estructura de respuesta:")
                    print(f"   Campos disponibles: {list(login_data_response.keys())}")
                    
                    # Check if required fields are present
                    required_fields = ['access_token', 'token_type']
                    missing_fields = [field for field in required_fields if field not in login_data_response]
                    
                    if not missing_fields:
                        print("✅ Respuesta de login contiene todos los campos requeridos")
                        
                        # Check if we can get user info with the token
                        token = login_data_response['access_token']
                        headers = {'Authorization': f'Bearer {token}'}
                        
                        me_response = requests.get(f"{self.api_base}/auth/me", headers=headers, timeout=5)
                        
                        if me_response.status_code == 200:
                            user_data = me_response.json()
                            print(f"✅ Endpoint /auth/me funciona. Campos de usuario: {list(user_data.keys())}")
                            return True
                        else:
                            self.log_issue("RESPONSE_STRUCTURE", f"Endpoint /auth/me falla: {me_response.status_code}")
                    else:
                        self.log_issue("RESPONSE_STRUCTURE", f"Campos faltantes en respuesta de login: {missing_fields}")
                else:
                    self.log_issue("RESPONSE_STRUCTURE", f"Login falla con usuario válido: {login_response.status_code}")
            else:
                self.log_issue("RESPONSE_STRUCTURE", f"No se pudo crear usuario de prueba: {register_response.status_code}")
                
        except Exception as e:
            self.log_issue("RESPONSE_STRUCTURE", f"Error al verificar estructura de respuestas: {e}")
        
        return False
    
    def generate_recommendations(self):
        """Generate recommendations based on found issues"""
        print("\n=== RECOMENDACIONES DE SOLUCIÓN ===")
        
        if any(issue['category'] == 'BACKEND' for issue in self.issues):
            self.log_recommendation("Verificar que el servidor backend esté ejecutándose en puerto 8000")
            self.log_recommendation("Ejecutar: cd backend && python start_server.py")
        
        if any(issue['category'] == 'CORS' for issue in self.issues):
            self.log_recommendation("Verificar configuración CORS en backend/src/main.py")
            self.log_recommendation("Asegurar que allow_origins incluya 'http://localhost:3000'")
        
        if any(issue['category'] == 'URL_MISMATCH' for issue in self.issues):
            self.log_recommendation("Verificar variables de entorno en frontend/.env")
            self.log_recommendation("Asegurar que VITE_API_BASE_URL=http://localhost:8000")
        
        if any(issue['category'] == 'AUTH_ENDPOINT' for issue in self.issues):
            self.log_recommendation("Verificar implementación de endpoints de autenticación")
            self.log_recommendation("Revisar backend/src/api/v1/endpoints/auth.py")
        
        if any(issue['category'] == 'RESPONSE_STRUCTURE' for issue in self.issues):
            self.log_recommendation("Verificar compatibilidad entre respuestas del backend y expectativas del frontend")
            self.log_recommendation("Revisar frontend/src/stores/auth.js y backend/src/schemas/auth.py")
    
    def run_full_diagnostic(self):
        """Run complete diagnostic"""
        print("🔍 INICIANDO DIAGNÓSTICO COMPLETO DE INTEGRACIÓN VERSAAI")
        print("=" * 60)
        
        # Run all checks
        backend_healthy = self.check_backend_health()
        api_docs_accessible = self.check_api_documentation()
        cors_ok = self.check_cors_configuration()
        auth_endpoints_ok = self.check_auth_endpoints()
        urls_match = self.check_frontend_backend_url_mismatch()
        responses_compatible = self.check_response_structure_compatibility()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL DIAGNÓSTICO")
        print("=" * 60)
        
        total_checks = 6
        passed_checks = sum([
            backend_healthy,
            api_docs_accessible, 
            cors_ok,
            bool(auth_endpoints_ok.get('login', False)),
            urls_match,
            responses_compatible
        ])
        
        print(f"Verificaciones pasadas: {passed_checks}/{total_checks}")
        print(f"Problemas encontrados: {len(self.issues)}")
        
        if self.issues:
            print("\n🚨 PROBLEMAS IDENTIFICADOS:")
            for issue in self.issues:
                print(f"  [{issue['severity']}] {issue['category']}: {issue['issue']}")
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Final assessment
        print("\n" + "=" * 60)
        if len(self.issues) == 0:
            print("✅ SISTEMA COMPLETAMENTE FUNCIONAL")
            print("No se encontraron problemas de integración.")
        elif len(self.issues) <= 2:
            print("⚠️ PROBLEMAS MENORES DETECTADOS")
            print("El sistema debería funcionar con correcciones menores.")
        else:
            print("❌ PROBLEMAS CRÍTICOS DETECTADOS")
            print("Se requieren correcciones importantes para el funcionamiento.")
        
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Revisar y aplicar las recomendaciones listadas arriba")
        print("2. Reiniciar los servicios después de hacer cambios")
        print("3. Ejecutar este diagnóstico nuevamente para verificar")
        print("4. Probar el login en el frontend con credenciales válidas")
        
        return len(self.issues) == 0

if __name__ == "__main__":
    diagnostic = VersaAIIntegrationDiagnostic()
    success = diagnostic.run_full_diagnostic()
    sys.exit(0 if success else 1)