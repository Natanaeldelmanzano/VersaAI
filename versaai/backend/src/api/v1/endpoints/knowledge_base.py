from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Any, List, Optional
import os
import uuid
from pathlib import Path

from src.api.deps import (
    get_db,
    get_current_active_user,
    check_organization_access,
    validate_organization_limits
)
from src.models.user import User, UserRole
from src.models.knowledge_base import KnowledgeBase, Document, DocumentChunk, DocumentType, DocumentStatus
from src.schemas.knowledge_base import (
    KnowledgeBase as KnowledgeBaseSchema,
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseWithStats,
    KnowledgeBaseList,
    KnowledgeBaseStats,
    KnowledgeBaseExport,
    Document as DocumentSchema,
    DocumentCreate,
    DocumentUpdate,
    DocumentWithChunks,
    DocumentList,
    DocumentUpload,
    DocumentProcessing,
    DocumentSearch,
    DocumentSearchResult,
    DocumentChunk as DocumentChunkSchema,
    DocumentChunkCreate,
    DocumentChunkWithSimilarity,
    DocumentBulkOperation,
    DocumentBulkResult
)
from src.services.document_processor import DocumentProcessor
from src.services.vector_store import VectorStore
from src.core.config import settings

router = APIRouter()
document_processor = DocumentProcessor()
vector_store = VectorStore()

@router.get("/", response_model=List[KnowledgeBaseSchema])
def read_knowledge_bases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0, description="Number of knowledge bases to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of knowledge bases to return"),
    search: Optional[str] = Query(None, description="Search knowledge bases by name or description")
) -> Any:
    """
    Retrieve knowledge bases from the current user's organization.
    """
    try:
        query = db.query(KnowledgeBase)
        
        # Filter by organization
        if current_user.role != UserRole.SUPER_ADMIN:
            query = query.filter(KnowledgeBase.organization_id == current_user.organization_id)
        
        # Apply search filter
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (KnowledgeBase.name.ilike(search_filter)) |
                (KnowledgeBase.description.ilike(search_filter))
            )
        
        # Order by most recent
        query = query.order_by(KnowledgeBase.updated_at.desc())
        
        # Apply pagination
        knowledge_bases = query.offset(skip).limit(limit).all()
        
        return knowledge_bases
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve knowledge bases: {str(e)}"
        )

@router.post("/", response_model=KnowledgeBaseSchema, status_code=status.HTTP_201_CREATED)
def create_knowledge_base(
    knowledge_base_data: KnowledgeBaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a new knowledge base.
    """
    try:
        # Check if name already exists in organization
        existing_kb = db.query(KnowledgeBase).filter(
            KnowledgeBase.name == knowledge_base_data.name,
            KnowledgeBase.organization_id == current_user.organization_id
        ).first()
        
        if existing_kb:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Knowledge base with this name already exists"
            )
        
        # Validate organization limits
        validate_organization_limits(db, current_user.organization_id, "knowledge_bases")
        
        # Create knowledge base
        knowledge_base = KnowledgeBase(
            name=knowledge_base_data.name,
            description=knowledge_base_data.description,
            organization_id=current_user.organization_id,
            created_by=current_user.id,
            settings=knowledge_base_data.settings or {}
        )
        
        db.add(knowledge_base)
        db.commit()
        db.refresh(knowledge_base)
        
        # Create vector collection for this knowledge base
        try:
            vector_store.create_collection(f"kb_{knowledge_base.id}")
        except Exception as e:
            print(f"Warning: Failed to create vector collection: {e}")
        
        return knowledge_base
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Knowledge base creation failed: {str(e)}"
        )

@router.get("/{knowledge_base_id}", response_model=KnowledgeBaseWithStats)
def read_knowledge_base(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get knowledge base by ID with statistics.
    """
    try:
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        # Check organization access
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Calculate statistics
        total_documents = db.query(Document).filter(
            Document.knowledge_base_id == knowledge_base_id
        ).count()
        
        processed_documents = db.query(Document).filter(
            Document.knowledge_base_id == knowledge_base_id,
            Document.status == DocumentStatus.PROCESSED
        ).count()
        
        total_chunks = db.query(DocumentChunk).join(Document).filter(
            Document.knowledge_base_id == knowledge_base_id
        ).count()
        
        # Convert to response format
        kb_dict = knowledge_base.__dict__.copy()
        kb_dict['stats'] = {
            'total_documents': total_documents,
            'processed_documents': processed_documents,
            'total_chunks': total_chunks,
            'processing_documents': total_documents - processed_documents
        }
        
        return kb_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve knowledge base: {str(e)}"
        )

