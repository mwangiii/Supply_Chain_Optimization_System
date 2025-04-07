from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import logging

# Setup logging
logger = logging.getLogger(__name__)

def success_response(
    data: Any = None, 
    message: str = "Operation successful",
    status_code: int = status.HTTP_200_OK,
) -> Dict[str, Any]:
    """Create a standardized success response"""
    response = {
        "status": "success",
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return response

def error_response(
    message: str, 
    errors: Optional[List[Dict[str, Any]]] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Dict[str, Any]:
    """Create a standardized error response"""
    response = {
        "status": "error",
        "message": message,
    }
    if errors:
        response["errors"] = errors
    return response

def http_exception(
    message: str, 
    status_code: int = status.HTTP_400_BAD_REQUEST
) -> HTTPException:
    """Create a standardized HTTP exception"""
    return HTTPException(
        status_code=status_code,
        detail={"status": "error", "message": message}
    )

class APIException(Exception):
    """Base exception for API errors"""
    def __init__(
        self, 
        message: str = "An error occurred", 
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dict for response"""
        response = {
            "status": "error",
            "message": self.message,
        }
        if self.errors:
            response["errors"] = self.errors
        return response
    
    def to_response(self) -> JSONResponse:
        """Convert exception to JSONResponse"""
        return JSONResponse(
            status_code=self.status_code,
            content=self.to_dict()
        )