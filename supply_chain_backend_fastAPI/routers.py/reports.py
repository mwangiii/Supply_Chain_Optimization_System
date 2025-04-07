from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.utils.helpers import success_response

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)

@router.get("/overview")
async def get_overview():
    return success_response(message="Get overview")

@router.get("/sales")
async def get_sales():
    return success_response(message="Get sales")

@router.get("/inventory")
async def get_inventory():
    return success_response(message="Get inventory")

@router.get("/logistics")
async def get_logistics():
    return success_response(message="Get logistics")

@router.get("/reports")
async def get_reports():
    return success_response(message="Get reports")