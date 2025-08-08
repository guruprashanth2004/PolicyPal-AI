import os
import logging
import email
from email import policy
from email.parser import BytesParser
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailExtractor:
    """
    Extractor for email documents.
    """
    
    async def extract_text(self, file_path: str) -> str:
        """
        Extract text from an email file.
        
        Args:
            file_path: Path to the email file.
            
        Returns:
            str: Extracted text from the email.
        """
        try:
            logger.info(f"Extracting text from email: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Email file not found: {file_path}")
            
            # Parse email
            with open(file_path, 'rb') as fp:
                msg = BytesParser(policy=policy.default).parse(fp)
            
            # Extract metadata
            metadata = [
                f"From: {msg.get('From', 'Unknown')}",
                f"To: {msg.get('To', 'Unknown')}",
                f"Subject: {msg.get('Subject', 'No Subject')}",
                f"Date: {msg.get('Date', 'Unknown')}"
            ]
            
            # Extract body
            body = ""
            
            # If the message is multipart
            if msg.is_multipart():
                for part in msg.iter_parts():
                    content_type = part.get_content_type()
                    
                    # Extract text from plain text and HTML parts
                    if content_type == "text/plain":
                        body += part.get_content() + "\n\n"
                    elif content_type == "text/html":
                        # Simple HTML to text conversion
                        import re
                        html_text = part.get_content()
                        # Remove HTML tags
                        text = re.sub('<.*?>', ' ', html_text)
                        # Replace multiple spaces with single space
                        text = re.sub('\s+', ' ', text)
                        body += text + "\n\n"
            else:
                # If the message is not multipart
                content_type = msg.get_content_type()
                if content_type == "text/plain":
                    body = msg.get_content()
                elif content_type == "text/html":
                    # Simple HTML to text conversion
                    import re
                    html_text = msg.get_content()
                    # Remove HTML tags
                    text = re.sub('<.*?>', ' ', html_text)
                    # Replace multiple spaces with single space
                    text = re.sub('\s+', ' ', text)
                    body = text
            
            # Combine metadata and body
            text_content = "\n".join(metadata) + "\n\n" + body
            
            logger.info(f"Extracted {len(text_content)} characters from email")
            return text_content
        
        except Exception as e:
            logger.error(f"Error extracting text from email: {str(e)}")
            raise