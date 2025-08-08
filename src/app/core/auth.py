from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

# Set up the HTTP Bearer authentication scheme
security = HTTPBearer()

async def validate_api_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate the API token provided in the Authorization header.
    
    Args:
        credentials: The HTTP Authorization credentials.
        
    Raises:
        HTTPException: If the token is invalid or missing.
        
    Returns:
        bool: True if the token is valid.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme. Expected 'Bearer'.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if credentials.credentials != settings.API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return True