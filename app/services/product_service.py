"""
Product service layer for business logic.
"""
from typing import List, Optional, Dict, Any
from app.database import get_database
from app.models import Product, ProductCreate

class ProductService:
    def __init__(self):
        self.db = get_database()
    
    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product."""
        product_dict = product_data.model_dump()
        created_product = self.db.insert_product(product_dict)
        return Product(**created_product)
    
    def get_products(
        self, 
        name: Optional[str] = None,
        size: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Product]:
        """Get products with optional filtering and pagination."""
        filters = {}
        if name:
            filters["name"] = name
        if size:
            filters["size"] = size
        
        products_data = self.db.find_products(filters, limit, offset)
        return [Product(**product) for product in products_data]
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a product by ID."""
        product_data = self.db.find_product_by_id(product_id)
        if product_data:
            return Product(**product_data)
        return None
    
    def validate_product_ids(self, product_ids: List[str]) -> bool:
        """Validate that all product IDs exist."""
        for product_id in product_ids:
            if not self.db.find_product_by_id(product_id):
                return False
        return True

# Global service instance
product_service = ProductService()