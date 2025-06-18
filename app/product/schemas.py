from pydantic import BaseModel,HttpUrl,Field,validator,field_validator
from typing import Literal, Optional
class ProductCreate(BaseModel):  # request body to create product
    name: str = Field(..., min_length=1, max_length=100, description="Product name must be between 1 and 100 characters")   
    description: str
    price: float = Field(..., gt=0, description="Price must be a non-negative number") 
    stock: int  = Field(..., ge=0, description="Stock must be a non-negative integer")
    category: str = Field(..., min_length=1, max_length=50, description="Category must be between 1 and 50 characters")
    image_url: HttpUrl = Field(
        ...,
        description="A valid image URL is required (should start with http/https)",
        example="https://example.com/images/product.jpg"
    )
    class Config:
        extra = "forbid"
    
    
    
  # response body after product creation   
class Product(ProductCreate): 
    id: int
    created_by: int  
    class Config:
        from_attributes = True
        

# used to show only basic info of products to customers : response body for product listing
class ProductSummary(BaseModel): 
    name: str
    price: float
    image_url: HttpUrl

    class Config:
        from_attributes = True
        
        
class ProductFilterParams(BaseModel): # used to filter products based on category, price range, sorting and pagination
    category: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    sort_by: Optional[Literal["price_asc", "price_desc", "name"]] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)

    @validator("max_price") #custom validation to ensure max_price is greater than or equal to min_price
    def validate_price_range(cls, v, values):
        min_price = values.get("min_price")
        if v is not None and min_price is not None and v < min_price:
            raise ValueError("max_price must be greater than or equal to min_price")
        return v

    def offset(self) -> int:  # calculates the offset for pagination means how many records to skip and start from which record
        return (self.page - 1) * self.page_size