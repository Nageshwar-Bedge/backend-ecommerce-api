"""
Order API routes
"""
from fastapi import APIRouter, HTTPException, Query, status
from typing import List
from app.models import OrderCreate, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])
order_service = OrderService()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """
    Create a new order
    
    - **user_id**: User identifier (required)
    - **products**: List of product IDs (required, at least one)
    - **total**: Total order amount (required, must be positive)
    """
    try:
        return await order_service.create_order(order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )

@router.get("/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: str,
    limit: int = Query(100, ge=1, le=1000, description="Number of orders to return"),
    offset: int = Query(0, ge=0, description="Number of orders to skip")
):
    """
    Get orders for a specific user with pagination
    
    - **user_id**: User identifier
    - **limit**: Maximum number of results (1-1000, default: 100)
    - **offset**: Number of results to skip for pagination (default: 0)
    """
    try:
        return await order_service.get_orders_by_user(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch orders: {str(e)}"
        )

@router.get("/order/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """
    Get a single order by ID
    
    - **order_id**: MongoDB ObjectId of the order
    """
    order = await order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order