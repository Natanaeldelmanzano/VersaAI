#!/usr/bin/env python3
"""
Script de Solución Automática para VersaAI
Registra un usuario de prueba y verifica la funcionalidad completa del sistema
"""

import requests
import json
import time
from typing import Dict, Any

class VersaAIAutoSolution:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.test_user = {
            "email": "admin@versaai.com",
            "password": "admin123456",
            "full_name": "VersaAI Administrator"
        }
        self.access_token = None
        
    def check_servers_status(self) -> Dict[str, bool]:
        """Verifica el estado de los servidores"""
        print("\n🔍 VERIFICANDO ESTADO DE SERVIDORES...")
        
        status = {
            "backend": False,
            "frontend": False
        }
        
        # Verificar Backend
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                status["backend"] = True
                print("✅ Backend: ACTIVO")
            else:
                print(f"❌ Backend: Error {response.status_code}")
        except Exception as e:
            print(f"❌ Backend: No disponible - {e}")
        
        # Verificar Frontend
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                status["frontend"] = True
                print("✅ Frontend: ACTIVO")
            else:
                print(f"❌ Frontend: Error {response.status_code}")
        except Exception as e:
            print(f"❌ Frontend: No disponible - {e}")
        
        return status
    
    def register_test_user(self) -> bool:
        """Registra un usuario de prueba"""
        print("\n👤 REGISTRANDO USUARIO DE PRUEBA...")
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/register",
                json=self.test_user,
                timeout=10
            )
            
            if response.status_code == 201:
                print("✅ Usuario registrado exitosamente")
                result = response.json()
                print(f"   ID: {result.get('id')}")
                print(f"   Email: {result.get('email')}")
                print(f"   Nombre: {result.get('full_name')}")
                return True
            elif response.status_code == 400 and "already registered" in response.text:
                print("ℹ️  Usuario ya existe, continuando...")
                return True
            else:
                print(f"❌ Error al registrar: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error en registro: {e}")
            return False
    
    def test_login(self) -> bool:
        """Prueba el login del usuario"""
        print("\n🔐 PROBANDO LOGIN...")
        
        try:
            login_data = {
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
            
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token")
                print("✅ Login exitoso")
                print(f"   Token: {self.access_token[:50]}...")
                print(f"   Usuario: {result.get('user', {}).get('email')}")
                return True
            else:
                print(f"❌ Error en login: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return False
    
    def test_authenticated_endpoints(self) -> Dict[str, bool]:
        """Prueba endpoints que requieren autenticación"""
        print("\n🔒 PROBANDO ENDPOINTS AUTENTICADOS...")
        
        if not self.access_token:
            print("❌ No hay token de acceso disponible")
            return {}
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        endpoints = {
            "profile": "/api/v1/auth/me",
            "chatbots": "/api/v1/chatbots/",
            "users": "/api/v1/users/",
            "conversations": "/api/v1/conversations/"
        }
        
        results = {}
        
        for name, endpoint in endpoints.items():
            try:
                response = requests.get(
                    f"{self.backend_url}{endpoint}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"✅ {name}: FUNCIONAL")
                    results[name] = True
                else:
                    print(f"❌ {name}: Error {response.status_code}")
                    results[name] = False
                    
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
                results[name] = False
        
        return results
    
    def test_chat_functionality(self) -> bool:
        """Prueba la funcionalidad de chat"""
        print("\n💬 PROBANDO FUNCIONALIDAD DE CHAT...")
        
        if not self.access_token:
            print("❌ No hay token de acceso disponible")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Crear una conversación de prueba
        chat_data = {
            "message": "Hola, ¿cómo estás?",
            "conversation_id": None
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/conversations/chat",
                json=chat_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Chat funcional")
                print(f"   Respuesta: {result.get('response', 'N/A')[:100]}...")
                return True
            else:
                print(f"❌ Error en chat: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error en chat: {e}")
            return False
    
    def generate_solution_report(self, results: Dict[str, Any]) -> str:
        """Genera un reporte de la solución"""
        report = "\n" + "="*60 + "\n"
        report += "🎯 REPORTE DE SOLUCIÓN AUTOMÁTICA VERSAAI\n"
        report += "="*60 + "\n\n"
        
        # Estado de servidores
        report += "📊 ESTADO DE SERVIDORES:\n"
        for server, status in results.get('servers', {}).items():
            status_icon = "✅" if status else "❌"
            report += f"   {status_icon} {server.upper()}: {'ACTIVO' if status else 'INACTIVO'}\n"
        
        # Autenticación
        report += "\n🔐 AUTENTICACIÓN:\n"
        auth_status = results.get('auth', {})
        for test, status in auth_status.items():
            status_icon = "✅" if status else "❌"
            report += f"   {status_icon} {test.upper()}: {'EXITOSO' if status else 'FALLIDO'}\n"
        
        # Endpoints
        report += "\n🔒 ENDPOINTS AUTENTICADOS:\n"
        for endpoint, status in results.get('endpoints', {}).items():
            status_icon = "✅" if status else "❌"
            report += f"   {status_icon} {endpoint.upper()}: {'FUNCIONAL' if status else 'ERROR'}\n"
        
        # Chat
        chat_status = results.get('chat', False)
        report += "\n💬 FUNCIONALIDAD DE CHAT:\n"
        status_icon = "✅" if chat_status else "❌"
        report += f"   {status_icon} CHAT: {'FUNCIONAL' if chat_status else 'ERROR'}\n"
        
        # Credenciales de prueba
        report += "\n👤 CREDENCIALES DE PRUEBA:\n"
        report += f"   📧 Email: {self.test_user['email']}\n"
        report += f"   🔑 Password: {self.test_user['password']}\n"
        
        # URLs importantes
        report += "\n🌐 URLS IMPORTANTES:\n"
        report += f"   🖥️  Frontend: {self.frontend_url}\n"
        report += f"   ⚙️  Backend API: {self.backend_url}/api/v1\n"
        report += f"   📚 Documentación: {self.backend_url}/api/docs\n"
        report += f"   🔄 ReDoc: {self.backend_url}/api/redoc\n"
        
        report += "\n" + "="*60 + "\n"
        
        return report
    
    def run_complete_solution(self):
        """Ejecuta la solución completa automáticamente"""
        print("🚀 INICIANDO SOLUCIÓN AUTOMÁTICA VERSAAI")
        print("="*50)
        
        results = {
            'servers': {},
            'auth': {},
            'endpoints': {},
            'chat': False
        }
        
        # 1. Verificar servidores
        results['servers'] = self.check_servers_status()
        
        if not all(results['servers'].values()):
            print("\n❌ ALGUNOS SERVIDORES NO ESTÁN ACTIVOS")
            print("   Por favor, inicia los servidores antes de continuar")
            return
        
        # 2. Registrar usuario de prueba
        results['auth']['register'] = self.register_test_user()
        
        # 3. Probar login
        results['auth']['login'] = self.test_login()
        
        if not results['auth']['login']:
            print("\n❌ LOGIN FALLÓ - No se pueden probar endpoints autenticados")
            return
        
        # 4. Probar endpoints autenticados
        results['endpoints'] = self.test_authenticated_endpoints()
        
        # 5. Probar chat
        results['chat'] = self.test_chat_functionality()
        
        # 6. Generar reporte
        report = self.generate_solution_report(results)
        print(report)
        
        # Guardar reporte
        with open('versaai_solution_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("📄 Reporte guardado en: versaai_solution_report.txt")
        
        # Determinar si la solución fue exitosa
        success_rate = (
            sum(results['servers'].values()) +
            sum(results['auth'].values()) +
            sum(results['endpoints'].values()) +
            (1 if results['chat'] else 0)
        ) / (len(results['servers']) + len(results['auth']) + len(results['endpoints']) + 1)
        
        if success_rate >= 0.8:
            print("\n🎉 SOLUCIÓN EXITOSA - Sistema funcionando correctamente")
        else:
            print("\n⚠️  SOLUCIÓN PARCIAL - Algunos componentes requieren atención")

if __name__ == "__main__":
    solution = VersaAIAutoSolution()
    solution.run_complete_solution()