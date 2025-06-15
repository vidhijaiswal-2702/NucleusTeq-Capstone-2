from app.core.logger import get_logger
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.cart.models import Cart
from app.cart.schemas import CartCreate, CartUpdate
from app.product.models import Product

from fastapi import status

logger = get_logger("cart")


def add_to_cart(db: Session, user_id: int, data: CartCreate):
    try:
        logger.info(f"Adding product {data.product_id} to cart for user {user_id}")

        existing_item = db.query(Cart).filter_by(user_id=user_id, product_id=data.product_id).first()
        if existing_item:
            logger.warning("Product already in cart")
            return JSONResponse(
                status_code=400,
                content={"error": True, "message": "Product already in cart. Update quantity instead.", "code": 400}
            )

        product = db.query(Product).filter_by(id=data.product_id).first()
        if not product:
            logger.warning("Product not found")
            return JSONResponse(
                status_code=404,
                content={"error": True, "message": "Product not found", "code": 404}
            )

        if data.quantity < 1 or data.quantity > 100:
            logger.warning("Invalid quantity")
            return JSONResponse(
                status_code=400,
                content={"error": True, "message": "Quantity must be between 1 and 100", "code": 400}
            )

        cart_item = Cart(
            user_id=user_id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        logger.info("Product added to cart successfully")
        return cart_item

    except Exception as e:
        logger.error(f"Error adding to cart: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": "Failed to add product to cart", "code": 500}
        )


def get_cart_items(db: Session, user_id: int):
    try:
        logger.info(f"Fetching cart items for user {user_id}")
        return db.query(Cart).filter_by(user_id=user_id).all()
    except Exception as e:
        logger.error(f"Error fetching cart items: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": "Failed to fetch cart items", "code": 500}
        )


def remove_cart_item(db: Session, user_id: int, product_id: int):
    try:
        logger.info(f"Removing product {product_id} from user {user_id}'s cart")

        cart_item = db.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not cart_item:
            logger.warning("Cart item not found")
            return JSONResponse(
                status_code=404,
                content={"error": True, "message": "Cart item not found", "code": 404}
            )

        db.delete(cart_item)
        db.commit()
        logger.info("Item removed from cart successfully")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"error": False, "message": "Item removed from the cart successfully.", "code": 200}
        )
    except Exception as e:
        logger.error(f"Error removing cart item: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": "Failed to remove item from cart", "code": 500}
        )


def update_cart_quantity(db: Session, user_id: int, product_id: int, update_data: CartUpdate):
    try:
        logger.info(f"Updating quantity of product {product_id} in user {user_id}'s cart")

        cart_item = db.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not cart_item:
            logger.warning("Cart item not found")
            return JSONResponse(
                status_code=404,
                content={"error": True, "message": "Cart item not found", "code": 404}
            )

        if update_data.quantity < 1 or update_data.quantity > 100:
            logger.warning("Invalid quantity")
            return JSONResponse(
                status_code=400,
                content={"error": True, "message": "Quantity must be between 1 and 100", "code": 400}
            )

        cart_item.quantity = update_data.quantity
        db.commit()
        db.refresh(cart_item)
        logger.info("Cart quantity updated successfully")
        return cart_item

    except Exception as e:
        logger.error(f"Error updating cart quantity: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": "Failed to update cart quantity", "code": 500}
        )
