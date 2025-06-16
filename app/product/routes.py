from typing import List, Optional
from app.auth.models import User
from app.core.security import admin_required, get_current_user
from app.product import schemas, services
from fastapi import APIRouter, Depends, HTTPException,status,Query
from sqlalchemy.orm import Session
from app.core.database import get_session
from fastapi.responses import JSONResponse


product_router = APIRouter(prefix="/products",     #for product crud
    tags=["products"],
    responses={404: {"description": "Not found"}},)

public_product_router = APIRouter(prefix="/public",  #for public product apis
    tags=["public"],
    responses={404: {"description": "Not found"}},)


@product_router.post("/create-products",status_code=status.HTTP_200_OK, response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(admin_required),  # Restrict to admin users
):
    """
    Create a new product (Admin only).
    """
    return  services.create_product(db=db, product=product,current_user=current_user)



@product_router.get("/", response_model=list[schemas.Product])
def get_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
    current_user: User = Depends(admin_required),
):
    """
    Get list of products with pagination (Admin only).
    """
    return  services.get_products(db=db, skip=skip, limit=limit)


@product_router.get("/{id}", response_model=schemas.Product)
def get_product_by_id(
    id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(admin_required),
):
    """
    Get a specific product by ID (Admin only).
    """
    return services.get_product_by_id(db=db, product_id=id)


@product_router.put("/{id}", response_model=schemas.Product)
def update_product(
    id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(admin_required),
):
    """
    Update a product by ID (Admin only).
    """
    return services.update_product(db=db, product_id=id, updated_data=updated_product, current_user=current_user)


@product_router.delete("/{product_id}", response_class=JSONResponse)
def delete_product(
    product_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(admin_required)
):
    services.delete_product(product_id=product_id, db=db, current_user=current_user)
    return JSONResponse(status_code=200, content={"message": "Product deleted successfully"})

   
@public_product_router.get("/products", response_model=List[schemas.Product])
def list_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query(None, description="Options: price_asc, price_desc"),
    page: int = 1,
    page_size: int = 10,
    session: Session = Depends(get_session)
):
    return  services.list_products_service(session, category, min_price, max_price, sort_by, page, page_size)


@public_product_router.get("/products/search", response_model=List[schemas.Product])
def search_products(
    keyword: str,
    session: Session = Depends(get_session)
):
    return  services.search_products_service(session, keyword)
 


