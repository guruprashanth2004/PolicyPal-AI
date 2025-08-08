from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, validator, Field
from typing import List, Optional, Dict, Any
from app.services.document_processor import DocumentProcessor
from app.services.query_processor import QueryProcessor
from app.core.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Define request and response models
class RunRequest(BaseModel):
    documents: str = Field(..., description="URL to the document to be processed")
    questions: List[str] = Field(..., description="List of questions to be answered")
    
    @validator('documents')
    def validate_document_url(cls, v):
        # Basic URL validation
        if not v.startswith('http'):
            raise ValueError("Document URL must be a valid HTTP/HTTPS URL")
        return v
    
    @validator('questions')
    def validate_questions(cls, v):
        if not v or len(v) == 0:
            raise ValueError("At least one question must be provided")
        return v

class RunResponse(BaseModel):
    answers: List[str] = Field(..., description="List of answers corresponding to the questions")

@router.post("/run", response_model=RunResponse, status_code=status.HTTP_200_OK)
async def run_query(request: RunRequest, background_tasks: BackgroundTasks):
    """
    Process documents and answer questions.
    
    Args:
        request: The request containing document URLs and questions.
        background_tasks: FastAPI background tasks for async processing.
        
    Returns:
        RunResponse: The answers to the questions.
    """
    try:
        logger.info(f"Processing document: {request.documents}")
        
        # Initialize document processor
        doc_processor = DocumentProcessor()
        
        # Process the document and extract text
        document_text = await doc_processor.process_document(request.documents)
        
        # Initialize query processor
        query_processor = QueryProcessor()
        
        # Process each question and get answers
        answers = []
        for question in request.questions:
            logger.info(f"Processing question: {question}")
            answer = await query_processor.process_query(question, document_text)
            answers.append(answer)
        
        # Schedule cleanup in the background
        background_tasks.add_task(doc_processor.cleanup)
        
        return RunResponse(answers=answers)
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )