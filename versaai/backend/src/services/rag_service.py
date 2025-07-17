from typing import List, Dict, Optional, Tuple
# from sentence_transformers import SentenceTransformer  # Commented out - causes CUDA downloads
from sqlalchemy.orm import Session
from ..models.knowledge_base import KnowledgeBase, Document, DocumentChunk
from ..models.chatbot import Chatbot
from .groq_service import groq_service
import numpy as np
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.embedding_model = None
        self.model_name = "all-MiniLM-L6-v2"
        self._load_embedding_model()
    
    def _load_embedding_model(self):
        """Load the sentence transformer model"""
        try:
            # self.embedding_model = SentenceTransformer(self.model_name)  # Commented out - causes CUDA downloads
            logger.info(f"Embedding model {self.model_name} temporarily disabled")
            self.embedding_model = None  # Temporarily disabled
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.embedding_model = None
    
    def is_available(self) -> bool:
        """Check if RAG service is available"""
        return self.embedding_model is not None
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a text"""
        if not self.is_available():
            logger.error("Embedding model not available")
            return None
        
        try:
            # Clean and prepare text
            text = text.strip()
            if not text:
                return None
            
            # Generate embedding
            # embedding = self.embedding_model.encode(text)  # Commented out - model disabled
            # return embedding.tolist()
            logger.warning("Embedding generation temporarily disabled")
            return None  # Temporarily return None
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def search_similar_chunks(
        self, 
        db: Session, 
        knowledge_base_id: int, 
        query: str, 
        top_k: int = 5,
        min_similarity: float = 0.3
    ) -> List[Tuple[DocumentChunk, float]]:
        """Search for similar chunks in the knowledge base"""
        
        if not self.is_available():
            logger.error("RAG service not available")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return []
            
            # Get all chunks from the knowledge base
            chunks = db.query(DocumentChunk).join(Document).filter(
                Document.knowledge_base_id == knowledge_base_id,
                DocumentChunk.embedding.isnot(None)
            ).all()
            
            if not chunks:
                logger.info(f"No chunks found in knowledge base {knowledge_base_id}")
                return []
            
            # Calculate similarities
            similarities = []
            for chunk in chunks:
                try:
                    chunk_embedding = chunk.embedding
                    if chunk_embedding:
                        similarity = self.calculate_similarity(query_embedding, chunk_embedding)
                        if similarity >= min_similarity:
                            similarities.append((chunk, similarity))
                except Exception as e:
                    logger.warning(f"Error calculating similarity for chunk {chunk.id}: {e}")
                    continue
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"Error searching similar chunks: {e}")
            return []
    
    def build_context(
        self, 
        similar_chunks: List[Tuple[DocumentChunk, float]], 
        max_context_length: int = 3000
    ) -> Tuple[str, List[Dict]]:
        """Build context from similar chunks"""
        
        context_parts = []
        sources = []
        current_length = 0
        
        for chunk, similarity in similar_chunks:
            chunk_text = chunk.content
            chunk_length = len(chunk_text)
            
            # Check if adding this chunk would exceed max length
            if current_length + chunk_length > max_context_length:
                # Try to add partial content
                remaining_length = max_context_length - current_length
                if remaining_length > 100:  # Only add if we have reasonable space
                    chunk_text = chunk_text[:remaining_length-3] + "..."
                    context_parts.append(chunk_text)
                break
            
            context_parts.append(chunk_text)
            current_length += chunk_length
            
            # Add source information
            sources.append({
                "document_id": chunk.document_id,
                "document_title": chunk.document.title or chunk.document.filename,
                "chunk_id": chunk.id,
                "similarity": similarity,
                "content_preview": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text
            })
        
        context = "\n\n".join(context_parts)
        return context, sources
    
    async def generate_rag_response(
        self,
        db: Session,
        chatbot: Chatbot,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        max_context_length: int = 3000
    ) -> Dict:
        """Generate a RAG-enhanced response"""
        
        try:
            # Initialize response data
            response_data = {
                "content": "",
                "sources": [],
                "context_used": "",
                "model": chatbot.model_name,
                "error": None
            }
            
            # Check if chatbot has knowledge base
            if not chatbot.knowledge_base_id:
                logger.info(f"Chatbot {chatbot.id} has no knowledge base, using direct AI response")
                # Generate response without RAG
                messages = conversation_history or []
                messages.append({"role": "user", "content": user_message})
                
                ai_response = await groq_service.generate_response(
                    messages=messages,
                    model=chatbot.model_name,
                    temperature=chatbot.temperature,
                    max_tokens=chatbot.max_tokens,
                    system_prompt=chatbot.system_prompt
                )
                
                response_data.update(ai_response)
                return response_data
            
            # Search for relevant chunks
            similar_chunks = self.search_similar_chunks(
                db=db,
                knowledge_base_id=chatbot.knowledge_base_id,
                query=user_message,
                top_k=5
            )
            
            # Build context from similar chunks
            context, sources = self.build_context(similar_chunks, max_context_length)
            
            # Prepare system prompt with context
            base_system_prompt = chatbot.system_prompt or "Eres un asistente útil y amigable."
            
            if context:
                rag_system_prompt = f"""{base_system_prompt}

