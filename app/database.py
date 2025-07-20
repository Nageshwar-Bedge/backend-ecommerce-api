"""
Database configuration using in-memory storage for WebContainer compatibility.
"""
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

class InMemoryDatabase:
    """In-memory database implementation for WebContainer compatibility."""
    
    def __init__(self):
        self.products: Dict[str, Dict] = {}
        self.orders: Dict[str, Dict] = {}
        self._product_counter = 1
        self._order_counter = 1
    
    def generate_id(self, collection: str) -> str:
        """Generate a simple ID for documents."""
        if collection == "products":
            id_val = f"prod_{self._product_counter:06d}"
            self._product_counter += 1
        else:
            id_val = f"order_{self._order_counter:06d}"
            self._order_counter += 1
        return id_val
    
    def insert_product(self, product_data: Dict) -> Dict:
        """Insert a product into the database."""
        product_id = self.generate_id("products")
        product_data["_id"] = product_id
        self.products[product_id] = product_data
        return product_data
    
    def find_products(self, filters: Dict = None, limit: int = None, offset: int = 0) -> List[Dict]:
        """Find products with optional filtering."""
        products = list(self.products.values())
        
        if filters:
            if "name" in filters:
                name_filter = filters["name"].lower()
                products = [p for p in products if name_filter in p["name"].lower()]
            if "size" in filters:
                products = [p for p in products if p["size"] == filters["size"]]
        
        # Apply pagination
        start = offset
        end = start + limit if limit else len(products)
        return products[start:end]
    
    def find_product_by_id(self, product_id: str) -> Optional[Dict]:
        """Find a product by ID."""
        return self.products.get(product_id)
    
    def insert_order(self, order_data: Dict) -> Dict:
        """Insert an order into the database."""
        order_id = self.generate_id("orders")
        order_data["_id"] = order_id
        order_data["created_at"] = datetime.utcnow().isoformat()
        self.orders[order_id] = order_data
        return order_data
    
    def find_orders_by_user(self, user_id: str, limit: int = None, offset: int = 0) -> List[Dict]:
        """Find orders by user ID."""
        user_orders = [order for order in self.orders.values() if order["user_id"] == user_id]
        
        # Apply pagination
        start = offset
        end = start + limit if limit else len(user_orders)
        return user_orders[start:end]

# Global database instance
db = InMemoryDatabase()

def get_database():
    """Get database instance."""
    return db