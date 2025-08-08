import os
import logging
import pdfplumber
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    """
    Extractor for PDF documents.
    """
    
    async def extract_text(self, file_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file.
            
        Returns:
            str: Extracted text from the PDF.
        """
        try:
            logger.info(f"Extracting text from PDF: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            # Extract text using pdfplumber
            text_content = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n\n"
            
            logger.info(f"Extracted {len(text_content)} characters from PDF")
            return text_content
        
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise