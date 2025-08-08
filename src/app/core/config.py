import os
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LLM-Powered Intelligent Query-Retrieval System"
    PROJECT_DESCRIPTION: str = "Process large documents and make contextual decisions for insurance, legal, HR, and compliance domains"
    VERSION: str = "1.0.0"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG_MODE: bool = True
    WORKERS: int = 1
    
    # Authentication
    API_TOKEN: str = "9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23"
    
    # Vector Database Settings
    VECTOR_DB_TYPE: str = "pinecone"  # Options: "faiss", "pinecone"
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "document-retrieval")
    
    # LLM Settings
    LLM_TYPE: str = "openai"  # Options: "openai", "huggingface"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4"  # Options: "gpt-3.5-turbo", "gpt-4"
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/document_retrieval")
    
    # Document Processing Settings
    EMBEDDING_MODEL: str = "text-embedding-ada-002"  # OpenAI embedding model
    EMBEDDING_DIMENSION: int = 1536  # Dimension of OpenAI embeddings
    CHUNK_SIZE: int = 1000  # Size of text chunks for embedding
    CHUNK_OVERLAP: int = 200  # Overlap between chunks
    
    # Supported Document Types
    SUPPORTED_DOCUMENT_TYPES: List[str] = ["pdf", "docx", "txt", "eml"]
    
    # Temporary File Storage
    TEMP_FILES_DIR: str = "temp_files"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()