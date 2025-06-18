from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.orders.models import Order
from app.core.logger import get_logger

logger = get_logger("orders")


def get_all_orders_for_user(session: Session, user_id: int) -> List[Order]: #get all orders for a specific user past orders also
    try:
        orders = session.query(Order).filter(Order.user_id == user_id).all()
        logger.info(f"Fetched {len(orders)} orders for user_id={user_id}")
        return orders
    except Exception as e:
        logger.error(f"Error fetching orders for user_id={user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve orders"
        )


def get_order_by_id(session: Session, order_id: int, user_id: int) -> Order: # get order detils  by id for a specific user
    try:
        order = session.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        if not order:
            logger.warning(f"Order not found: order_id={order_id} for user_id={user_id}")
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )
        logger.info(f"Fetched order_id={order_id} for user_id={user_id}")
        return order
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error retrieving order_id={order_id} for user_id={user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve the order"
        )
