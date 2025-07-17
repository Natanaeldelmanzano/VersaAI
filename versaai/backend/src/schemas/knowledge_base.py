from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    """Document type enum"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
    URL = "url"

class DocumentStatus(str, Enum):
    """Document status enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"

class KnowledgeBaseBase(BaseModel):
    """Base knowledge base schema"""
    name: str = Field(..., min_length=2, max_length=100, description="Knowledge base name")
    description: Optional[str] = Field(None, max_length=500, description="Knowledge base description")
    is_active: bool = Field(default=True, description="Knowledge base active status")

class KnowledgeBaseCreate(KnowledgeBaseBase):
    """Knowledge base creation schema"""
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Embedding model")
    chunk_size: int = Field(default=1000, ge=100, le=2000, description="Chunk size")
    chunk_overlap: int = Field(default=200, ge=0, le=500, description="Chunk overlap")
    settings: Optional[Dict[str, Any]] = Field(None, description="Additional settings")

class KnowledgeBaseUpdate(BaseModel):
    """Knowledge base update schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Knowledge base name")
    description: Optional[str] = Field(None, max_length=500, description="Knowledge base description")
    is_active: Optional[bool] = Field(None, description="Knowledge base active status")
    settings: Optional[Dict[str, Any]] = Field(None, description="Additional settings")

class KnowledgeBaseInDBBase(KnowledgeBaseBase):
    """Base knowledge base schema with database fields"""
    id: int = Field(..., description="Knowledge base ID")
    organization_id: int = Field(..., description="Organization ID")
    created_by: int = Field(..., description="Creator user ID")
    embedding_model: str = Field(..., description="Embedding model")
    chunk_size: int = Field(..., description="Chunk size")
    chunk_overlap: int = Field(..., description="Chunk overlap")
    total_documents: int = Field(default=0, description="Total document count")
    total_chunks: int = Field(default=0, description="Total chunk count")
    total_size_bytes: int = Field(default=0, description="Total size in bytes")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Additional settings")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_indexed_at: Optional[datetime] = Field(None, description="Last indexing timestamp")

    class Config:
        from_attributes = True

class KnowledgeBase(KnowledgeBaseInDBBase):
    """Knowledge base schema for API responses"""
    pass

class KnowledgeBaseWithStats(KnowledgeBase):
    """Knowledge base schema with statistics"""
    documents_by_status: Dict[str, int] = Field(default_factory=dict, description="Documents grouped by status")
    documents_by_type: Dict[str, int] = Field(default_factory=dict, description="Documents grouped by type")
    avg_chunk_size: float = Field(default=0.0, description="Average chunk size")
    last_document_added: Optional[datetime] = Field(None, description="Last document addition")
    processing_queue_size: int = Field(default=0, description="Processing queue size")

class DocumentBase(BaseModel):
    """Base document schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Document title")
    document_type: DocumentType = Field(..., description="Document type")
    content: Optional[str] = Field(None, description="Document content")
    url: Optional[str] = Field(None, description="Document URL")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Document metadata")

class DocumentCreate(DocumentBase):
    """Document creation schema"""
    knowledge_base_id: int = Field(..., description="Knowledge base ID")
    file_path: Optional[str] = Field(None, description="File path for uploaded files")
    extract_metadata: bool = Field(default=True, description="Extract metadata from document")
    auto_chunk: bool = Field(default=True, description="Automatically chunk document")

