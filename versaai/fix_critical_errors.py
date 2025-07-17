#!/usr/bin/env python3
"""
Script para corregir errores críticos identificados en VersaAI:
1. ChatRequest no tiene campo chatbot_id pero el endpoint lo requiere
2. Endpoint de chatbots devuelve error 500
3. Problemas de esquemas y modelos
"""

import os
import shutil
from datetime import datetime

def backup_file(file_path):
    """Crear backup de un archivo"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        return backup_path
    return None

def fix_chat_request_schema():
    """Corregir el esquema ChatRequest para incluir chatbot_id"""
    print("\n🔧 CORRIGIENDO ESQUEMA CHATREQUEST...")
    
    schema_file = "backend/src/schemas/conversation.py"
    
    if not os.path.exists(schema_file):
        print(f"❌ Archivo no encontrado: {schema_file}")
        return False
    
    # Crear backup
    backup_file(schema_file)
    
    # Leer archivo actual
    with open(schema_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y reemplazar ChatRequest
    old_chat_request = '''class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID")
    session_id: str = Field(..., description="Session ID")
    user_info: Optional[Dict[str, Any]] = Field(None, description="Anonymous user info")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    stream: bool = Field(default=False, description="Enable streaming response")'''
    
    new_chat_request = '''class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID")
    chatbot_id: Optional[int] = Field(None, description="Chatbot ID (required for new conversations)")
    session_id: str = Field(..., description="Session ID")
    user_info: Optional[Dict[str, Any]] = Field(None, description="Anonymous user info")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    stream: bool = Field(default=False, description="Enable streaming response")'''
    
    if old_chat_request in content:
        content = content.replace(old_chat_request, new_chat_request)
        
        # Escribir archivo corregido
        with open(schema_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ ChatRequest schema corregido")
        return True
    else:
        print("⚠️ No se encontró el patrón exacto de ChatRequest")
        return False

def fix_chatbots_endpoint():
    """Corregir el endpoint de chatbots que devuelve error 500"""
    print("\n🔧 CORRIGIENDO ENDPOINT DE CHATBOTS...")
    
    endpoint_file = "backend/src/api/v1/endpoints/chatbots.py"
    
    if not os.path.exists(endpoint_file):
        print(f"❌ Archivo no encontrado: {endpoint_file}")
        return False
    
    # Crear backup
    backup_file(endpoint_file)
    
    # Leer archivo actual
    with open(endpoint_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y reemplazar el endpoint problemático
    old_endpoint = '''        return {
            "chatbots": chatbots,
            "total": total,
            "skip": skip,
            "limit": limit
        }'''
    
    new_endpoint = '''        # Calcular páginas
        pages = (total + limit - 1) // limit if limit > 0 else 1
        page = (skip // limit) + 1 if limit > 0 else 1
        
        return ChatbotList(
            chatbots=chatbots,
            total=total,
            page=page,
            per_page=limit,
            pages=pages
        )'''
    
    if old_endpoint in content:
        content = content.replace(old_endpoint, new_endpoint)
        
        # Escribir archivo corregido
        with open(endpoint_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Endpoint de chatbots corregido")
        return True
    else:
        print("⚠️ No se encontró el patrón exacto del endpoint")
        return False

def fix_chat_endpoint_logic():
    """Corregir la lógica del endpoint de chat para manejar chatbot_id opcional"""
    print("\n🔧 CORRIGIENDO LÓGICA DEL ENDPOINT DE CHAT...")
    
    endpoint_file = "backend/src/api/v1/endpoints/conversations.py"
    
    if not os.path.exists(endpoint_file):
        print(f"❌ Archivo no encontrado: {endpoint_file}")
        return False
    
    # Crear backup
    backup_file(endpoint_file)
    
    # Leer archivo actual
    with open(endpoint_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y reemplazar la lógica problemática
    old_logic = '''        if not conversation:
            # Create new conversation
            chatbot = db.query(Chatbot).filter(
                Chatbot.id == chat_request.chatbot_id,
                Chatbot.is_active == True
            ).first()
            
            if not chatbot:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chatbot not found or inactive"
                )
            
            conversation = Conversation(
                chatbot_id=chat_request.chatbot_id,
                user_id=current_user.id if current_user else None,
                session_id=chat_request.session_id,
                title="New Conversation"
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)'''
    
    new_logic = '''        if not conversation:
            # Create new conversation - require chatbot_id for new conversations
            if not chat_request.chatbot_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="chatbot_id is required for new conversations"
                )
            
            chatbot = db.query(Chatbot).filter(
                Chatbot.id == chat_request.chatbot_id,
                Chatbot.is_active == True
            ).first()
            
            if not chatbot:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chatbot not found or inactive"
                )
            
            # Check if user has access to this chatbot
            if current_user and current_user.organization_id != chatbot.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this chatbot"
                )
            
            conversation = Conversation(
                chatbot_id=chat_request.chatbot_id,
                user_id=current_user.id if current_user else None,
                session_id=chat_request.session_id,
                title="New Conversation"
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)'''
    
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        
        # Escribir archivo corregido
        with open(endpoint_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Lógica del endpoint de chat corregida")
        return True
    else:
        print("⚠️ No se encontró el patrón exacto de la lógica de chat")
        return False

def create_test_script():
    """Crear script de prueba actualizado"""
    print("\n📝 CREANDO SCRIPT DE PRUEBA ACTUALIZADO...")
    
    test_script = '''#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones en VersaAI
"""

