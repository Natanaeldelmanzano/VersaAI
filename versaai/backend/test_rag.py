#!/usr/bin/env python3
"""
Script de prueba para verificar las capacidades RAG
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.rag_service import RAGService
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_rag_service():
    """Prueba básica del servicio RAG"""
    print("=== Prueba del Servicio RAG ===")
    
    # Inicializar el servicio RAG
    rag_service = RAGService()
    
    # Verificar si está disponible
    print(f"RAG Service disponible: {rag_service.is_available()}")
    
    if rag_service.is_available():
        print(f"Modelo de embedding: {rag_service.model_name}")
        
        # Probar generación de embedding
        test_text = "Este es un texto de prueba para generar embeddings"
        print(f"Texto de prueba: {test_text}")
        
        embedding = rag_service.generate_embedding(test_text)
        if embedding:
            print(f"Embedding generado exitosamente. Dimensiones: {len(embedding)}")
            print(f"Primeros 5 valores: {embedding[:5]}")
            
            # Probar similitud
            test_text2 = "Otro texto para comparar similitud"
            embedding2 = rag_service.generate_embedding(test_text2)
            if embedding2:
                similarity = rag_service.calculate_similarity(embedding, embedding2)
                print(f"Similitud entre textos: {similarity:.4f}")
        else:
            print("Error: No se pudo generar el embedding")
    else:
        print("Error: RAG Service no está disponible")
    
    print("=== Fin de la prueba ===")

if __name__ == "__main__":
    test_rag_service()