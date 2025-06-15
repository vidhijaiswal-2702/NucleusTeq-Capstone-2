from pydantic import BaseModel,HttpUrl,Field
from typing import Optional
class ProductCreate(BaseModel):
    name: str 
    description: str 
    price: float 
    stock: int 
    category: str
    image_url: HttpUrl = Field(...,description="A valid image URL is required (should start with http/https)",
        example="https://example.com/images/product.jpg")

class Product(ProductCreate):  # Inherit from ProductCreate
    id: int
    created_by: int  
    class Config:
        from_attributes = True
        
class ProductSummary(BaseModel):
    name: str
    price: float
    image_url: HttpUrl

    class Config:
        from_attributes = True