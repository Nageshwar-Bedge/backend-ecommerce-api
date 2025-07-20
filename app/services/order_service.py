"""
Order service layer for business logic.
"""
from typing import List, Optional
from app.database import get_database
from app.models import Order, OrderCreate
from app.services.product_service import product_service

class OrderService:
    def __init__(self):
        self.db = get_database()
    
    def create_order(self, order_data: OrderCreate) -> Order:
        """Create a new order."""
        # Validate that all products exist
        if not product_service.validate_product_ids(order_data.products):
            raise ValueError("One or more products do not exist")
        
        order_dict = order_data.model_dump()
        created_order = self.db.insert_order(order_dict)
        return Order(**created_order)
    
    def get_orders_by_user(
        self, 
        user_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Order]:
        """Get orders for a specific user with pagination."""
        orders_data = self.db.find_orders_by_user(user_id, limit, offset)
        return [Order(**order) for order in orders_data]

# Global service instance
order_service = OrderService()