import os
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import products, orders

load_dotenv()

# ✅ Initialize FastAPI application (no lifespan needed)
app = FastAPI(
    title="E-Commerce API",
    description=r"""
## HROne Backend Intern Hiring Task

A complete e-commerce backend API built with FastAPI and in-memory storage.

### Features:
* Product Management: Create and list products with filtering
* Order Management: Place orders and retrieve user order history
* Search & Filter: Advanced product search with pagination
* Data Validation: Comprehensive input validation and error handling

### Tech Stack:
* FastAPI (Python web framework)
* Pydantic (Data validation)
""",
    version="1.0.0",
    contact={
        "name": "HROne Backend Task",
        "url": "https://github.com/hrone-task/ecommerce-api",
    }
)

# ✅ CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/", tags=["Health Check"])
async def root():
    """
    Health check endpoint
    Returns API status and basic information
    """
    return {
        "message": "E-Commerce API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_check():
    """
    Detailed health check endpoint
    """
    return {
        "status": "healthy",
        "service": "E-Commerce API",
        "version": "1.0.0",
        "database": "InMemory",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
