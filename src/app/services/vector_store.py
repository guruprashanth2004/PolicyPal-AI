import os
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Union
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """
    Service for managing vector embeddings and similarity search.
    Supports both FAISS and Pinecone as backend vector databases.
    """
    
    def __init__(self):
        self.vector_db_type = settings.VECTOR_DB_TYPE
        self.embedding_dimension = settings.EMBEDDING_DIMENSION
        self.texts = []  # Store original texts for reference
        
        if self.vector_db_type == "faiss":
            self._init_faiss()
        elif self.vector_db_type == "pinecone":
            self._init_pinecone()
        else:
            raise ValueError(f"Unsupported vector database type: {self.vector_db_type}")
        
        logger.info(f"Initialized VectorStore with backend: {self.vector_db_type}")
    
    def _init_faiss(self):
        """
        Initialize FAISS vector database.
        """
        try:
            import faiss
            
            # Create a new index
            self.index = faiss.IndexFlatL2(self.embedding_dimension)
            logger.info("Initialized FAISS vector database")
        
        except ImportError:
            logger.error("FAISS is not installed. Please install it with 'pip install faiss-cpu' or 'pip install faiss-gpu'")
            raise
        except Exception as e:
            logger.error(f"Error initializing FAISS: {str(e)}")
            raise
    
    def _init_pinecone(self):
        """
        Initialize Pinecone vector database.
        """
        try:
            import pinecone
            
            # Initialize Pinecone client
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )
            
            # Check if index exists, create if not
            if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                pinecone.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=self.embedding_dimension,
                    metric="cosine"
                )
            
            # Connect to the index
            self.index = pinecone.Index(settings.PINECONE_INDEX_NAME)
            logger.info("Initialized Pinecone vector database")
        
        except ImportError:
            logger.error("Pinecone is not installed. Please install it with 'pip install pinecone-client'")
            raise
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
            raise
    
    async def add_texts(self, texts: List[str]) -> List[str]:
        """
        Add texts to the vector database.
        
        Args:
            texts: List of text chunks to add.
            
        Returns:
            List[str]: List of IDs for the added texts.
        """
        try:
            # Store original texts
            self.texts = texts
            
            # Generate embeddings for texts
            from app.services.llm_service import LLMService
            llm_service = LLMService()
            embeddings = await llm_service.get_embeddings(texts)
            
            # Add embeddings to vector database
            if self.vector_db_type == "faiss":
                return self._add_to_faiss(embeddings)
            elif self.vector_db_type == "pinecone":
                return self._add_to_pinecone(embeddings)
        
        except Exception as e:
            logger.error(f"Error adding texts to vector database: {str(e)}")
            raise
    
    def _add_to_faiss(self, embeddings: List[List[float]]) -> List[str]:
        """
        Add embeddings to FAISS.
        
        Args:
            embeddings: List of embedding vectors.
            
        Returns:
            List[str]: List of IDs for the added embeddings.
        """
        try:
            # Convert embeddings to numpy array
            embeddings_np = np.array(embeddings).astype('float32')
            
            # Add to FAISS index
            self.index.add(embeddings_np)
            
            # Generate IDs (just the indices in this case)
            ids = [str(i) for i in range(self.index.ntotal - len(embeddings), self.index.ntotal)]
            
            logger.info(f"Added {len(embeddings)} embeddings to FAISS")
            return ids
        
        except Exception as e:
            logger.error(f"Error adding to FAISS: {str(e)}")
            raise
    
    def _add_to_pinecone(self, embeddings: List[List[float]]) -> List[str]:
        """
        Add embeddings to Pinecone.
        
        Args:
            embeddings: List of embedding vectors.
            
        Returns:
            List[str]: List of IDs for the added embeddings.
        """
        try:
            # Generate IDs
            import uuid
            ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
            
            # Create vector data
            vectors = []
            for i, embedding in enumerate(embeddings):
                vectors.append({
                    "id": ids[i],
                    "values": embedding,
                    "metadata": {"text": self.texts[i]}
                })
            
            # Upsert to Pinecone
            self.index.upsert(vectors=vectors)
            
            logger.info(f"Added {len(embeddings)} embeddings to Pinecone")
            return ids
        
        except Exception as e:
            logger.error(f"Error adding to Pinecone: {str(e)}")
            raise
    
    async def similarity_search(self, query: str, k: int = 5) -> List[str]:
        """
        Perform similarity search to find relevant text chunks.
        
        Args:
            query: The query to search for.
            k: Number of results to return.
            
        Returns:
            List[str]: List of relevant text chunks.
        """
        try:
            # Generate embedding for query
            from app.services.llm_service import LLMService
            llm_service = LLMService()
            query_embedding = await llm_service.get_embeddings([query])
            
            # Perform similarity search
            if self.vector_db_type == "faiss":
                return self._search_faiss(query_embedding[0], k)
            elif self.vector_db_type == "pinecone":
                return self._search_pinecone(query_embedding[0], k)
        
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise
    
    def _search_faiss(self, query_embedding: List[float], k: int) -> List[str]:
        """
        Perform similarity search in FAISS.
        
        Args:
            query_embedding: The query embedding vector.
            k: Number of results to return.
            
        Returns:
            List[str]: List of relevant text chunks.
        """
        try:
            # Convert query embedding to numpy array
            query_np = np.array([query_embedding]).astype('float32')
            
            # Perform search
            distances, indices = self.index.search(query_np, k)
            
            # Get corresponding texts
            results = [self.texts[int(idx)] for idx in indices[0] if idx < len(self.texts)]
            
            logger.info(f"Found {len(results)} relevant chunks in FAISS")
            return results
        
        except Exception as e:
            logger.error(f"Error searching in FAISS: {str(e)}")
            raise
    
    def _search_pinecone(self, query_embedding: List[float], k: int) -> List[str]:
        """
        Perform similarity search in Pinecone.
        
        Args:
            query_embedding: The query embedding vector.
            k: Number of results to return.
            
        Returns:
            List[str]: List of relevant text chunks.
        """
        try:
            # Perform search
            results = self.index.query(
                vector=query_embedding,
                top_k=k,
                include_metadata=True
            )
            
            # Extract texts from metadata
            texts = [match["metadata"]["text"] for match in results["matches"]]
            
            logger.info(f"Found {len(texts)} relevant chunks in Pinecone")
            return texts
        
        except Exception as e:
            logger.error(f"Error searching in Pinecone: {str(e)}")
            raise
    
    async def clear(self):
        """
        Clear the vector database.
        """
        try:
            if self.vector_db_type == "faiss":
                self._clear_faiss()
            elif self.vector_db_type == "pinecone":
                self._clear_pinecone()
            
            # Clear stored texts
            self.texts = []
            
            logger.info(f"Cleared {self.vector_db_type} vector database")
        
        except Exception as e:
            logger.error(f"Error clearing vector database: {str(e)}")
            raise
    
    def _clear_faiss(self):
        """
        Clear FAISS index.
        """
        try:
            import faiss
            
            # Reset the index
            self.index = faiss.IndexFlatL2(self.embedding_dimension)
        
        except Exception as e:
            logger.error(f"Error clearing FAISS: {str(e)}")
            raise
    
    def _clear_pinecone(self):
        """
        Clear Pinecone index.
        """
        try:
            # Delete all vectors
            self.index.delete(delete_all=True)
        
        except Exception as e:
            logger.error(f"Error clearing Pinecone: {str(e)}")
            raise