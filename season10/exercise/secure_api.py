from fastapi import FastAPI, Query, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import re
import html
import logging
import uuid
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Secure API Example",
    description="An example of a secure FastAPI application with proper input validation",
    version="1.0.0"
)

# Add security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trusted-site.com"],  # Restrict to trusted origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample database of products (in a real app, this would be a proper database)
PRODUCTS = {
    1: {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 999.99},
    2: {"id": 2, "name": "Smartphone", "description": "Latest smartphone model", "price": 699.99},
    3: {"id": 3, "name": "Headphones", "description": "Noise-cancelling headphones", "price": 199.99},
}

# Define validation models with Pydantic
class ProductSearchQuery(BaseModel):
    query: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Search query string"
    )
    
    # Validate search query to prevent injection attacks
    @validator('query')
    def sanitize_query(cls, v):
        # Remove any potentially dangerous characters
        # Only allow alphanumeric characters, spaces and some punctuation
        if not re.match(r'^[a-zA-Z0-9\s\.,\-_\'\"]+$', v):
            raise ValueError("Search query contains invalid characters")
        return v

# Request ID middleware to help with request tracing
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    # Add request_id to request state
    request.state.request_id = request_id
    
    # Add security headers
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Request-ID"] = request_id
    return response

# Dependency for request logging
async def log_request(request: Request):
    request_id = request.state.request_id
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"Request {request_id} received from {client_host} - {request.method} {request.url.path}")
    return request_id

# Define the endpoint
@app.get("/api/products/search", response_model=Dict[str, Any])
async def search_products(
    request_id: str = Depends(log_request),
    query: str = Query(
        ..., 
        min_length=1, 
        max_length=100,
        description="Search term for product"
    ),
    category: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        regex="^[a-zA-Z0-9\-_]+$",  # Strict validation for category
        description="Product category filter"
    ),
    max_price: Optional[float] = Query(
        None,
        gt=0,
        lt=100000,
        description="Maximum price filter"
    )
):
    """
    Search for products based on query string and optional filters.
    All inputs are properly validated and sanitized.
    """
    try:
        # Validate query using Pydantic model
        validated_query = ProductSearchQuery(query=query)
        
        # Sanitize inputs to prevent XSS
        safe_query = html.escape(validated_query.query)
        
        # Log the sanitized search
        logger.info(f"Request {request_id}: Searching for products with query: '{safe_query}'")
        
        # Perform the search (simplified for example)
        results = []
        for product in PRODUCTS.values():
            # Case-insensitive search in name or description
            if (safe_query.lower() in product["name"].lower() or 
                safe_query.lower() in product["description"].lower()):
                
                # Apply category filter if specified
                if category and category != "all":
                    # In a real app, you'd check the product category
                    continue
                
                # Apply price filter if specified
                if max_price is not None and product["price"] > max_price:
                    continue
                    
                # Add matching product to results
                results.append(product)
        
        # Return safe, structured response
        return {
            "request_id": request_id,
            "query": safe_query,
            "filters": {
                "category": category,
                "max_price": max_price
            },
            "result_count": len(results),
            "results": results
        }
        
    except ValueError as e:
        # Log the validation error
        logger.warning(f"Request {request_id}: Validation error: {str(e)}")
        
        # Return a safe error message (don't leak implementation details)
        raise HTTPException(
            status_code=400,
            detail="Invalid search parameters. Please check your input."
        )
    except Exception as e:
        # Log the unexpected error
        logger.error(f"Request {request_id}: Unexpected error: {str(e)}")
        
        # Return a generic error (don't expose internal errors to clients)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

# Default route with security information
@app.get("/")
async def root():
    return {
        "message": "Secure API Example",
        "documentation": "/docs",
        "security_features": [
            "Input validation and sanitization",
            "XSS protection",
            "Security headers",
            "Request tracing",
            "Proper error handling",
            "CORS protection"
        ]
    }

# Main function to run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("secure_api:app", host="0.0.0.0", port=8000, reload=False)