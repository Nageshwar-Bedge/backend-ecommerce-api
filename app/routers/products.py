"""
Product API routes
"""
from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from app.models import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])
product_service = ProductService()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Create a new product
    
    - **name**: Product name (required)
    - **description**: Product description (required)
    - **price**: Product price in currency units (required, must be positive)
    - **size**: Product size (required)
    """
    try:
        return await product_service.create_product(product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    name: Optional[str] = Query(None, description="Search products by name (partial match)"),
    size: Optional[str] = Query(None, description="Filter products by size"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip")
):
    """
    Get list of products with optional filtering and pagination
    
    - **name**: Optional name filter (case-insensitive partial match)
    - **size**: Optional size filter (exact match)
    - **limit**: Maximum number of results (1-1000, default: 100)
    - **offset**: Number of results to skip for pagination (default: 0)
    """
    try:
        return await product_service.get_products(
            name=name,
            size=size,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products: {str(e)}"
        )

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """
    Get a single product by ID
    
    - **product_id**: MongoDB ObjectId of the product
    """
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product