class DocumentUpdate(BaseModel):
    """Document update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Document title")
    content: Optional[str] = Field(None, description="Document content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Document metadata")
    status: Optional[DocumentStatus] = Field(None, description="Document status")

class DocumentInDBBase(DocumentBase):
    """Base document schema with database fields"""
    id: int = Field(..., description="Document ID")
    knowledge_base_id: int = Field(..., description="Knowledge base ID")
    uploaded_by: int = Field(..., description="Uploader user ID")
    status: DocumentStatus = Field(default=DocumentStatus.PENDING, description="Document status")
    file_path: Optional[str] = Field(None, description="File path")
    file_size_bytes: Optional[int] = Field(None, description="File size in bytes")
    chunk_count: int = Field(default=0, description="Number of chunks")
    processing_error: Optional[str] = Field(None, description="Processing error message")
    checksum: Optional[str] = Field(None, description="File checksum")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    processed_at: Optional[datetime] = Field(None, description="Processing completion timestamp")

    class Config:
        from_attributes = True

class Document(DocumentInDBBase):
    """Document schema for API responses"""
    pass

class DocumentWithChunks(Document):
    """Document schema with chunks"""
    chunks: List['DocumentChunk'] = Field(..., description="Document chunks")

class DocumentChunkBase(BaseModel):
    """Base document chunk schema"""
    content: str = Field(..., description="Chunk content")
    chunk_index: int = Field(..., description="Chunk index")
    start_char: int = Field(..., description="Start character position")
    end_char: int = Field(..., description="End character position")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Chunk metadata")

class DocumentChunkCreate(DocumentChunkBase):
    """Document chunk creation schema"""
    document_id: int = Field(..., description="Document ID")
    embedding: Optional[List[float]] = Field(None, description="Chunk embedding")

class DocumentChunkInDBBase(DocumentChunkBase):
    """Base document chunk schema with database fields"""
    id: int = Field(..., description="Chunk ID")
    document_id: int = Field(..., description="Document ID")
    embedding: Optional[List[float]] = Field(None, description="Chunk embedding")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True

class DocumentChunk(DocumentChunkInDBBase):
    """Document chunk schema for API responses"""
    pass

class DocumentChunkWithSimilarity(DocumentChunk):
    """Document chunk schema with similarity score"""
    similarity_score: float = Field(..., description="Similarity score")
    document_title: str = Field(..., description="Parent document title")

class KnowledgeBaseList(BaseModel):
    """Knowledge base list schema"""
    knowledge_bases: List[KnowledgeBaseWithStats] = Field(..., description="List of knowledge bases")
    total: int = Field(..., description="Total number of knowledge bases")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")

class DocumentList(BaseModel):
    """Document list schema"""
    documents: List[Document] = Field(..., description="List of documents")
    total: int = Field(..., description="Total number of documents")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")

class DocumentUpload(BaseModel):
    """Document upload schema"""
    title: Optional[str] = Field(None, description="Document title (auto-generated if not provided)")
    extract_metadata: bool = Field(default=True, description="Extract metadata from document")
    auto_chunk: bool = Field(default=True, description="Automatically chunk document")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class DocumentProcessing(BaseModel):
    """Document processing schema"""
    document_id: int = Field(..., description="Document ID")
    reprocess: bool = Field(default=False, description="Reprocess existing document")
    chunk_size: Optional[int] = Field(None, description="Override chunk size")
    chunk_overlap: Optional[int] = Field(None, description="Override chunk overlap")

class DocumentSearch(BaseModel):
    """Document search schema"""
    query: str = Field(..., min_length=1, description="Search query")
    knowledge_base_id: Optional[int] = Field(None, description="Filter by knowledge base")
    document_type: Optional[DocumentType] = Field(None, description="Filter by document type")
    status: Optional[DocumentStatus] = Field(None, description="Filter by status")
    limit: int = Field(default=10, ge=1, le=50, description="Result limit")
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Similarity threshold")

class DocumentSearchResult(BaseModel):
    """Document search result schema"""
    chunks: List[DocumentChunkWithSimilarity] = Field(..., description="Found chunks")
    total: int = Field(..., description="Total results")
    query: str = Field(..., description="Search query")
    search_time_ms: float = Field(..., description="Search time in milliseconds")

class KnowledgeBaseStats(BaseModel):
    """Knowledge base statistics schema"""
    total_documents: int = Field(..., description="Total documents")
    total_chunks: int = Field(..., description="Total chunks")
    total_size_mb: float = Field(..., description="Total size in MB")
    documents_by_status: Dict[str, int] = Field(..., description="Documents by status")
    documents_by_type: Dict[str, int] = Field(..., description="Documents by type")
    avg_chunk_size: float = Field(..., description="Average chunk size")
    processing_queue_size: int = Field(..., description="Processing queue size")
    last_document_added: Optional[datetime] = Field(None, description="Last document addition")
    last_indexed_at: Optional[datetime] = Field(None, description="Last indexing time")

class DocumentBulkOperation(BaseModel):
    """Document bulk operation schema"""
    document_ids: List[int] = Field(..., description="List of document IDs")
    operation: str = Field(..., description="Operation type (delete, reprocess, archive)")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Operation parameters")

class DocumentBulkResult(BaseModel):
    """Document bulk operation result schema"""
    success_count: int = Field(..., description="Number of successful operations")
    error_count: int = Field(..., description="Number of failed operations")
    errors: List[Dict[str, Any]] = Field(..., description="Error details")
    operation: str = Field(..., description="Operation type")
    total_processed: int = Field(..., description="Total documents processed")

class KnowledgeBaseExport(BaseModel):
    """Knowledge base export schema"""
    format: str = Field(default="json", description="Export format (json, csv)")
    include_chunks: bool = Field(default=True, description="Include document chunks")
    include_embeddings: bool = Field(default=False, description="Include embeddings")
    include_metadata: bool = Field(default=True, description="Include metadata")
    document_types: Optional[List[DocumentType]] = Field(None, description="Filter by document types")
    status_filter: Optional[List[DocumentStatus]] = Field(None, description="Filter by status")

# Resolve forward references
DocumentWithChunks.model_rebuild()