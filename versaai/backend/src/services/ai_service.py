from typing import List, Dict, Any, Optional, Tuple
import asyncio
import json
import logging
from datetime import datetime, timedelta
import hashlib
import re
from groq import Groq
import openai
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models.chatbot import Chatbot
from ..models.conversation import Conversation, Message
from .vector_service import VectorService
from ..core.cache import cache_manager

logger = logging.getLogger(__name__)

class AIService:
    """Servicio para integración con IA y generación de respuestas"""
    
    def __init__(self):
        self.groq_client = None
        self.openai_client = None
        self.vector_service = VectorService()
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Inicializa los clientes de IA"""
        try:
            if settings.GROQ_API_KEY:
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info("Groq client initialized successfully")
            
            if settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
                self.openai_client = openai
                logger.info("OpenAI client initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing AI clients: {e}")
    
    async def generate_response(
        self,
        chatbot_id: int,
        message: str,
        conversation_id: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """Genera una respuesta usando IA"""
        try:
            # Obtener configuración del chatbot
            chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
            if not chatbot:
                raise ValueError(f"Chatbot {chatbot_id} not found")
            
            # Verificar caché
            cache_key = self._generate_cache_key(chatbot_id, message, context)
            cached_response = await cache_manager.get(cache_key)
            if cached_response:
                return json.loads(cached_response)
            
            # Obtener contexto RAG
            rag_context = await self._get_rag_context(chatbot_id, message)
            
            # Construir contexto de conversación
            conversation_context = await self._build_conversation_context(
                conversation_id, db
            )
            
            # Generar respuesta
            response = await self._generate_ai_response(
                chatbot, message, rag_context, conversation_context, context
            )
            
            # Procesar y enriquecer respuesta
            processed_response = await self._process_response(
                response, chatbot, message
            )
            
            # Guardar en caché
            await cache_manager.set(
                cache_key, 
                json.dumps(processed_response),
                expire=3600  # 1 hora
            )
            
            return processed_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return {
                "response": "Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo.",
                "confidence": 0.0,
                "sources": [],
                "intent": "error",
                "entities": [],
                "error": str(e)
            }
    
    async def train_model(
        self,
        chatbot_id: int,
        training_data: List[Dict[str, Any]],
        db: Session
    ) -> Dict[str, Any]:
        """Entrena el modelo con nuevos datos"""
        try:
            chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
            if not chatbot:
                raise ValueError(f"Chatbot {chatbot_id} not found")
            
            # Procesar datos de entrenamiento
            processed_data = await self._process_training_data(training_data)
            
            # Actualizar base de conocimiento vectorial
            vector_stats = await self.vector_service.add_documents(
                chatbot_id, processed_data
            )
            
            # Actualizar configuración del chatbot
            training_config = {
                "last_training": datetime.utcnow().isoformat(),
                "training_data_count": len(processed_data),
                "vector_stats": vector_stats
            }
            
            # Actualizar configuración en la base de datos
            current_config = chatbot.configuration or {}
            current_config.update(training_config)
            chatbot.configuration = current_config
            chatbot.status = "trained"
            
            db.commit()
            
            return {
                "success": True,
                "message": "Modelo entrenado exitosamente",
                "training_stats": training_config
            }
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def deploy_model(
        self,
        chatbot_id: int,
        deployment_config: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """Despliega el modelo entrenado"""
        try:
            chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
            if not chatbot:
                raise ValueError(f"Chatbot {chatbot_id} not found")
            
            if chatbot.status != "trained":
                raise ValueError("El chatbot debe estar entrenado antes del despliegue")
            
            # Validar configuración de despliegue
            validated_config = self._validate_deployment_config(deployment_config)
            
            # Actualizar configuración del chatbot
            current_config = chatbot.configuration or {}
            current_config.update({
                "deployment": validated_config,
                "deployed_at": datetime.utcnow().isoformat(),
                "deployment_version": self._generate_version_hash(chatbot_id)
            })
            
            chatbot.configuration = current_config
            chatbot.status = "deployed"
            chatbot.is_active = True
            
            db.commit()
            
            return {
                "success": True,
                "message": "Modelo desplegado exitosamente",
                "deployment_url": f"/api/v1/chat/{chatbot_id}",
                "widget_code": self._generate_widget_code(chatbot_id)
            }
            
        except Exception as e:
            logger.error(f"Error deploying model: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_rag_context(
        self, 
        chatbot_id: int, 
        query: str, 
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Obtiene contexto relevante usando RAG"""
        try:
            return await self.vector_service.search_similar(
                chatbot_id, query, max_results
            )
        except Exception as e:
            logger.error(f"Error getting RAG context: {e}")
            return []
    
    async def _build_conversation_context(
        self,
        conversation_id: Optional[int],
        db: Session,
        max_messages: int = 10
    ) -> List[Dict[str, str]]:
        """Construye el contexto de la conversación"""
        if not conversation_id:
            return []
        
        try:
            messages = db.query(Message).filter(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.desc()).limit(max_messages).all()
            
            context = []
            for msg in reversed(messages):
                context.append({
                    "role": "user" if msg.is_from_user else "assistant",
                    "content": msg.content
                })
            
            return context
            
        except Exception as e:
            logger.error(f"Error building conversation context: {e}")
            return []
    
    async def _generate_ai_response(
        self,
        chatbot: Chatbot,
        message: str,
        rag_context: List[Dict[str, Any]],
        conversation_context: List[Dict[str, str]],
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Genera respuesta usando el modelo de IA"""
        try:
            # Construir prompt
            system_prompt = self._build_system_prompt(
                chatbot, rag_context, additional_context
            )
            
            # Preparar mensajes
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Agregar contexto de conversación
            messages.extend(conversation_context[-5:])  # Últimos 5 mensajes
            
            # Agregar mensaje actual
            messages.append({"role": "user", "content": message})
            
            # Generar respuesta con Groq
            if self.groq_client:
                response = await self._generate_groq_response(messages, chatbot)
            elif self.openai_client:
                response = await self._generate_openai_response(messages, chatbot)
            else:
                raise ValueError("No AI client available")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return "Lo siento, no puedo procesar tu solicitud en este momento."
    
    async def _generate_groq_response(
        self, 
        messages: List[Dict[str, str]], 
        chatbot: Chatbot
    ) -> str:
        """Genera respuesta usando Groq"""
        try:
            config = chatbot.configuration or {}
            model = config.get("model", settings.GROQ_MODEL or "mixtral-8x7b-32768")
            
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=config.get("max_tokens", 1000),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 0.9),
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error with Groq API: {e}")
            raise
    
    async def _generate_openai_response(
        self, 
        messages: List[Dict[str, str]], 
        chatbot: Chatbot
    ) -> str:
        """Genera respuesta usando OpenAI"""
        try:
            config = chatbot.configuration or {}
            model = config.get("model", "gpt-3.5-turbo")
            
            response = await self.openai_client.ChatCompletion.acreate(
                model=model,
                messages=messages,
                max_tokens=config.get("max_tokens", 1000),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 0.9)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error with OpenAI API: {e}")
            raise
    
    def _build_system_prompt(
        self,
        chatbot: Chatbot,
        rag_context: List[Dict[str, Any]],
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Construye el prompt del sistema"""
        base_prompt = f"""
Eres {chatbot.name}, un asistente de IA especializado.

Descripción: {chatbot.description}

Instrucciones:
- Responde de manera útil y precisa
- Mantén un tono profesional pero amigable
- Si no sabes algo, admítelo honestamente
- Usa la información del contexto cuando sea relevante
"""
        
        # Agregar contexto RAG
        if rag_context:
            base_prompt += "\n\nContexto relevante:\n"
            for i, ctx in enumerate(rag_context[:3], 1):
                base_prompt += f"{i}. {ctx.get('content', '')}\n"
        
        # Agregar contexto adicional
        if additional_context:
            base_prompt += f"\n\nInformación adicional: {json.dumps(additional_context, ensure_ascii=False)}\n"
        
        return base_prompt
    
    async def _process_response(
        self,
        response: str,
        chatbot: Chatbot,
        original_message: str
    ) -> Dict[str, Any]:
        """Procesa y enriquece la respuesta"""
        try:
            # Extraer entidades
            entities = await self._extract_entities(original_message)
            
            # Clasificar intención
            intent = await self._classify_intent(original_message)
            
            # Calcular confianza (simplificado)
            confidence = self._calculate_confidence(response, original_message)
            
            return {
                "response": response.strip(),
                "confidence": confidence,
                "intent": intent,
                "entities": entities,
                "sources": [],  # Se puede implementar tracking de fuentes
                "metadata": {
                    "model": chatbot.configuration.get("model", "unknown"),
                    "processing_time": 0,  # Se puede medir tiempo real
                    "tokens_used": len(response.split())
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            return {
                "response": response,
                "confidence": 0.5,
                "intent": "unknown",
                "entities": [],
                "sources": [],
                "metadata": {}
            }
    
    async def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extrae entidades del texto"""
        entities = []
        
        # Extraer emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        for email in emails:
            entities.append({"type": "email", "value": email})
        
        # Extraer números de teléfono (patrón simple)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            entities.append({"type": "phone", "value": phone})
        
        # Extraer fechas (patrón simple)
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
        dates = re.findall(date_pattern, text)
        for date in dates:
            entities.append({"type": "date", "value": date})
        
        return entities
    
    async def _classify_intent(self, text: str) -> str:
        """Clasifica la intención del mensaje"""
        text_lower = text.lower()
        
        # Intenciones básicas
        if any(word in text_lower for word in ['hola', 'buenos días', 'buenas tardes']):
            return 'greeting'
        elif any(word in text_lower for word in ['adiós', 'hasta luego', 'chao']):
            return 'goodbye'
        elif any(word in text_lower for word in ['ayuda', 'help', 'soporte']):
            return 'help_request'
        elif '?' in text:
            return 'question'
        else:
            return 'general'
    
    def _calculate_confidence(self, response: str, original_message: str) -> float:
        """Calcula la confianza de la respuesta (simplificado)"""
        # Implementación básica - se puede mejorar con ML
        if len(response) < 10:
            return 0.3
        elif "no sé" in response.lower() or "no puedo" in response.lower():
            return 0.4
        elif len(response) > 50:
            return 0.8
        else:
            return 0.6
    
    async def _process_training_data(
        self, 
        training_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Procesa los datos de entrenamiento"""
        processed = []
        
        for item in training_data:
            if isinstance(item, dict) and 'content' in item:
                processed.append({
                    'content': item['content'],
                    'metadata': item.get('metadata', {}),
                    'type': item.get('type', 'text')
                })
        
        return processed
    
    def _validate_deployment_config(
        self, 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Valida la configuración de despliegue"""
        validated = {
            'environment': config.get('environment', 'production'),
            'max_concurrent_users': min(config.get('max_concurrent_users', 100), 1000),
            'response_timeout': min(config.get('response_timeout', 30), 60),
            'rate_limit': min(config.get('rate_limit', 60), 300)
        }
        
        return validated
    
    def _generate_version_hash(self, chatbot_id: int) -> str:
        """Genera un hash de versión para el despliegue"""
        timestamp = datetime.utcnow().isoformat()
        content = f"{chatbot_id}-{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _generate_widget_code(self, chatbot_id: int) -> str:
        """Genera el código del widget embebible"""
        return f"""
<script>
(function() {{
    var script = document.createElement('script');
    script.src = '{settings.FRONTEND_URL}/widget.js';
    script.setAttribute('data-chatbot-id', '{chatbot_id}');
    document.head.appendChild(script);
}})();
</script>
"""
    
    def _generate_cache_key(
        self,
        chatbot_id: int,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Genera clave de caché para respuestas"""
        content = f"{chatbot_id}-{message}"
        if context:
            content += f"-{json.dumps(context, sort_keys=True)}"
        
        return f"ai_response:{hashlib.md5(content.encode()).hexdigest()}"
    
    async def get_model_stats(
        self, 
        chatbot_id: int, 
        db: Session
    ) -> Dict[str, Any]:
        """Obtiene estadísticas del modelo"""
        try:
            chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
            if not chatbot:
                return {}
            
            # Estadísticas básicas
            total_conversations = db.query(Conversation).filter(
                Conversation.chatbot_id == chatbot_id
            ).count()
            
            total_messages = db.query(Message).join(Conversation).filter(
                Conversation.chatbot_id == chatbot_id
            ).count()
            
            # Estadísticas del vector store
            vector_stats = await self.vector_service.get_stats(chatbot_id)
            
            return {
                "chatbot_id": chatbot_id,
                "status": chatbot.status,
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "vector_stats": vector_stats,
                "last_training": chatbot.configuration.get("last_training"),
                "deployment_version": chatbot.configuration.get("deployment_version")
            }
            
        except Exception as e:
            logger.error(f"Error getting model stats: {e}")
            return {}

# Instancia global del servicio
ai_service = AIService()