@router.put("/{knowledge_base_id}", response_model=KnowledgeBaseSchema)
def update_knowledge_base(
    knowledge_base_id: int,
    knowledge_base_update: KnowledgeBaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update knowledge base by ID.
    """
    try:
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        # Check organization access
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Check if new name already exists (if name is being updated)
        if knowledge_base_update.name and knowledge_base_update.name != knowledge_base.name:
            existing_kb = db.query(KnowledgeBase).filter(
                KnowledgeBase.name == knowledge_base_update.name,
                KnowledgeBase.organization_id == current_user.organization_id,
                KnowledgeBase.id != knowledge_base_id
            ).first()
            
            if existing_kb:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Knowledge base with this name already exists"
                )
        
        # Update knowledge base
        for field, value in knowledge_base_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(knowledge_base, field, value)
        
        db.commit()
        db.refresh(knowledge_base)
        
        return knowledge_base
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Knowledge base update failed: {str(e)}"
        )

@router.delete("/{knowledge_base_id}")
def delete_knowledge_base(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete knowledge base by ID.
    """
    try:
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        # Check organization access
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Check if knowledge base is being used by any chatbots
        from src.models.chatbot import chatbot_knowledge_base_association
        chatbot_count = db.query(chatbot_knowledge_base_association).filter(
            chatbot_knowledge_base_association.c.knowledge_base_id == knowledge_base_id
        ).count()
        
        if chatbot_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete knowledge base that is being used by chatbots"
            )
        
        # Delete associated documents and chunks
        documents = db.query(Document).filter(
            Document.knowledge_base_id == knowledge_base_id
        ).all()
        
        for document in documents:
            # Delete document chunks
            db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document.id
            ).delete()
            
            # Delete document file if exists
            if document.file_path and os.path.exists(document.file_path):
                try:
                    os.remove(document.file_path)
                except Exception as e:
                    print(f"Warning: Failed to delete file {document.file_path}: {e}")
        
        # Delete documents
        db.query(Document).filter(
            Document.knowledge_base_id == knowledge_base_id
        ).delete()
        
        # Delete vector collection
        try:
            vector_store.delete_collection(f"kb_{knowledge_base_id}")
        except Exception as e:
            print(f"Warning: Failed to delete vector collection: {e}")
        
        # Delete knowledge base
        db.delete(knowledge_base)
        db.commit()
        
        return {"message": "Knowledge base deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Knowledge base deletion failed: {str(e)}"
        )

