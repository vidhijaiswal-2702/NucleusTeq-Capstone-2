from fastapi import FastAPI, Request ,HTTPException
 # type: ignore
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.auth.routes import user_router, guest_router, auth_router
from app.product.routes import product_router, public_product_router
from app.cart.routes import cart_router
from app.orders.routes import order_router
from app.checkout.routes import checkout_router
from app.core.logger import get_logger

logger = get_logger("global")

app = FastAPI(debug=True)  

#  include routers here
app.include_router(user_router)
app.include_router(guest_router)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(public_product_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(order_router)

# root route
@app.get("/")
def read_root():
    return {"message": "Welcome to our E-commerce Backend System!!"}

# exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"{request.method} {request.url} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail, "code": exc.status_code},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"{request.method} {request.url} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "code": exc.status_code
        },
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal server error", "code": 500},
    )
