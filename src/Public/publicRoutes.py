from fastapi import APIRouter
from src.Public import publicController
from src.Public.publicSchema import CreateUser,LoginUser

publicrouter = APIRouter(tags=["Public"])

# ------------- Create User ------------
@publicrouter.post("/signup")
async def signUp(data:CreateUser):
    return await publicController.createUser(data)

# ----------- Login -------------
@publicrouter.post("/loginuser")
async def login(data:LoginUser):
    return await publicController.loginUser(data)

# ----------- All Products ---------
@publicrouter.get("/allproducts")
async def getallproducts():
    return await publicController.all_products()

# ------------- Search Products -----------
@publicrouter.get("/search/{search}")
async def productSearch(search:str):
    return await publicController.serchProducts(search)

# ------------- Filter Products By Indexing --------------
@publicrouter.get("/filter/{search}")
async def productFilter(search:str):
    return await publicController.filterProducts(search)

# -------------- Filter By Price -------------
@publicrouter.get("/filterbyprice/{gtPrice}/{ltPrice}")
async def priceByFilter(gtPrice:int,ltPrice:int):
    return await publicController.filterByPrice(gtPrice,ltPrice)