Utiliza la siguiente información de contexto para responder las preguntas del usuario. Si la información del contexto no es suficiente para responder la pregunta, indícalo claramente y proporciona la mejor respuesta posible basada en tu conocimiento general.

Contexto:
{context}

Instrucciones:
- Responde basándote principalmente en el contexto proporcionado
- Si el contexto no contiene información relevante, menciona que no tienes información específica sobre ese tema
- Sé preciso y útil en tus respuestas
- Mantén un tono amigable y profesional"""
            else:
                rag_system_prompt = f"""{base_system_prompt}

No se encontró información específica en la base de conocimiento para esta consulta. Responde basándote en tu conocimiento general y menciona que no tienes información específica sobre este tema en la base de datos."""
            
            # Prepare conversation messages
            messages = conversation_history or []
            messages.append({"role": "user", "content": user_message})
            
            # Generate AI response
            ai_response = await groq_service.generate_response(
                messages=messages,
                model=chatbot.model_name,
                temperature=chatbot.temperature,
                max_tokens=chatbot.max_tokens,
                system_prompt=rag_system_prompt
            )
            
            # Update response data
            response_data.update(ai_response)
            response_data["sources"] = sources
            response_data["context_used"] = context
            
            logger.info(f"RAG response generated successfully. Sources: {len(sources)}")
            return response_data
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            response_data["error"] = str(e)
            response_data["content"] = "Lo siento, ocurrió un error al procesar tu consulta. Por favor, inténtalo de nuevo."
            return response_data
    
    async def generate_streaming_rag_response(
        self,
        db: Session,
        chatbot: Chatbot,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        max_context_length: int = 3000
    ):
        """Generate a streaming RAG-enhanced response"""
        
        try:
            # Search for relevant chunks
            similar_chunks = self.search_similar_chunks(
                db=db,
                knowledge_base_id=chatbot.knowledge_base_id or 0,
                query=user_message,
                top_k=5
            )
            
            # Build context from similar chunks
            context, sources = self.build_context(similar_chunks, max_context_length)
            
            # Send sources first
            yield {
                "type": "sources",
                "sources": sources,
                "context_length": len(context)
            }
            
            # Prepare system prompt with context
            base_system_prompt = chatbot.system_prompt or "Eres un asistente útil y amigable."
            
            if context:
                rag_system_prompt = f"""{base_system_prompt}

Utiliza la siguiente información de contexto para responder las preguntas del usuario:

Contexto:
{context}

Instrucciones:
- Responde basándote principalmente en el contexto proporcionado
- Si el contexto no contiene información relevante, indícalo claramente
- Sé preciso y útil en tus respuestas"""
            else:
                rag_system_prompt = base_system_prompt
            
            # Prepare conversation messages
            messages = conversation_history or []
            messages.append({"role": "user", "content": user_message})
            
            # Generate streaming AI response
            async for chunk in groq_service.generate_streaming_response(
                messages=messages,
                model=chatbot.model_name,
                temperature=chatbot.temperature,
                max_tokens=chatbot.max_tokens,
                system_prompt=rag_system_prompt
            ):
                yield chunk
            
        except Exception as e:
            logger.error(f"Error generating streaming RAG response: {e}")
            yield {
                "type": "error",
                "error": str(e)
            }

# Global instance
rag_service = RAGService()