from app.auth.base import BaseResponse
from app.product.schemas import Product, ProductSummary
from pydantic import BaseModel, EmailStr, Field, field_validator,PositiveInt, conint # type: ignore
from app.auth.roles import UserRole
from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt, conint
from typing import Optional

# Shared base schema for reuse
class CartBase(BaseModel):
    product_id: PositiveInt = Field(..., description="ID of the product (must be > 0)")
    quantity: Annotated [ conint(ge=1, le=100) , Field(..., description="Quantity must be between 1 and 100")]

# Schema for cart item creation
class CartCreate(CartBase):
    pass

# Schema for updating quantity
class CartUpdate(BaseModel):
    quantity: Annotated[conint(ge=1, le=100) , Field(..., description="Updated quantity must be between 1 and 100")]

# Schema for returning cart data
class CartResponse(BaseModel):
    # id: int = Field(..., description="Cart item ID")
    # user_id: int = Field(..., description="ID of the user who owns this cart item")
    product_id: PositiveInt = Field(..., description="Product ID")
    quantity:Annotated [conint(ge=1,le=100), Field(..., description="Quantity of the product in cart")]
    product: ProductSummary

    class Config:
        from_attributes = True

