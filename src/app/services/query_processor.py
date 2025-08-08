import logging
import json
from typing import Dict, List, Optional, Any
from app.core.config import settings
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.utils.text_utils import chunk_text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    Service for processing queries and generating answers using LLM and vector search.
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_service = LLMService()
        logger.info("Initialized QueryProcessor")
    
    async def process_query(self, query: str, document_text: str) -> str:
        """
        Process a query against a document and generate an answer.
        
        Args:
            query: The query to process.
            document_text: The text of the document to query against.
            
        Returns:
            str: The answer to the query.
        """
        try:
            logger.info(f"Processing query: {query}")
            
            # Chunk the document text
            chunks = chunk_text(
                document_text, 
                chunk_size=settings.CHUNK_SIZE, 
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            
            # Create embeddings and store in vector database
            await self.vector_store.add_texts(chunks)
            
            # Extract structured query using LLM
            structured_query = await self.llm_service.extract_structured_query(query)
            
            # Retrieve relevant chunks using vector search
            relevant_chunks = await self.vector_store.similarity_search(
                query=structured_query,
                k=5  # Retrieve top 5 most relevant chunks
            )
            
            # Generate answer using LLM
            answer = await self.llm_service.generate_answer(
                query=query,
                context=relevant_chunks,
                structured_query=structured_query
            )
            
            # Clean up vector store
            await self.vector_store.clear()
            
            return answer
        
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    async def _evaluate_logic(self, query: str, relevant_chunks: List[str]) -> Dict[str, Any]:
        """
        Evaluate the logic of the query against the relevant chunks.
        
        Args:
            query: The query to evaluate.
            relevant_chunks: The relevant chunks from the document.
            
        Returns:
            Dict[str, Any]: The evaluation result.
        """
        try:
            # Use LLM to evaluate the logic
            evaluation_result = await self.llm_service.evaluate_logic(
                query=query,
                context=relevant_chunks
            )
            
            return evaluation_result
        
        except Exception as e:
            logger.error(f"Error evaluating logic: {str(e)}")
            raise