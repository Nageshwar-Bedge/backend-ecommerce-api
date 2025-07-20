"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ProductCreate(BaseModel):
    """Product creation model"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: str = Field(..., min_length=1, max_length=1000, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    size: str = Field(..., min_length=1, max_length=50, description="Product size")

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return round(v, 2)

class ProductResponse(BaseModel):
    """Product response model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    price: float
    size: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OrderCreate(BaseModel):
    """Order creation model"""
    user_id: str = Field(..., min_length=1, max_length=100, description="User identifier")
    products: List[str] = Field(..., min_items=1, description="List of product IDs")
    total: float = Field(..., gt=0, description="Total order amount")

    @validator('products')
    def validate_products(cls, v):
        if not v:
            raise ValueError('At least one product is required')
        # Validate ObjectId format for each product
        for product_id in v:
            if not ObjectId.is_valid(product_id):
                raise ValueError(f'Invalid product ID: {product_id}')
        return v

    @validator('total')
    def validate_total(cls, v):
        if v <= 0:
            raise ValueError('Total must be positive')
        return round(v, 2)

class OrderResponse(BaseModel):
    """Order response model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    products: List[str]
    total: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}