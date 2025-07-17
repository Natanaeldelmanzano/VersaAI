from typing import Optional
import asyncio
import logging
from sqlalchemy.orm import Session
from .document_service import DocumentService
from ..api.deps import get_db

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Document processor that handles async document processing"""
    
    def __init__(self):
        self.document_service = DocumentService()
    
    def process_document_async(self, document_id: int) -> None:
        """Process document asynchronously"""
        try:
            # Create a new event loop for async processing
            asyncio.create_task(self._process_document_task(document_id))
        except Exception as e:
            logger.error(f"Failed to start async document processing for document {document_id}: {e}")
    
    async def _process_document_task(self, document_id: int) -> None:
        """Internal async task for document processing"""
        try:
            # Get database session
            db = next(get_db())
            try:
                await self.document_service.process_document(db, document_id)
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")