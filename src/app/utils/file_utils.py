import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_file_extension(file_path: str) -> str:
    """
    Get the extension of a file.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        str: The file extension without the dot.
    """
    try:
        _, ext = os.path.splitext(file_path)
        return ext.lstrip('.').lower()
    
    except Exception as e:
        logger.error(f"Error getting file extension: {str(e)}")
        raise

def is_supported_file_type(file_path: str) -> bool:
    """
    Check if a file type is supported.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        bool: True if the file type is supported, False otherwise.
    """
    try:
        ext = get_file_extension(file_path)
        return ext in settings.SUPPORTED_DOCUMENT_TYPES
    
    except Exception as e:
        logger.error(f"Error checking file type: {str(e)}")
        raise

def create_temp_dir() -> str:
    """
    Create a temporary directory for file processing.
    
    Returns:
        str: Path to the created temporary directory.
    """
    try:
        import tempfile
        
        # Create temp directory if it doesn't exist
        os.makedirs(settings.TEMP_FILES_DIR, exist_ok=True)
        
        # Create a temporary directory within the temp_files directory
        temp_dir = tempfile.mkdtemp(dir=settings.TEMP_FILES_DIR)
        
        logger.info(f"Created temporary directory: {temp_dir}")
        return temp_dir
    
    except Exception as e:
        logger.error(f"Error creating temporary directory: {str(e)}")
        raise

def cleanup_temp_files(temp_dir: str):
    """
    Clean up temporary files and directories.
    
    Args:
        temp_dir: Path to the temporary directory to clean up.
    """
    try:
        import shutil
        
        # Check if directory exists
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            # Remove directory and all its contents
            shutil.rmtree(temp_dir)
            
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
    
    except Exception as e:
        logger.error(f"Error cleaning up temporary files: {str(e)}")
        # Don't raise the exception, just log it

def get_mime_type(file_path: str) -> str:
    """
    Get the MIME type of a file.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        str: The MIME type of the file.
    """
    try:
        import mimetypes
        
        # Initialize mimetypes
        mimetypes.init()
        
        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # If MIME type is None, use a default based on extension
        if mime_type is None:
            ext = get_file_extension(file_path)
            mime_map = {
                'pdf': 'application/pdf',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'doc': 'application/msword',
                'txt': 'text/plain',
                'eml': 'message/rfc822'
            }
            mime_type = mime_map.get(ext, 'application/octet-stream')
        
        return mime_type
    
    except Exception as e:
        logger.error(f"Error getting MIME type: {str(e)}")
        raise