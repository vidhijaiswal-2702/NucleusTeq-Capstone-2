from app.auth.models import User
from app.core.security import user_required
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session

from app.checkout.services import perform_checkout

checkout_router = APIRouter(prefix="/checkout",
    tags=["checkout"],
    responses={404: {"description": "Not found"}},)

#Mocks paymment and checkout the products in cart

@checkout_router.post("/checkout", status_code=status.HTTP_201_CREATED)
async def checkout(
    session: Session = Depends(get_session), 
    current_user: User = Depends(user_required)
    ):
    return await perform_checkout(session, current_user)
