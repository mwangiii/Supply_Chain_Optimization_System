from fastapi import HTTPException
from typing import List, Dict, Any

def error_response(status_code: int, message: str):
    """Create a standardized error response"""
    return {"status": "error", "message": message, "status_code": status_code}

def success_response(data: Any = None, message: str = "Operation successful"):
    """Create a standardized success response"""
    response = {"status": "success", "message": message}
    if data is not None:
        response["data"] = data
    return response