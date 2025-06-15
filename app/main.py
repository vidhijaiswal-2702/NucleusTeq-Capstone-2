from app.core.logger import get_logger
from fastapi import FastAPI , Request# type: ignore
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.auth.routes import user_router, guest_router, auth_router

from app.product.routes import product_router,public_product_router

from app.cart.routes import cart_router
from app.orders.routes import order_router
from app.checkout.routes import checkout_router


logger = get_logger("global")

app = FastAPI(debug=True)

def create_app():
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(guest_router)
    app.include_router(auth_router)
    app.include_router(product_router)
    app.include_router(public_product_router)
    app.include_router(cart_router)
    app.include_router(checkout_router)
    app.include_router(order_router)
    
    
  
    return app

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"{request.method} {request.url} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail, "code": exc.status_code},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": True, "message": "Validation error", "code": 422},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal server error", "code": 500},
    )

 
 
app = create_app()
@app.get("/")
def read_root():
    return {"message": "Welcome to our E-commerce Backend System!!1"}