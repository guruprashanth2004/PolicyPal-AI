import os
import tempfile
import logging
import aiohttp
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from app.core.config import settings
from app.utils.file_utils import get_file_extension
from app.services.extractors.pdf_extractor import PDFExtractor
from app.services.extractors.docx_extractor import DocxExtractor
from app.services.extractors.email_extractor import EmailExtractor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Service for processing documents from various sources and extracting text.
    """
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(dir=settings.TEMP_FILES_DIR)
        self.downloaded_files = []
        
        # Create temp directory if it doesn't exist
        os.makedirs(settings.TEMP_FILES_DIR, exist_ok=True)
        
        # Initialize extractors
        self.extractors = {
            "pdf": PDFExtractor(),
            "docx": DocxExtractor(),
            "eml": EmailExtractor(),
            # Add more extractors as needed
        }
        
        logger.info(f"Initialized DocumentProcessor with temp directory: {self.temp_dir}")
    
    async def process_document(self, document_url: str) -> str:
        """
        Process a document from a URL and extract its text content.
        
        Args:
            document_url: URL to the document.
            
        Returns:
            str: Extracted text from the document.
        """
        try:
            # Download the document
            local_path = await self._download_document(document_url)
            self.downloaded_files.append(local_path)
            
            # Get file extension
            file_ext = get_file_extension(local_path).lower()
            
            # Check if file type is supported
            if file_ext not in settings.SUPPORTED_DOCUMENT_TYPES:
                raise ValueError(f"Unsupported document type: {file_ext}")
            
            # Extract text based on file type
            if file_ext in self.extractors:
                extractor = self.extractors[file_ext]
                text = await extractor.extract_text(local_path)
                return text
            else:
                # Fallback for text files
                if file_ext == "txt":
                    with open(local_path, "r", encoding="utf-8") as f:
                        return f.read()
                else:
                    raise ValueError(f"No extractor available for file type: {file_ext}")
        
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
    
    async def _download_document(self, url: str) -> str:
        """
        Download a document from a URL to a local temporary file.
        
        Args:
            url: URL to download the document from.
            
        Returns:
            str: Path to the downloaded file.
        """
        try:
            # Extract filename from URL
            filename = url.split("/")[-1].split("?")[0]
            local_path = os.path.join(self.temp_dir, filename)
            
            # Download the file
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to download document: HTTP {response.status}")
                    
                    with open(local_path, "wb") as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
            
            logger.info(f"Downloaded document to {local_path}")
            return local_path
        
        except Exception as e:
            logger.error(f"Error downloading document: {str(e)}")
            raise
    
    async def cleanup(self):
        """
        Clean up temporary files.
        """
        try:
            for file_path in self.downloaded_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            if os.path.exists(self.temp_dir):
                os.rmdir(self.temp_dir)
            
            logger.info("Cleaned up temporary files")
        
        except Exception as e:
            logger.error(f"Error cleaning up: {str(e)}")