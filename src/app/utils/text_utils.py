import re
import logging
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks of specified size.
    
    Args:
        text: The text to split into chunks.
        chunk_size: The size of each chunk in characters.
        chunk_overlap: The overlap between chunks in characters.
        
    Returns:
        List[str]: List of text chunks.
    """
    try:
        # Clean the text
        text = clean_text(text)
        
        # If text is shorter than chunk size, return as is
        if len(text) <= chunk_size:
            return [text]
        
        # Split text into paragraphs
        paragraphs = text.split("\n\n")
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > chunk_size:
                # Add current chunk to chunks list
                if current_chunk:
                    chunks.append(current_chunk)
                
                # Start a new chunk with overlap
                if chunks and chunk_overlap > 0:
                    # Get the last chunk_overlap characters from the previous chunk
                    overlap_text = chunks[-1][-chunk_overlap:]
                    current_chunk = overlap_text + "\n\n" + paragraph
                else:
                    current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(current_chunk)
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    except Exception as e:
        logger.error(f"Error chunking text: {str(e)}")
        raise

def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace, normalizing line breaks, etc.
    
    Args:
        text: The text to clean.
        
    Returns:
        str: The cleaned text.
    """
    try:
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        
        # Replace multiple newlines with double newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Trim leading/trailing whitespace
        text = text.strip()
        
        return text
    
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        raise

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using simple frequency analysis.
    
    Args:
        text: The text to extract keywords from.
        max_keywords: Maximum number of keywords to extract.
        
    Returns:
        List[str]: List of extracted keywords.
    """
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Split into words
        words = text.split()
        
        # Remove common stop words
        stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
            'when', 'where', 'how', 'who', 'which', 'this', 'that', 'these', 'those',
            'then', 'just', 'so', 'than', 'such', 'both', 'through', 'about', 'for',
            'is', 'of', 'while', 'during', 'to', 'from', 'in', 'on', 'at', 'by', 'with'
        }
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequencies
        word_freq = {}
        for word in filtered_words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Extract top keywords
        keywords = [word for word, freq in sorted_words[:max_keywords]]
        
        logger.info(f"Extracted {len(keywords)} keywords")
        return keywords
    
    except Exception as e:
        logger.error(f"Error extracting keywords: {str(e)}")
        raise