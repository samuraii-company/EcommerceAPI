from fastapi import FastAPI
import uvicorn
from ecommerce.user import router
from ecommerce.cart import router as cart_router
from ecommerce.products import router as product_router
from ecommerce.orders import router as order_router
from ecommerce.auth import router as auth_router

app = FastAPI(title="EcommerceAPI", version="0.1.0")

app.include_router(auth_router.router)
app.include_router(router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)

@app.get("/")
async def root():
    return {"message": "Ecommerce API"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