@router.get("/{knowledge_base_id}/documents", response_model=List[DocumentSchema])
def read_documents(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0, description="Number of documents to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of documents to return"),
    document_type: Optional[DocumentType] = Query(None, description="Filter by document type"),
    status: Optional[DocumentStatus] = Query(None, description="Filter by document status"),
    search: Optional[str] = Query(None, description="Search documents by title or content")
) -> Any:
    """
    Retrieve documents from a knowledge base.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Build query
        query = db.query(Document).filter(
            Document.knowledge_base_id == knowledge_base_id
        )
        
        # Apply filters
        if document_type:
            query = query.filter(Document.document_type == document_type)
        
        if status:
            query = query.filter(Document.status == status)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Document.title.ilike(search_filter)) |
                (Document.content.ilike(search_filter))
            )
        
        # Order by most recent
        query = query.order_by(Document.updated_at.desc())
        
        # Apply pagination
        documents = query.offset(skip).limit(limit).all()
        
        return documents
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve documents: {str(e)}"
        )

@router.post("/{knowledge_base_id}/documents/upload", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
async def upload_document(
    knowledge_base_id: int,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Upload a document to a knowledge base.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Validate file type
        allowed_extensions = {".pdf", ".txt", ".docx", ".md", ".html", ".csv"}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_extension} not supported. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        file_content = await file.read()
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 10MB limit"
            )
        
        # Create upload directory if it doesn't exist
        upload_dir = Path(settings.UPLOAD_DIR) / "documents" / str(knowledge_base_id)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_extension}"
        file_path = upload_dir / filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Determine document type
        document_type = DocumentType.PDF if file_extension == ".pdf" else DocumentType.TEXT
        
        # Create document record
        document = Document(
            title=title or file.filename,
            knowledge_base_id=knowledge_base_id,
            document_type=document_type,
            file_path=str(file_path),
            file_name=file.filename,
            file_size=len(file_content),
            uploaded_by=current_user.id,
            status=DocumentStatus.UPLOADED
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Process document asynchronously
        try:
            document_processor.process_document_async(document.id)
        except Exception as e:
            print(f"Warning: Failed to start document processing: {e}")
        
        return document
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        # Clean up file if it was created
        if 'file_path' in locals() and file_path.exists():
            try:
                file_path.unlink()
            except:
                pass
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}"
        )

@router.post("/{knowledge_base_id}/documents", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
def create_document(
    knowledge_base_id: int,
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a text document in a knowledge base.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Create document
        document = Document(
            title=document_data.title,
            content=document_data.content,
            knowledge_base_id=knowledge_base_id,
            document_type=DocumentType.TEXT,
            uploaded_by=current_user.id,
            status=DocumentStatus.UPLOADED,
            metadata=document_data.metadata or {}
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Process document asynchronously
        try:
            document_processor.process_document_async(document.id)
        except Exception as e:
            print(f"Warning: Failed to start document processing: {e}")
        
        return document
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document creation failed: {str(e)}"
        )

@router.get("/{knowledge_base_id}/documents/{document_id}", response_model=DocumentWithChunks)
def read_document(
    knowledge_base_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get document by ID with chunks.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Get document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.knowledge_base_id == knowledge_base_id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Get document chunks
        chunks = db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).order_by(DocumentChunk.chunk_index.asc()).all()
        
        # Convert to response format
        document_dict = document.__dict__.copy()
        document_dict['chunks'] = chunks
        
        return document_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve document: {str(e)}"
        )

@router.put("/{knowledge_base_id}/documents/{document_id}", response_model=DocumentSchema)
def update_document(
    knowledge_base_id: int,
    document_id: int,
    document_update: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update document by ID.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Get document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.knowledge_base_id == knowledge_base_id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Update document
        content_changed = False
        for field, value in document_update.dict(exclude_unset=True).items():
            if value is not None:
                if field == "content" and value != document.content:
                    content_changed = True
                setattr(document, field, value)
        
        db.commit()
        db.refresh(document)
        
        # Reprocess document if content changed
        if content_changed:
            try:
                document_processor.process_document_async(document.id)
            except Exception as e:
                print(f"Warning: Failed to start document reprocessing: {e}")
        
        return document
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document update failed: {str(e)}"
        )

@router.delete("/{knowledge_base_id}/documents/{document_id}")
def delete_document(
    knowledge_base_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete document by ID.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Get document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.knowledge_base_id == knowledge_base_id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Delete document chunks from vector store
        try:
            vector_store.delete_document_vectors(f"kb_{knowledge_base_id}", document_id)
        except Exception as e:
            print(f"Warning: Failed to delete vectors: {e}")
        
        # Delete document chunks
        db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).delete()
        
        # Delete document file if exists
        if document.file_path and os.path.exists(document.file_path):
            try:
                os.remove(document.file_path)
            except Exception as e:
                print(f"Warning: Failed to delete file {document.file_path}: {e}")
        
        # Delete document
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document deletion failed: {str(e)}"
        )

@router.post("/{knowledge_base_id}/search", response_model=List[DocumentChunkWithSimilarity])
def search_knowledge_base(
    knowledge_base_id: int,
    search_request: DocumentSearch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Search documents in a knowledge base.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Perform vector search
        try:
            results = vector_store.search(
                collection_name=f"kb_{knowledge_base_id}",
                query=search_request.query,
                limit=search_request.limit or 10,
                threshold=search_request.threshold or 0.7
            )
            
            # Get document chunks with similarity scores
            chunk_results = []
            for result in results:
                chunk = db.query(DocumentChunk).filter(
                    DocumentChunk.id == result["id"]
                ).first()
                
                if chunk:
                    chunk_dict = chunk.__dict__.copy()
                    chunk_dict['similarity_score'] = result["score"]
                    chunk_results.append(chunk_dict)
            
            return chunk_results
            
        except Exception as e:
            # Fallback to text search if vector search fails
            print(f"Vector search failed, falling back to text search: {e}")
            
            search_filter = f"%{search_request.query}%"
            chunks = db.query(DocumentChunk).join(Document).filter(
                Document.knowledge_base_id == knowledge_base_id,
                DocumentChunk.content.ilike(search_filter)
            ).limit(search_request.limit or 10).all()
            
            # Add dummy similarity scores
            chunk_results = []
            for chunk in chunks:
                chunk_dict = chunk.__dict__.copy()
                chunk_dict['similarity_score'] = 0.8  # Dummy score
                chunk_results.append(chunk_dict)
            
            return chunk_results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@router.post("/{knowledge_base_id}/documents/{document_id}/reprocess")
def reprocess_document(
    knowledge_base_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Reprocess a document.
    """
    try:
        # Verify knowledge base exists and user has access
        knowledge_base = db.query(KnowledgeBase).filter(
            KnowledgeBase.id == knowledge_base_id
        ).first()
        
        if not knowledge_base:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found"
            )
        
        check_organization_access(current_user, knowledge_base.organization_id)
        
        # Get document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.knowledge_base_id == knowledge_base_id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Update status to processing
        document.status = DocumentStatus.PROCESSING
        db.commit()
        
        # Start reprocessing
        try:
            document_processor.process_document_async(document.id)
        except Exception as e:
            document.status = DocumentStatus.ERROR
            document.error_message = str(e)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start document reprocessing: {str(e)}"
            )
        
        return {"message": "Document reprocessing started"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document reprocessing failed: {str(e)}"
        )