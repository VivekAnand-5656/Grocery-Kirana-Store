from fastapi import APIRouter, Depends, File,UploadFile, Form
from src.Seller import seller_controller 
from src.Dependencies.check import isLogin

seller_router = APIRouter(prefix="/sellers",tags=["Seller"])

# -------- Update Profile ------------
@seller_router.put("/updateprofile")
async def profile_update(
    name:str = Form(...),
    email:str = Form(...),
    mobile:str = Form(...),
    shopname:str = Form(...),
    address:str = Form(...),
    city:str = Form(...),
    state:str = Form(...),
    pincode:int = Form(...),
    file:UploadFile = File(...),
    user=Depends(isLogin)
):
    return await seller_controller.updateProfile(name,email,mobile,shopname,address,city,state,pincode,file,user)

# --------------- My Profile ------------
@seller_router.get("/myprofile")
async def getprofile(user=Depends(isLogin)):
    return await seller_controller.myprofile(user)

# ------------ Add Products -----------
@seller_router.put("/addproduct")
async def productadd(
    productname:str = Form(...),
    detail:str = Form(...),
    category:str = Form(...),
    brand:str = Form(...),
    price:float = Form(...),
    discount:int = Form(...), 
    unit:str = Form(...),
    isAvailable:bool =Form(...),
    file:UploadFile = File(...),
    user=Depends(isLogin)
):
    return await seller_controller.addProduct(productname,detail,category,brand,price,discount,unit,isAvailable,file,user)

# --------------- My Products ----------
@seller_router.get("/myproducts")
async def myproducts(user=Depends(isLogin)):
    return await seller_controller.my_products(user)

# ------------------ Update Products --------------
@seller_router.put("/updateproduct/{productId}")
async def productUpdate(
    productId:str,
    productname:str = Form(...),
    detail:str = Form(...),
    category:str = Form(...),
    brand:str = Form(...),
    price:float = Form(...),
    discount:int = Form(...), 
    unit:str = Form(...),
    isAvailable:bool =Form(...),
    file:UploadFile = File(...),
    user=Depends(isLogin)
):
    return await seller_controller.updateProduct(productId,productname,detail,category,brand,price,discount,unit,isAvailable,file,user)

# ------------- Update Availbility -----------
@seller_router.patch("/updateavailable/{productId}")
async def availableUpdate(productId:str,isAvailable:bool = Form(...),user=Depends(isLogin)):
    return await seller_controller.updateIsAvailable(productId,isAvailable,user)

# -------------- Delete Product -------------
@seller_router.delete("/deleteProduct/{productId}")
async def deleteProduct(productId:str,user=Depends(isLogin)):
    return await seller_controller.deleteProduct(productId,user)