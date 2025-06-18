from app.core.logger import get_logger
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.cart.models import Cart
from app.cart.schemas import CartCreate, CartUpdate
from app.product.models import Product

from fastapi import status,HTTPException

logger = get_logger("cart")


def add_to_cart(db: Session, user_id: int, data: CartCreate):
    try:
        logger.info(f"Adding product {data.product_id} to cart for user {user_id}")

        item_exist = db.query(Cart).filter_by(user_id=user_id, product_id=data.product_id).first()
        if item_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already in cart. Update quantity instead."
            )

        product = db.query(Product).filter_by(id=data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if not (1 <= data.quantity <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be between 1 and 100"
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

    except HTTPException as ht: #custom exceptions
        raise ht 
    
    except Exception as e:  #detect unexcepted errors
        logger.error(f"Error adding to cart: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to add product to cart")


def get_cart_items(db: Session, user_id: int): #get cart items present for current signed in user
    try:
        logger.info(f"Fetching cart items for user {user_id}")
        
        return db.query(Cart).filter_by(user_id=user_id).all()

    except Exception as e:
        logger.error(f"Error fetching cart items: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch cart items")


def remove_cart_item(db: Session, user_id: int, product_id: int):
    try:
        logger.info(f"Removing product {product_id} from user {user_id}'s cart")

        cart_item = db.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        db.delete(cart_item)
        db.commit()

        logger.info("Item removed from cart successfully")
        return { "message": "Item removed from the cart successfully.", "code": 200}

    except HTTPException as ht:
        raise ht
    except Exception as e:
        logger.error(f"Error removing cart item: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to remove item from cart")


def update_cart_quantity(db: Session, user_id: int, product_id: int, update_data: CartUpdate): #cartupdate-> as response model
    try:
        logger.info(f"Updating quantity of product {product_id} in user {user_id}'s cart")

        cart_item = db.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        if not (1 <= update_data.quantity <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be between 1 and 100"
            )

        cart_item.quantity = update_data.quantity # only quantity updated
        db.commit()
        db.refresh(cart_item)

        logger.info("Cart quantity updated successfully")
        return cart_item

    except HTTPException as ht:
        raise ht
    except Exception as e:
        logger.error(f"Error updating cart quantity: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update cart quantity")
