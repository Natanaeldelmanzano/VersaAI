from typing import List, Dict, Optional, AsyncGenerator
from groq import Groq
from ..core.config import settings
import logging
import time
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set. Groq service will not work properly.")
            self.client = None
        else:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        
        self.default_model = settings.GROQ_MODEL
        self.default_temperature = settings.DEFAULT_TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
    
    def is_available(self) -> bool:
        """Check if Groq service is available"""
        return self.client is not None
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> Dict:
        """Generate a response using Groq API"""
        
        if not self.is_available():
            raise Exception("Groq service is not available. Please check your API key.")
        
        # Use defaults if not provided
        model = model or self.default_model
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens or self.max_tokens
        
        # Prepare messages
        formatted_messages = []
        
        # Add system prompt if provided
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation messages
        formatted_messages.extend(messages)
        
        try:
            start_time = time.time()
            
            # Make API call
            response = self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=False
            )
            
            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)
            
            # Extract response data
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            
            # Get usage information
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            total_tokens = usage.total_tokens if usage else 0
            
            result = {
                "content": content,
                "model": model,
                "finish_reason": finish_reason,
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens
                },
                "response_time_ms": response_time_ms,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Groq API call successful. Model: {model}, Tokens: {total_tokens}, Time: {response_time_ms}ms")
            return result
            
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[Dict, None]:
        """Generate a streaming response using Groq API"""
        
        if not self.is_available():
            raise Exception("Groq service is not available. Please check your API key.")
        
        # Use defaults if not provided
        model = model or self.default_model
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens or self.max_tokens
        
        # Prepare messages
        formatted_messages = []
        
        # Add system prompt if provided
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation messages
        formatted_messages.extend(messages)
        
        try:
            start_time = time.time()
            
            # Make streaming API call
            stream = self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=True
            )
            
            full_content = ""
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content_delta = chunk.choices[0].delta.content
                    full_content += content_delta
                    
                    yield {
                        "type": "content_delta",
                        "content": content_delta,
                        "full_content": full_content
                    }
                
                # Check if stream is done
                if chunk.choices[0].finish_reason is not None:
                    end_time = time.time()
                    response_time_ms = int((end_time - start_time) * 1000)
                    
                    yield {
                        "type": "done",
                        "content": full_content,
                        "finish_reason": chunk.choices[0].finish_reason,
                        "model": model,
                        "response_time_ms": response_time_ms,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    break
            
            logger.info(f"Groq streaming API call successful. Model: {model}, Time: {response_time_ms}ms")
            
        except Exception as e:
            logger.error(f"Error calling Groq streaming API: {e}")
            yield {
                "type": "error",
                "error": str(e)
            }
    
    async def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate a summary of the given text"""
        
        system_prompt = f"""Eres un asistente que genera resúmenes concisos y precisos. 
        Genera un resumen del texto proporcionado en máximo {max_length} caracteres.
        El resumen debe capturar los puntos principales y ser fácil de entender."""
        
        messages = [
            {
                "role": "user",
                "content": f"Resume el siguiente texto:\n\n{text}"
            }
        ]
        
        try:
            response = await self.generate_response(
                messages=messages,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=100
            )
            
            summary = response["content"].strip()
            
            # Truncate if too long
            if len(summary) > max_length:
                summary = summary[:max_length-3] + "..."
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Error al generar resumen"
    
    async def generate_title(self, conversation_messages: List[str]) -> str:
        """Generate a title for a conversation"""
        
        # Take first few messages to generate title
        context = " ".join(conversation_messages[:3])
        
        system_prompt = """Eres un asistente que genera títulos concisos para conversaciones.
        Genera un título descriptivo de máximo 50 caracteres basado en el contenido de la conversación.
        El título debe ser claro y representativo del tema principal."""
        
        messages = [
            {
                "role": "user",
                "content": f"Genera un título para esta conversación:\n\n{context}"
            }
        ]
        
        try:
            response = await self.generate_response(
                messages=messages,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=50
            )
            
            title = response["content"].strip().replace('"', '').replace("'", "")
            
            # Truncate if too long
            if len(title) > 50:
                title = title[:47] + "..."
            
            return title
            
        except Exception as e:
            logger.error(f"Error generating title: {e}")
            return "Conversación"
    
    def get_available_models(self) -> List[str]:
        """Get list of available Groq models"""
        return [
            "mixtral-8x7b-32768",
            "llama2-70b-4096",
            "gemma-7b-it",
            "llama3-8b-8192",
            "llama3-70b-8192"
        ]
    
    def validate_model(self, model: str) -> bool:
        """Validate if model is available"""
        return model in self.get_available_models()

# Global instance
groq_service = GroqService()