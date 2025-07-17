import os
import uuid
from pathlib import Path
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_file_type(filename: str, allowed_types: Optional[List[str]] = None) -> bool:
    """
    Validate if file type is allowed
    
    Args:
        filename: Name of the file
        allowed_types: List of allowed file extensions
    
    Returns:
        True if file type is allowed, False otherwise
    """
    if allowed_types is None:
        allowed_types = settings.ALLOWED_FILE_TYPES
    
    file_extension = filename.split('.')[-1].lower()
    return file_extension in [ext.lower() for ext in allowed_types]


def validate_file_size(file_size: int, max_size_mb: Optional[int] = None) -> bool:
    """
    Validate if file size is within limits
    
    Args:
        file_size: Size of the file in bytes
        max_size_mb: Maximum allowed size in MB
    
    Returns:
        True if file size is valid, False otherwise
    """
    if max_size_mb is None:
        max_size_mb = settings.MAX_FILE_SIZE_MB
    
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes


async def save_uploaded_file(
    file: UploadFile, 
    upload_dir: Optional[str] = None,
    custom_filename: Optional[str] = None
) -> str:
    """
    Save uploaded file to disk
    
    Args:
        file: FastAPI UploadFile object
        upload_dir: Directory to save the file
        custom_filename: Custom filename (optional)
    
    Returns:
        Path to the saved file
    
    Raises:
        HTTPException: If file validation fails
    """
    try:
        # Validate file type
        if not validate_file_type(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}"
            )
        
        # Read file content to check size
        content = await file.read()
        
        # Validate file size
        if not validate_file_size(len(content)):
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        # Determine upload directory
        if upload_dir is None:
            upload_dir = settings.UPLOAD_DIR
        
        # Create upload directory if it doesn't exist
        upload_path = Path(upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if custom_filename:
            filename = custom_filename
        else:
            # Generate unique filename
            file_extension = file.filename.split('.')[-1]
            filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Save file
        file_path = upload_path / filename
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        logger.info(f"File saved successfully: {file_path}")
        return str(file_path)
        
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving file: {str(e)}"
        )


def delete_file(file_path: str) -> bool:
    """
    Delete file from disk
    
    Args:
        file_path: Path to the file to delete
    
    Returns:
        True if file was deleted successfully, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted successfully: {file_path}")
            return True
        else:
            logger.warning(f"File not found: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False


def get_file_info(file_path: str) -> dict:
    """
    Get file information
    
    Args:
        file_path: Path to the file
    
    Returns:
        Dictionary with file information
    """
    try:
        if not os.path.exists(file_path):
            return {}
        
        stat = os.stat(file_path)
        return {
            "name": os.path.basename(file_path),
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "extension": file_path.split('.')[-1].lower()
        }
    except Exception as e:
        logger.error(f"Error getting file info for {file_path}: {str(e)}")
        return {}


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path
    
    Returns:
        True if directory exists or was created successfully
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        return False