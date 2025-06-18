from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class OrderItemResponse(BaseModel): # represent the response schema for order items list
    # product_id: Optional[int]
    product_name: str
    product_description: str
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel): #response schema for order full details
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes= True


class OrderSummary(BaseModel): # represent the response schema for order summary
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True
