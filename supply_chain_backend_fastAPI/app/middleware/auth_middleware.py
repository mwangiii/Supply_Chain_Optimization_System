from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional, Dict, Any
import time

from supply_chain_backend_fastAPI.core.config import settings

security = HTTPBearer()

class JWTAuth:
    """
    JWT Authentication middleware for FastAPI
    """
    
    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await security(request)
        
        if credentials:
            if credentials.scheme != "Bearer":
                if self.auto_error:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid authentication scheme.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                else:
                    return None
            
            token_payload = self.verify_jwt(credentials.credentials)
            if token_payload is None:
                if self.auto_error:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid token or expired token.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                else:
                    return None
            
            return token_payload
        else:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
    
    def verify_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token and return payload if valid
        
        Args:
            token: JWT token
            
        Returns:
            Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                options={"verify_signature": True, "verify_exp": True}
            )
            
            # Check if token has expired
            if payload.get("exp") and time.time() > payload["exp"]:
                return None
            
            return payload
        except JWTError:
            return None