import requests
import json
import uuid
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test1@versaai.com"
TEST_PASSWORD = "test123456"

def get_auth_token():
    """Obtener token de autenticación"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_chatbots_fixed(token):
    """Probar endpoint de chatbots corregido"""
    print("\n🤖 PROBANDO ENDPOINT DE CHATBOTS CORREGIDO...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/chatbots/", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chatbots endpoint funcional")
            print(f"Total chatbots: {data.get('total', 0)}")
            print(f"Página: {data.get('page', 1)} de {data.get('pages', 1)}")
            return True, data.get('chatbots', [])
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False, []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def test_chat_fixed(token, chatbots):
    """Probar chat con chatbot_id correcto"""
    print("\n💬 PROBANDO CHAT CORREGIDO...")
    
    if not chatbots:
        print("❌ No hay chatbots disponibles para probar")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    chatbot_id = chatbots[0].get('id', 1)
    session_id = str(uuid.uuid4())
    
    chat_data = {
        "message": "Hola, esta es una prueba del chat corregido",
        "chatbot_id": chatbot_id,
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/conversations/chat",
            headers=headers,
            json=chat_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat funcional")
            print(f"Respuesta: {data.get('message', '')[:100]}...")
            print(f"Conversation ID: {data.get('conversation_id')}")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 PROBANDO CORRECCIONES VERSAAI")
    print("=" * 50)
    
    # Obtener token
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    print(f"✅ Token obtenido")
    
    # Probar chatbots
    chatbots_ok, chatbots = test_chatbots_fixed(token)
    
    # Probar chat
    chat_ok = test_chat_fixed(token, chatbots)
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"✅ Chatbots: {'FUNCIONAL' if chatbots_ok else 'ERROR'}")
    print(f"✅ Chat: {'FUNCIONAL' if chat_ok else 'ERROR'}")
    
    if chatbots_ok and chat_ok:
        print("\n🎉 ¡TODAS LAS CORRECCIONES FUNCIONAN!")
    else:
        print("\n⚠️ Algunas correcciones necesitan más trabajo")

if __name__ == "__main__":
    main()
'''
    
    with open('test_corrections.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Script de prueba creado: test_corrections.py")

def main():
    """Función principal"""
    print("🔧 INICIANDO CORRECCIÓN DE ERRORES CRÍTICOS VERSAAI")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('backend/src'):
        print("❌ No se encuentra el directorio backend/src")
        print("   Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return
    
    corrections_made = []
    
    # Corregir ChatRequest schema
    if fix_chat_request_schema():
        corrections_made.append("ChatRequest schema")
    
    # Corregir endpoint de chatbots
    if fix_chatbots_endpoint():
        corrections_made.append("Chatbots endpoint")
    
    # Corregir lógica del chat
    if fix_chat_endpoint_logic():
        corrections_made.append("Chat endpoint logic")
    
    # Crear script de prueba
    create_test_script()
    corrections_made.append("Test script")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CORRECCIONES:")
    print("=" * 60)
    
    if corrections_made:
        print("✅ Correcciones aplicadas:")
        for correction in corrections_made:
            print(f"   - {correction}")
        
        print("\n🔄 PRÓXIMOS PASOS:")
        print("1. Reinicia el servidor backend para aplicar los cambios")
        print("2. Ejecuta 'python test_corrections.py' para verificar las correcciones")
        print("3. Si hay errores, revisa los archivos de backup creados")
        
        print("\n💡 COMANDOS SUGERIDOS:")
        print("   # Reiniciar backend (en terminal backend):")
        print("   Ctrl+C (para detener)")
        print("   python start_server.py")
        print("   ")
        print("   # Probar correcciones:")
        print("   python test_corrections.py")
        
    else:
        print("⚠️ No se pudieron aplicar las correcciones")
        print("   Revisa los mensajes de error anteriores")
    
    print("\n🎯 Las correcciones están listas para ser probadas")

if __name__ == "__main__":
    main()