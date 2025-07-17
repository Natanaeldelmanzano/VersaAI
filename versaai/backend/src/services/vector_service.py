from typing import List, Dict, Any, Optional
import asyncio
import json
import numpy as np
from datetime import datetime
import hashlib
# from sentence_transformers import SentenceTransformer
# import faiss
import pickle
import os

from src.core.config import settings
from src.utils.logger import get_logger
from src.utils.cache import cache_manager

logger = get_logger(__name__)

class VectorService:
    def __init__(self):
        self.model = None
        self.indexes = {}  # Store FAISS indexes per chatbot
        self.documents = {}  # Store document metadata per chatbot
        self.embedding_dim = 384  # Default for all-MiniLM-L6-v2
        self._initialize_model()
    
    def _initialize_model(self):
        """
        Initialize sentence transformer model
        """
        try:
            # Temporarily disabled - sentence_transformers dependency issue
            # model_name = settings.EMBEDDING_MODEL or 'all-MiniLM-L6-v2'
            # self.model = SentenceTransformer(model_name)
            # self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Vector model temporarily disabled")
            self.model = None
        except Exception as e:
            logger.error(f"Failed to initialize vector model: {str(e)}")
            # Fallback to a simple embedding method
            self.model = None
    
    async def create_embeddings(
        self,
        chatbot_id: int,
        training_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create embeddings for training data
        """
        try:
            logger.info(f"Creating embeddings for chatbot {chatbot_id}")
            
            # Extract text chunks
            text_chunks = training_data.get('text_chunks', [])
            qa_pairs = training_data.get('qa_pairs', [])
            
            # Combine all text for embedding
            all_texts = []
            all_metadata = []
            
            # Process text chunks
            for i, chunk in enumerate(text_chunks):
                if isinstance(chunk, dict):
                    text = chunk.get('content', '')
                    metadata = chunk.get('metadata', {})
                else:
                    text = str(chunk)
                    metadata = {}
                
                if text.strip():
                    all_texts.append(text)
                    all_metadata.append({
                        'type': 'text_chunk',
                        'index': i,
                        'chatbot_id': chatbot_id,
                        **metadata
                    })
            
            # Process Q&A pairs
            for i, qa_pair in enumerate(qa_pairs):
                if isinstance(qa_pair, dict):
                    question = qa_pair.get('question', '')
                    answer = qa_pair.get('answer', '')
                    
                    if question.strip():
                        all_texts.append(question)
                        all_metadata.append({
                            'type': 'question',
                            'index': i,
                            'chatbot_id': chatbot_id,
                            'answer': answer
                        })
                    
                    if answer.strip():
                        all_texts.append(answer)
                        all_metadata.append({
                            'type': 'answer',
                            'index': i,
                            'chatbot_id': chatbot_id,
                            'question': question
                        })
            
            if not all_texts:
                logger.warning(f"No text found for embedding creation for chatbot {chatbot_id}")
                return {'count': 0, 'status': 'no_data'}
            
            # Generate embeddings
            embeddings = await self._generate_embeddings(all_texts)
            
            # Create FAISS index
            index = await self._create_faiss_index(embeddings)
            
            # Store index and metadata
            self.indexes[chatbot_id] = index
            self.documents[chatbot_id] = {
                'texts': all_texts,
                'metadata': all_metadata,
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Save to disk - temporarily disabled
            # await self._save_index_to_disk(chatbot_id, index, all_texts, all_metadata)
            
            result = {
                'count': len(all_texts),
                'embedding_dim': self.embedding_dim,
                'index_size': index.ntotal if index else 0,
                'status': 'completed',
                'created_at': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Created {len(all_texts)} embeddings for chatbot {chatbot_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to create embeddings for chatbot {chatbot_id}: {str(e)}")
            raise Exception(f"Embedding creation failed: {str(e)}")
    
    async def search_similar(
        self,
        chatbot_id: int,
        query: str,
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity
        """
        try:
            # Check if index exists
            if chatbot_id not in self.indexes:
                # await self._load_index_from_disk(chatbot_id)
                pass
            
            if chatbot_id not in self.indexes:
                logger.warning(f"No index found for chatbot {chatbot_id}")
                return []
            
            # Generate query embedding
            query_embedding = await self._generate_embeddings([query])
            if not query_embedding:
                return []
            
            # Search in FAISS index
            index = self.indexes[chatbot_id]
            documents = self.documents[chatbot_id]
            
            # Perform similarity search
            scores, indices = index.search(
                query_embedding.astype(np.float32), 
                min(limit * 2, index.ntotal)  # Search more to filter by threshold
            )
            
            # Filter results by threshold and format
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx != -1 and score >= threshold:
                    doc_metadata = documents['metadata'][idx]
                    doc_text = documents['texts'][idx]
                    
                    results.append({
                        'content': doc_text,
                        'metadata': doc_metadata,
                        'similarity_score': float(score),
                        'index': int(idx)
                    })
            
            # Sort by similarity score and limit results
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Failed to search similar documents: {str(e)}")
            return []
    
    async def add_document(
        self,
        chatbot_id: int,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a single document to the vector store
        """
        try:
            # Generate embedding for the document
            embedding = await self._generate_embeddings([content])
            if not embedding:
                raise Exception("Failed to generate embedding")
            
            # Load existing index or create new one
            if chatbot_id not in self.indexes:
                # await self._load_index_from_disk(chatbot_id)
                pass
            
            if chatbot_id not in self.indexes:
                # Create new index
                # index = faiss.IndexFlatIP(self.embedding_dim)
                index = None  # FAISS temporarily disabled
                self.indexes[chatbot_id] = index
                self.documents[chatbot_id] = {
                    'texts': [],
                    'metadata': [],
                    'created_at': datetime.utcnow().isoformat()
                }
            
            # Add to index
            index = self.indexes[chatbot_id]
            documents = self.documents[chatbot_id]
            
            index.add(embedding.astype(np.float32))
            documents['texts'].append(content)
            documents['metadata'].append({
                'chatbot_id': chatbot_id,
                'added_at': datetime.utcnow().isoformat(),
                **(metadata or {})
            })
            
            # Save updated index - temporarily disabled
            # await self._save_index_to_disk(
            #     chatbot_id, 
            #     index, 
            #     documents['texts'], 
            #     documents['metadata']
            # )
            
            return {
                'status': 'added',
                'index': len(documents['texts']) - 1,
                'total_documents': len(documents['texts'])
            }
            
        except Exception as e:
            logger.error(f"Failed to add document: {str(e)}")
            raise Exception(f"Document addition failed: {str(e)}")
    
    async def remove_document(
        self,
        chatbot_id: int,
        document_index: int
    ) -> Dict[str, Any]:
        """
        Remove a document from the vector store
        """
        try:
            if chatbot_id not in self.indexes:
                # await self._load_index_from_disk(chatbot_id)
                pass
            
            if chatbot_id not in self.indexes:
                raise Exception(f"No index found for chatbot {chatbot_id}")
            
            documents = self.documents[chatbot_id]
            
            if document_index >= len(documents['texts']):
                raise Exception("Document index out of range")
            
            # Remove from documents (FAISS doesn't support removal, so we rebuild)
            documents['texts'].pop(document_index)
            documents['metadata'].pop(document_index)
            
            # Rebuild index
            if documents['texts']:
                embeddings = await self._generate_embeddings(documents['texts'])
                index = await self._create_faiss_index(embeddings)
                self.indexes[chatbot_id] = index
            else:
                # Empty index
                # self.indexes[chatbot_id] = faiss.IndexFlatIP(self.embedding_dim)
                self.indexes[chatbot_id] = None  # FAISS temporarily disabled
            
            # Save updated index - temporarily disabled
            # await self._save_index_to_disk(
            #     chatbot_id,
            #     self.indexes[chatbot_id],
            #     documents['texts'],
            #     documents['metadata']
            # )
            
            return {
                'status': 'removed',
                'total_documents': len(documents['texts'])
            }
            
        except Exception as e:
            logger.error(f"Failed to remove document: {str(e)}")
            raise Exception(f"Document removal failed: {str(e)}")
    
    async def get_statistics(
        self,
        chatbot_id: int
    ) -> Dict[str, Any]:
        """
        Get statistics for chatbot's vector store
        """
        try:
            if chatbot_id not in self.indexes:
                # await self._load_index_from_disk(chatbot_id)
                pass
            
            if chatbot_id not in self.indexes:
                return {
                    'total_documents': 0,
                    'embedding_dim': self.embedding_dim,
                    'index_size': 0,
                    'status': 'no_index'
                }
            
            index = self.indexes[chatbot_id]
            documents = self.documents[chatbot_id]
            
            # Calculate statistics
            text_chunks = sum(1 for meta in documents['metadata'] if meta.get('type') == 'text_chunk')
            questions = sum(1 for meta in documents['metadata'] if meta.get('type') == 'question')
            answers = sum(1 for meta in documents['metadata'] if meta.get('type') == 'answer')
            
            return {
                'total_documents': len(documents['texts']),
                'text_chunks': text_chunks,
                'questions': questions,
                'answers': answers,
                'embedding_dim': self.embedding_dim,
                'index_size': index.ntotal,
                'created_at': documents.get('created_at'),
                'status': 'active'
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    async def _generate_embeddings(self, texts: List[str]) -> Optional[np.ndarray]:
        """
        Generate embeddings for a list of texts
        """
        try:
            if not self.model:
                # Fallback to simple hash-based embeddings
                return self._generate_simple_embeddings(texts)
            
            # Use sentence transformer
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            return self._generate_simple_embeddings(texts)
    
    def _generate_simple_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate simple hash-based embeddings as fallback
        """
        embeddings = []
        for text in texts:
            # Create a simple embedding based on text hash and length
            text_hash = hashlib.md5(text.encode()).hexdigest()
            embedding = np.zeros(self.embedding_dim)
            
            # Fill embedding with hash-based values
            for i, char in enumerate(text_hash[:self.embedding_dim//16]):
                idx = i * 16
                if idx < self.embedding_dim:
                    embedding[idx] = ord(char) / 255.0
            
            # Add text length information
            if len(embedding) > 0:
                embedding[0] = min(len(text) / 1000.0, 1.0)
            
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    async def _create_faiss_index(self, embeddings: np.ndarray):
        """
        Create FAISS index from embeddings - TEMPORARILY DISABLED
        """
        logger.warning("FAISS index creation temporarily disabled")
        return None
        # try:
        #     # Use Inner Product index for cosine similarity
        #     index = faiss.IndexFlatIP(self.embedding_dim)
        #     
        #     # Normalize embeddings for cosine similarity
        #     faiss.normalize_L2(embeddings.astype(np.float32))
        #     
        #     # Add embeddings to index
        #     index.add(embeddings.astype(np.float32))
        #     
        #     return index
        #     
        # except Exception as e:
        #     logger.error(f"Failed to create FAISS index: {str(e)}")
        #     raise
    
    # async def _save_index_to_disk(
    #     self,
    #     chatbot_id: int,
    #     index,  # faiss.Index temporarily disabled
    #     texts: List[str],
    #     metadata: List[Dict[str, Any]]
    # ):
    #     """
    #     Save index and documents to disk
    #     """
    #     try:
    #         # Create directory if it doesn't exist
    #         index_dir = os.path.join(settings.DATA_DIR or './data', 'indexes')
    #         os.makedirs(index_dir, exist_ok=True)
    #         
    #         # Save FAISS index - temporarily disabled
    #         # index_path = os.path.join(index_dir, f'chatbot_{chatbot_id}.index')
    #         # faiss.write_index(index, index_path)
    #         
    #         # Save documents and metadata
    #         docs_path = os.path.join(index_dir, f'chatbot_{chatbot_id}_docs.pkl')
    #         with open(docs_path, 'wb') as f:
    #             pickle.dump({
    #                 'texts': texts,
    #                 'metadata': metadata,
    #                 'created_at': datetime.utcnow().isoformat()
    #             }, f)
    #         
    #         logger.info(f"Saved index for chatbot {chatbot_id} to disk")
    #         
    #     except Exception as e:
    #         logger.error(f"Failed to save index to disk: {str(e)}")
    
    # async def _load_index_from_disk(self, chatbot_id: int):
    #     """
    #     Load index and documents from disk
    #     """
    #     try:
    #         index_dir = os.path.join(settings.DATA_DIR or './data', 'indexes')
    #         
    #         # Load FAISS index - temporarily disabled
    #         # index_path = os.path.join(index_dir, f'chatbot_{chatbot_id}.index')
    #         # if not os.path.exists(index_path):
    #         #     return
    #         # index = faiss.read_index(index_path)
    #         index = None
    #         
    #         # Load documents and metadata
    #         docs_path = os.path.join(index_dir, f'chatbot_{chatbot_id}_docs.pkl')
    #         if not os.path.exists(docs_path):
    #             return
    #         
    #         with open(docs_path, 'rb') as f:
    #             docs_data = pickle.load(f)
    #         
    #         self.indexes[chatbot_id] = index
    #         self.documents[chatbot_id] = docs_data
    #         
    #         logger.info(f"Loaded index for chatbot {chatbot_id} from disk")
    #         
    #     except Exception as e:
    #         logger.error(f"Failed to load index from disk: {str(e)}")
    
    async def get_stats(self, chatbot_id: int) -> Dict[str, Any]:
        """Obtiene estadísticas del almacén de vectores"""
        try:
            index_path = self._get_index_path(chatbot_id)
            documents_path = self._get_documents_path(chatbot_id)
            
            stats = {
                "chatbot_id": chatbot_id,
                "index_exists": os.path.exists(index_path),
                "documents_count": 0,
                "index_size": 0,
                "last_updated": None
            }
            
            if os.path.exists(index_path):
                stats["index_size"] = os.path.getsize(index_path)
                stats["last_updated"] = datetime.fromtimestamp(
                    os.path.getmtime(index_path)
                ).isoformat()
            
            if os.path.exists(documents_path):
                with open(documents_path, 'r', encoding='utf-8') as f:
                    documents = json.load(f)
                    stats["documents_count"] = len(documents)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting vector stats: {e}")
            return {"error": str(e)}
    
    def _get_index_path(self, chatbot_id: int) -> str:
        """Obtiene la ruta del archivo de índice"""
        return os.path.join(settings.DATA_DIR or './data', 'indexes', f"chatbot_{chatbot_id}.index")
    
    def _get_documents_path(self, chatbot_id: int) -> str:
        """Obtiene la ruta del archivo de documentos"""
        return os.path.join(settings.DATA_DIR or './data', 'indexes', f"chatbot_{chatbot_id}_docs.pkl")
    
    async def clear_index(self, chatbot_id: int) -> Dict[str, Any]:
        """Limpia el índice de un chatbot específico"""
        try:
            index_path = self._get_index_path(chatbot_id)
            documents_path = self._get_documents_path(chatbot_id)
            
            # Eliminar archivos si existen
            if os.path.exists(index_path):
                os.remove(index_path)
            
            if os.path.exists(documents_path):
                os.remove(documents_path)
            
            # Limpiar caché en memoria
            if chatbot_id in self.indexes:
                del self.indexes[chatbot_id]
            
            if chatbot_id in self.documents:
                del self.documents[chatbot_id]
            
            logger.info(f"Index cleared for chatbot {chatbot_id}")
            return {'status': 'cleared'}
            
        except Exception as e:
            logger.error(f"Error clearing index for chatbot {chatbot_id}: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def update_document(
        self, 
        chatbot_id: int, 
        document_id: str, 
        new_content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Actualiza un documento específico"""
        try:
            # Eliminar documento existente
            await self.remove_document(chatbot_id, int(document_id))
            
            # Agregar documento actualizado
            result = await self.add_document(chatbot_id, new_content, metadata)
            return result["status"] == "added"
            
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {e}")
            return False


# Instancia global del servicio
vector_service = VectorService()