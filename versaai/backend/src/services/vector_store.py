from typing import List, Dict, Any, Optional
import logging
import numpy as np
from ..core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    """Simple vector store implementation"""
    
    def __init__(self):
        self.collections = {}
        logger.info("VectorStore initialized")
    
    def create_collection(self, collection_name: str) -> bool:
        """Create a new collection"""
        try:
            if collection_name not in self.collections:
                self.collections[collection_name] = {
                    'vectors': [],
                    'metadata': [],
                    'ids': []
                }
                logger.info(f"Created collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create collection {collection_name}: {e}")
            return False
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection"""
        try:
            if collection_name in self.collections:
                del self.collections[collection_name]
                logger.info(f"Deleted collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection {collection_name}: {e}")
            return False
    
    def add_vectors(self, collection_name: str, vectors: List[List[float]], 
                   metadata: List[Dict[str, Any]], ids: List[str]) -> bool:
        """Add vectors to a collection"""
        try:
            if collection_name not in self.collections:
                self.create_collection(collection_name)
            
            collection = self.collections[collection_name]
            collection['vectors'].extend(vectors)
            collection['metadata'].extend(metadata)
            collection['ids'].extend(ids)
            
            logger.info(f"Added {len(vectors)} vectors to collection {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add vectors to collection {collection_name}: {e}")
            return False
    
    def search(self, collection_name: str, query_vector: List[float], 
              limit: int = 10, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        try:
            if collection_name not in self.collections:
                logger.warning(f"Collection {collection_name} not found")
                return []
            
            collection = self.collections[collection_name]
            if not collection['vectors']:
                return []
            
            # Simple cosine similarity search
            query_vector = np.array(query_vector)
            similarities = []
            
            for i, vector in enumerate(collection['vectors']):
                vector_array = np.array(vector)
                similarity = np.dot(query_vector, vector_array) / (
                    np.linalg.norm(query_vector) * np.linalg.norm(vector_array)
                )
                
                if similarity >= threshold:
                    similarities.append({
                        'id': collection['ids'][i],
                        'metadata': collection['metadata'][i],
                        'similarity': float(similarity)
                    })
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:limit]
            
        except Exception as e:
            logger.error(f"Failed to search collection {collection_name}: {e}")
            return []
    
    def delete_document_vectors(self, collection_name: str, document_id: int) -> bool:
        """Delete vectors for a specific document"""
        try:
            if collection_name not in self.collections:
                return True
            
            collection = self.collections[collection_name]
            indices_to_remove = []
            
            for i, metadata in enumerate(collection['metadata']):
                if metadata.get('document_id') == document_id:
                    indices_to_remove.append(i)
            
            # Remove in reverse order to maintain indices
            for i in reversed(indices_to_remove):
                del collection['vectors'][i]
                del collection['metadata'][i]
                del collection['ids'][i]
            
            logger.info(f"Deleted {len(indices_to_remove)} vectors for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete vectors for document {document_id}: {e}")
            return False