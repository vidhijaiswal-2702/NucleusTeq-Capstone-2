from app.auth.models import User
from app.core.security import user_required
from app.orders.schemas import OrderResponse, OrderSummary
from app.orders.services import get_all_orders_for_user, get_order_by_id
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_session


order_router = APIRouter(prefix="/orders", tags=["Orders"],
                         responses={404: {"description": "Not found"}},)

@order_router.get("", response_model=List[OrderSummary])
def get_orders(
    session: Session = Depends(get_session), 
    current_user:User=Depends(user_required)
    ):
    return  get_all_orders_for_user(session, current_user.id)

@order_router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id: int, 
    session: Session = Depends(get_session), 
    current_user:User=Depends(user_required)
    ):
    order = get_order_by_id(session, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
