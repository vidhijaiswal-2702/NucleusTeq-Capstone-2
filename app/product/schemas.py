from pydantic import BaseModel,HttpUrl,Field
from typing import Optional
class ProductCreate(BaseModel):  # request body to create product
    name: str 
    description: str 
    price: float =  Field(..., gt=0)
    stock: int 
    category: str
    image_url: HttpUrl = Field(...,description="A valid image URL is required (should start with http/https)",
        example="https://example.com/images/product.jpg")

class Product(ProductCreate):  # response body after product creation
    id: int
    # created_by: int  
    class Config:
        from_attributes = True
        

class ProductSummary(BaseModel): # used to show only basic info of products to customers
    name: str
    price: float
    image_url: HttpUrl

    class Config:
        from_attributes = True