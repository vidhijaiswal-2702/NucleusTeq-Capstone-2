from app.auth.models import User
from app.cart.models import Cart
from app.core.logger import get_logger
from app.orders.models import Order, OrderItem
from fastapi import HTTPException
from sqlalchemy.orm import Session

from datetime import datetime

logger = get_logger("checkout")

def perform_checkout(session: Session, current_user: User):
    try:
        cart_items = session.query(Cart).filter(Cart.user_id == current_user.id).all()

        if not cart_items:
            logger.warning(f"Checkout attempt with empty cart by user_id={current_user.id}")
            raise HTTPException(status_code=400, detail="Cart is empty")

        total_amount = 0
        order_items = []

        for item in cart_items:
            if not item.product:
                logger.error(f"Cart item with product_id={item.product_id} has no associated product.")
                raise HTTPException(status_code=400, detail="Invalid product in cart.")

            item_total = item.product.price * item.quantity
            total_amount += item_total
            order_items.append(OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
                product_name=item.product.name,
                product_description=item.product.description
            ))

        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            status="paid",  # mock payment success
            created_at=datetime.utcnow(),
            items=order_items
        )

        session.add(order)

        for item in cart_items:
            session.delete(item)

        session.commit()
        session.refresh(order)

        logger.info(f"Checkout successful for user_id={current_user.id} | order_id={order.id} | amount={total_amount}")
        return {
            "message": "Checkout successful",
            "order_id": order.id,
            "total_amount": total_amount
        }

    except HTTPException as http_exc:
        raise http_exc  

    except Exception as e:
        session.rollback()
        logger.error(f"Checkout failed for user_id={current_user.id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process checkout"
        )
