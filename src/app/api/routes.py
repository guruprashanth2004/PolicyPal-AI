from fastapi import APIRouter, Depends, HTTPException, status
from app.api.endpoints import hackrx
from app.core.auth import validate_api_token

api_router = APIRouter()

# Root endpoint
@api_router.get("/", tags=["root"])
async def root():
    return {
        "message": "LLM-Powered Intelligent Query-Retrieval System",
        "version": "1.0.0",
        "status": "running"
    }

# Health check endpoint
@api_router.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "ok",
        "service": "query-retrieval-api",
        "version": "1.0.0"
    }

# Include the hackrx endpoints with authentication
api_router.include_router(
    hackrx.router,
    prefix="/hackrx",
    tags=["hackrx"],
    dependencies=[Depends(validate_api_token)]
)