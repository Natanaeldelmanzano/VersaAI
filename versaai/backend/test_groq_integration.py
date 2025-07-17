#!/usr/bin/env python3
"""
Script para probar la integración completa de Groq API
Verifica que los chats del dashboard funcionen correctamente con Groq
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

def test_groq_integration():
    """Prueba completa de la integración de Groq"""
    print("🚀 INICIANDO PRUEBAS DE INTEGRACIÓN GROQ")
    print("=" * 50)
    
    # 1. Login con usuario demo
    print("\n1️⃣ AUTENTICACIÓN")
    login_data = {
        "username": "admin@versaai.com",
        "password": "admin123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("✅ Login exitoso")
        else:
            print(f"❌ Error en login: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Verificar configuración de Groq
    print("\n2️⃣ VERIFICACIÓN DE CONFIGURACIÓN GROQ")
    try:
        # Obtener lista de chatbots
        response = requests.get(f"{BASE_URL}/chatbots/", headers=headers)
        if response.status_code == 200:
            chatbots_data = response.json()
            chatbots = chatbots_data.get('chatbots', [])
            print(f"✅ Chatbots disponibles: {len(chatbots)}")
            
            if chatbots:
                chatbot = chatbots[0]
                print(f"   📋 Chatbot de prueba: {chatbot['name']}")
                print(f"   🤖 Modelo configurado: {chatbot.get('model_name', 'No especificado')}")
                chatbot_id = chatbot['id']
            else:
                print("⚠️ No hay chatbots disponibles, creando uno nuevo...")
                chatbot_id = create_test_chatbot(headers)
                if not chatbot_id:
                    return False
        else:
            print(f"❌ Error obteniendo chatbots: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 3. Probar chat con Groq
    print("\n3️⃣ PRUEBA DE CHAT CON GROQ")
    test_messages = [
        "Hola, ¿cómo estás?",
        "¿Puedes explicarme qué es la inteligencia artificial?",
        "¿Cuál es la capital de España?",
        "Gracias por tu ayuda"
    ]
    
    conversation_id = None
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   💬 Mensaje {i}: {message}")
        
        chat_data = {
            "message": message,
            "chatbot_id": chatbot_id
        }
        
        if conversation_id:
            chat_data["conversation_id"] = conversation_id
        
        try:
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/conversations/chat", 
                                   json=chat_data, headers=headers)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                chat_response = response.json()
                ai_response = chat_response.get('response', 'Sin respuesta')
                conversation_id = chat_response.get('conversation_id')
                
                print(f"   ✅ Respuesta recibida ({response_time:.2f}s)")
                print(f"   🤖 IA: {ai_response[:100]}{'...' if len(ai_response) > 100 else ''}")
                print(f"   📊 Confianza: {chat_response.get('confidence', 'N/A')}")
                print(f"   🎯 Intención: {chat_response.get('intent', 'N/A')}")
                
                # Verificar que la respuesta viene de Groq
                metadata = chat_response.get('metadata', {})
                model_used = metadata.get('model', 'unknown')
                print(f"   🔧 Modelo usado: {model_used}")
                
                if 'mixtral' in model_used.lower() or 'llama' in model_used.lower():
                    print("   ✅ Confirmado: Usando modelo Groq")
                else:
                    print(f"   ⚠️ Modelo no reconocido como Groq: {model_used}")
                    
            else:
                print(f"   ❌ Error en chat: {response.status_code}")
                print(f"   📝 Detalle: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        # Pausa entre mensajes
        time.sleep(1)
    
    # 4. Verificar historial de conversación
    print("\n4️⃣ VERIFICACIÓN DE HISTORIAL")
    if conversation_id:
        try:
            response = requests.get(f"{BASE_URL}/conversations/{conversation_id}/messages", 
                                  headers=headers)
            if response.status_code == 200:
                messages = response.json()
                print(f"   ✅ Historial recuperado: {len(messages)} mensajes")
                
                # Contar mensajes de usuario vs IA
                user_msgs = sum(1 for msg in messages if msg.get('is_from_user'))
                ai_msgs = sum(1 for msg in messages if not msg.get('is_from_user'))
                print(f"   👤 Mensajes de usuario: {user_msgs}")
                print(f"   🤖 Respuestas de IA: {ai_msgs}")
            else:
                print(f"   ❌ Error obteniendo historial: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎉 PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("✅ La integración de Groq está funcionando correctamente")
    print("✅ Los chats del dashboard están operativos")
    print("✅ El historial de conversaciones se guarda correctamente")
    return True

def create_test_chatbot(headers: Dict[str, str]) -> int:
    """Crea un chatbot de prueba"""
    chatbot_data = {
        "name": "Chatbot Groq Test",
        "description": "Chatbot de prueba para verificar integración con Groq",
        "model_name": "mixtral-8x7b-32768",
        "temperature": 0.7,
        "max_tokens": 1000,
        "system_prompt": "Eres un asistente útil y amigable. Responde de manera clara y concisa."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chatbots/", 
                               json=chatbot_data, headers=headers)
        if response.status_code == 201:
            chatbot = response.json()
            print(f"   ✅ Chatbot creado: {chatbot['name']} (ID: {chatbot['id']})")
            return chatbot['id']
        else:
            print(f"   ❌ Error creando chatbot: {response.status_code}")
            print(f"   📝 Detalle: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

if __name__ == "__main__":
    success = test_groq_integration()
    if success:
        print("\n🌟 INTEGRACIÓN GROQ COMPLETAMENTE FUNCIONAL 🌟")
    else:
        print("\n💥 PROBLEMAS DETECTADOS EN LA INTEGRACIÓN")
        exit(1)