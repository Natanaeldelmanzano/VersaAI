from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from ..core.database import get_db
from .user_repository import UserRepository
from .chatbot_repository import ChatbotRepository
from .conversation_repository import ConversationRepository
from .knowledge_base_repository import KnowledgeBaseRepository, DocumentRepository, DocumentChunkRepository
from .organization_repository import OrganizationRepository

# Repository Dependencies for FastAPI Dependency Injection

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Get UserRepository instance with database session"""
    return UserRepository(db)

def get_chatbot_repository(db: Session = Depends(get_db)) -> ChatbotRepository:
    """Get ChatbotRepository instance with database session"""
    return ChatbotRepository(db)

def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    """Get ConversationRepository instance with database session"""
    return ConversationRepository(db)

def get_knowledge_base_repository(db: Session = Depends(get_db)) -> KnowledgeBaseRepository:
    """Get KnowledgeBaseRepository instance with database session"""
    return KnowledgeBaseRepository(db)

def get_document_repository(db: Session = Depends(get_db)) -> DocumentRepository:
    """Get DocumentRepository instance with database session"""
    return DocumentRepository(db)

def get_document_chunk_repository(db: Session = Depends(get_db)) -> DocumentChunkRepository:
    """Get DocumentChunkRepository instance with database session"""
    return DocumentChunkRepository(db)

def get_organization_repository(db: Session = Depends(get_db)) -> OrganizationRepository:
    """Get OrganizationRepository instance with database session"""
    return OrganizationRepository(db)

# Repository Factory for manual instantiation
class RepositoryFactory:
    """Factory class for creating repository instances"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_repository(self) -> UserRepository:
        return UserRepository(self.db)
    
    def get_chatbot_repository(self) -> ChatbotRepository:
        return ChatbotRepository(self.db)
    
    def get_conversation_repository(self) -> ConversationRepository:
        return ConversationRepository(self.db)
    
    def get_knowledge_base_repository(self) -> KnowledgeBaseRepository:
        return KnowledgeBaseRepository(self.db)
    
    def get_document_repository(self) -> DocumentRepository:
        return DocumentRepository(self.db)
    
    def get_document_chunk_repository(self) -> DocumentChunkRepository:
        return DocumentChunkRepository(self.db)
    
    def get_organization_repository(self) -> OrganizationRepository:
        return OrganizationRepository(self.db)

def get_repository_factory(db: Session = Depends(get_db)) -> RepositoryFactory:
    """Get RepositoryFactory instance with database session"""
    return RepositoryFactory(db)