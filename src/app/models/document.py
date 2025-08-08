from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class Document(BaseModel):
    """
    Model for document data.
    """
    id: Optional[str] = None
    url: str
    content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('url')
    def validate_url(cls, v):
        if not v.startswith('http'):
            raise ValueError("URL must start with http or https")
        return v

class Query(BaseModel):
    """
    Model for query data.
    """
    id: Optional[str] = None
    text: str
    structured_text: Optional[str] = None
    document_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Answer(BaseModel):
    """
    Model for answer data.
    """
    id: Optional[str] = None
    text: str
    query_id: str
    document_id: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    relevant_clauses: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

class DocumentChunk(BaseModel):
    """
    Model for document chunk data.
    """
    id: Optional[str] = None
    document_id: str
    text: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)