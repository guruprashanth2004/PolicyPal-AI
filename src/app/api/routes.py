from fastapi import APIRouter, Depends, HTTPException, status
from app.api.endpoints import hackrx
from app.core.auth import validate_api_token

api_router = APIRouter()

# Include the hackrx endpoints with authentication
api_router.include_router(
    hackrx.router,
    prefix="/hackrx",
    tags=["hackrx"],
    dependencies=[Depends(validate_api_token)]
)

# Health check endpoint
@api_router.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}