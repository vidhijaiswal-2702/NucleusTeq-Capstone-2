from app.auth.models import User
from app.core.security import  get_current_user, user_required
from app.cart import schemas, services
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_session
from fastapi.responses import JSONResponse

cart_router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    responses={404: {"description": "Not found"}},)

@cart_router.post("/", response_model=schemas.CartResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    cart_data: schemas.CartCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(user_required)
):
    return services.add_to_cart(db, current_user.id, cart_data)


@cart_router.get("/", response_model=list[schemas.CartResponse])
def view_cart(
    db: Session = Depends(get_session),
    current_user: User = Depends(user_required)
):
    return services.get_cart_items(db, current_user.id)


@cart_router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(user_required)
):
    return services.remove_cart_item(db, current_user.id, product_id)
    


@cart_router.put("/{product_id}", response_model=schemas.CartResponse)
def update_cart_quantity(
    product_id: int,
    update_data: schemas.CartUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(user_required)
):
    return services.update_cart_quantity(db, current_user.id, product_id, update_data)