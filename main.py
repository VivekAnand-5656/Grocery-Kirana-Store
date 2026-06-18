from fastapi import FastAPI
from src.Config.cloudinaryConfig import cloudinary
from src.Public.publicRoutes import publicrouter
from src.Seller.seller_routes import seller_router
from src.Customer.customer_routes import customer_route
from src.Config.indexex import create_indexex

app = FastAPI(
    title="Grocery Store"
)

@app.on_event("startup")
async def startup():
    await create_indexex()
 
app.include_router(publicrouter)
app.include_router(seller_router)
app.include_router(customer_route)

