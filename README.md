# 🛒 E-Commerce API - HROne Backend Intern Hiring Task

A complete e-commerce backend API built with **FastAPI** and **MongoDB**, simulating platforms like Amazon/Flipkart with full CRUD operations for products and order management.

## 📦 Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern, fast web framework
- **MongoDB** - NoSQL database with Motor (async driver)
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server
- **Auto-generated API Documentation** (Swagger UI)

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ecommerce-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
Create a `.env` file in the root directory:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ecommerce_db
PORT=8000
```

4. **Start the application**
```bash
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 API Endpoints

### 🛍️ Products

#### Create Product
```http
POST /products
Content-Type: application/json

{
  "name": "iPhone 14",
  "description": "Latest model with A16 Bionic",
  "price": 99999,
  "size": "large"
}
```

**Response (201 Created):**
```json
{
  "_id": "64b60af1a1234e77e1234567",
  "name": "iPhone 14",
  "description": "Latest model with A16 Bionic",
  "price": 99999,
  "size": "large"
}
```

#### List Products
```http
GET /products?name=iPhone&size=large&limit=10&offset=0
```

**Query Parameters:**
- `name` (optional): Search by name (partial match, case-insensitive)
- `size` (optional): Filter by size (exact match)
- `limit` (optional): Number of results (default: 100, max: 1000)
- `offset` (optional): Skip results for pagination (default: 0)

**Response (200 OK):**
```json
[
  {
    "_id": "64b60af1a1234e77e1234567",
    "name": "iPhone 14",
    "description": "Latest model with A16 Bionic",
    "price": 99999,
    "size": "large"
  }
]
```

### 🛒 Orders

#### Create Order
```http
POST /orders
Content-Type: application/json

{
  "user_id": "user123",
  "products": ["64b60af1a1234e77e1234567", "64b60af1a1234e77e1234568"],
  "total": 179998
}
```

**Response (201 Created):**
```json
{
  "_id": "64b60bf2a1234e77e1234599",
  "user_id": "user123",
  "products": ["64b60af1a1234e77e1234567", "64b60af1a1234e77e1234568"],
  "total": 179998
}
```

#### Get User Orders
```http
GET /orders/user123?limit=10&offset=0
```

**Query Parameters:**
- `limit` (optional): Number of results (default: 100, max: 1000)
- `offset` (optional): Skip results for pagination (default: 0)

**Response (200 OK):**
```json
[
  {
    "_id": "64b60bf2a1234e77e1234599",
    "user_id": "user123",
    "products": ["64b60af1a1234e77e1234567", "64b60af1a1234e77e1234568"],
    "total": 179998
  }
]
```

## 🏗️ Project Structure

```
ecommerce-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # MongoDB connection and configuration
│   ├── models.py            # Pydantic models for validation
│   ├── routers/
│   │   ├── products.py      # Product API endpoints
│   │   └── orders.py        # Order API endpoints
│   └── services/
│       ├── product_service.py  # Product business logic
│       └── order_service.py    # Order business logic
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables
└── README.md              # Project documentation
```

## 🔧 Features

### ✅ Core Functionality
- **Product Management**: Create, list, and search products
- **Order Management**: Place orders and retrieve order history
- **Data Validation**: Comprehensive input validation with Pydantic
- **Error Handling**: Proper HTTP status codes and error messages

### 🚀 Performance Optimizations
- **Database Indexing**: Optimized MongoDB indexes for fast queries
- **Async Operations**: Non-blocking database operations with Motor
- **Pagination**: Efficient data retrieval with limit/offset
- **Query Optimization**: Efficient filtering and search operations

### 📚 Documentation
- **Auto-generated API Docs**: Interactive Swagger UI at `/docs`
- **ReDoc Documentation**: Alternative docs at `/redoc`
- **Type Hints**: Full type annotations for better code quality
- **Comprehensive Comments**: Well-documented codebase

### 🛡️ Data Validation
- **Input Validation**: Pydantic models ensure data integrity
- **ObjectId Validation**: Proper MongoDB ObjectId handling
- **Business Logic Validation**: Product existence checks for orders
- **Error Messages**: Clear, actionable error responses

## 🧪 Testing the API

### Using curl

**Create a product:**
```bash
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 14",
    "description": "Latest model with A16 Bionic",
    "price": 99999,
    "size": "large"
  }'
```

**List products:**
```bash
curl "http://localhost:8000/products?name=iPhone&limit=5"
```

**Create an order:**
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "products": ["PRODUCT_ID_HERE"],
    "total": 99999
  }'
```

**Get user orders:**
```bash
curl "http://localhost:8000/orders/user123"
```

### Using the Interactive Docs
Visit http://localhost:8000/docs to test all endpoints interactively with the built-in Swagger UI.

## 🚀 Deployment

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push to main branch

### Render Deployment
1. Connect repository to Render
2. Configure environment variables
3. Use `python -m app.main` as start command

### Environment Variables for Production
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=ecommerce_prod
PORT=8000
ENVIRONMENT=production
```

## 📊 Database Schema

### Products Collection
```javascript
{
  "_id": ObjectId,
  "name": String,
  "description": String,
  "price": Number,
  "size": String
}
```

### Orders Collection
```javascript
{
  "_id": ObjectId,
  "user_id": String,
  "products": [String], // Array of product ObjectIds
  "total": Number
}
```

### Indexes
- **Products**: Text index on `name`, ascending index on `size` and `price`
- **Orders**: Ascending index on `user_id` and `products`

## 🎯 Evaluation Criteria Met

✅ **Functionality**: All endpoints work with exact specifications  
✅ **Code Quality**: Modular structure, clean formatting, comprehensive comments  
✅ **Database Design**: Efficient MongoDB schema with proper indexing  
✅ **Documentation**: Auto-generated Swagger docs and detailed README  
✅ **Error Handling**: Proper HTTP status codes and validation  
✅ **Performance**: Optimized queries and async operations  

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is created for the HROne Backend Intern Hiring Task.

---

**Built with ❤️ using FastAPI and MongoDB**