from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float, LargeBinary, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from datetime import datetime
import enum

class DocumentType(str, enum.Enum):
    TEXT = "text"
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"

class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"
    ARCHIVED = "archived"

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Organization
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Configuration
    embedding_model = Column(String, default="all-MiniLM-L6-v2")
    chunk_size = Column(Integer, default=1000)
    chunk_overlap = Column(Integer, default=200)
    
    # Statistics
    total_documents = Column(Integer, default=0)
    total_chunks = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Settings
    settings = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="knowledge_bases")
    documents = relationship("Document", back_populates="knowledge_base")
    chatbots = relationship("Chatbot", back_populates="knowledge_base")
    
    def __repr__(self):
        return f"<KnowledgeBase(id={self.id}, name='{self.name}', org_id={self.organization_id})>"
    
    @property
    def processed_documents_count(self) -> int:
        """Count of successfully processed documents"""
        return len([d for d in self.documents if d.status == DocumentStatus.PROCESSED])
    
    @property
    def pending_documents_count(self) -> int:
        """Count of pending documents"""
        return len([d for d in self.documents if d.status == DocumentStatus.PENDING])
    
    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        if not self.settings:
            return default
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value):
        """Set a specific setting value"""
        if not self.settings:
            self.settings = {}
        self.settings[key] = value

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    title = Column(String, nullable=True)
    
    # Knowledge base
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"), nullable=False)
    
    # Document info
    document_type = Column(Enum(DocumentType), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    file_path = Column(String, nullable=False)
    
    # Content
    content = Column(Text, nullable=True)  # Extracted text content
    summary = Column(Text, nullable=True)  # AI-generated summary
    
    # Processing status
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING)
    error_message = Column(Text, nullable=True)
    
    # Processing metadata
    chunks_count = Column(Integer, default=0)
    processing_time_seconds = Column(Float, nullable=True)
    
    # Document metadata
    extra_data = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    knowledge_base = relationship("KnowledgeBase", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', status='{self.status}')>"
    
    @property
    def file_size_mb(self) -> float:
        """File size in megabytes"""
        return self.file_size / (1024 * 1024)
    
    @property
    def is_processed(self) -> bool:
        """Check if document is successfully processed"""
        return self.status == DocumentStatus.PROCESSED
    
    def get_extra_data(self, key: str, default=None):
        """Get extra data value"""
        if not self.extra_data:
            return default
        return self.extra_data.get(key, default)
    
    def set_extra_data(self, key: str, value):
        """Set extra data value"""
        if not self.extra_data:
            self.extra_data = {}
        self.extra_data[key] = value

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Document reference
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Chunk info
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    
    # Embeddings (stored as JSON array)
    embedding = Column(JSON, nullable=True)
    
    # Metadata
    start_char = Column(Integer, nullable=True)
    end_char = Column(Integer, nullable=True)
    token_count = Column(Integer, nullable=True)
    
    # Additional metadata
    extra_data = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id}, index={self.chunk_index})>"
    
    @property
    def has_embedding(self) -> bool:
        """Check if chunk has embedding"""
        return self.embedding is not None and len(self.embedding) > 0
    
    def get_extra_data(self, key: str, default=None):
        """Get extra data value"""
        if not self.extra_data:
            return default
        return self.extra_data.get(key, default)
    
    def set_extra_data(self, key: str, value):
        """Set extra data value"""
        if not self.extra_data:
            self.extra_data = {}
        self.extra_data[key] = value