from typing import List, Optional

from app.auth.models import User
from app.core.logger import get_logger
from fastapi import HTTPException, status

from app.product.models import Product
from app.product.schemas import ProductCreate
from sqlalchemy.orm import Session

logger = get_logger("product")


def create_product(db: Session, product: ProductCreate,current_user: User):
    try:
        if not product.name:
            raise HTTPException(status_code=400,detail="Enter a valid product name")
        if not product.price:
            raise HTTPException(status_code=400,detail="Enter price")
        if not product.stock:
            raise HTTPException(status_code=400,detail="Stock of item is mandatory")
        if not product.category:
            raise HTTPException(status_code=400,detail="Enter a valid product category")
        if not product.image_url:
            raise HTTPException(status_code=400,detail="Enter an image url")
        
        db_product = Product(
            name = product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=product.category,
            image_url=str(product.image_url),
            created_by=current_user.id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Product created: {db_product.name}")
        return db_product
    
    except HTTPException as http_exc:
        logger.warning(f"Validation error during product creation: {http_exc.detail}")
        raise http_exc  # Re-raise excepion to catch custom validation errors

    except Exception as e: #any unexcepted errors -> internal server error
        logger.error(f"Error creating product: {e}",exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create product")
        


def get_products(db: Session, skip: int = 0, limit: int = 10):
    try:
        logger.debug(f"Fetching products skip={skip},limit={limit}")
        return db.query(Product).offset(skip).limit(limit).all()
    
    except Exception as e:
        logger.error(f"Error fetching products:{e}",exc_info=True)
        raise HTTPException(status_code=500,detail="Failed to fetch products")
    


def get_product_by_id(db: Session, product_id: int):
    try:
        logger.debug(f"Fetching product ID: {product_id}")
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f"Product not found: ID {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        logger.error(f"Error getting product by ID: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get product")
    
   

def update_product(db: Session, product_id: int, updated_data: ProductCreate,current_user: User):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f"Product not found for update: ID {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        
        if product.created_by != current_user.id:
            logger.warning(f"Unauthorized product update attempt by user {current_user.email}")
            raise HTTPException(status_code=403, detail="You are not allowed to update this product.")

        product.name = updated_data.name
        product.description = updated_data.description
        product.price = updated_data.price
        product.stock = updated_data.stock
        product.category = updated_data.category
        product.image_url = str(updated_data.image_url) 

        db.commit()
        db.refresh(product)
        
        logger.info(f"Product updated: ID {product_id}")
        return product
    
    except HTTPException as http_exc:
        logger.warning(f"Validation error during product updation: {http_exc.detail}")
        raise http_exc   # Re-raise excepion to catch custom validation errors

    except Exception as e:
        logger.error(f"Error updating product ID {product_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update product")



def delete_product(db: Session, product_id: int, current_user:User):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f"Product not found for deletion: ID {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        
        if product.created_by != current_user.id:
            logger.warning(f"Unauthorized product deletion attempt by {current_user.email}")
            raise HTTPException(status_code=403, detail="You are not allowed to delete this product.")

        db.delete(product)
        db.commit()
        logger.info(f"Product deleted: ID {product_id}")
        
    except HTTPException as http_exc:
        logger.warning(f"Validation error during product deletion: {http_exc.detail}")
        raise http_exc  #  Re-raise excepion to catch custom validation errors

    except Exception as e:
        logger.error(f"Error deleting product: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete product")
    
    
#PUBLIC PRODUCT APIS

def list_products_service(
    session: Session,
    category: Optional[str],
    min_price: Optional[float],
    max_price: Optional[float],
    sort_by: Optional[str],
    skip: int=0,
    limit: int=10
) -> List[Product]:
    try:
        logger.debug("Listing products with filters")
        query = session.query(Product)

        if category:
            query = query.filter(Product.category.ilike(f"%{category}%")) #ilike means matches case insensative values

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if sort_by == "price_asc":
            query = query.order_by(Product.price.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort_by == "name":
            query = query.order_by(Product.name.asc())

        products = query.offset(skip).limit(limit).all()
        return products
    except Exception as e:
        logger.error(f"Error listing products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list products")

def search_products_service(
    session: Session,
    keyword: str
) -> List[Product]:
    try:
        logger.debug(f"Searching products by keyword: {keyword}")
        return session.query(Product).filter(
            (Product.name.ilike(f"%{keyword}%")) |
            (Product.description.ilike(f"%{keyword}%"))
        ).all()
    except Exception as e:
        logger.error(f"Error searching products: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to search products")