from fastapi import APIRouter, Depends, File,UploadFile, Form
from src.Seller import seller_controller 
from src.Dependencies.check import isLogin
from src.Seller.seller_schema import UpdateStatus, CouponModel

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

# -------------- Status Update -----------
@seller_router.put("/statusupdate/{orderId}")
async def statusUpdate(orderId:str,data:UpdateStatus,user=Depends(isLogin)):
    return await seller_controller.updateStatus(orderId,data,user)

# -------------- Delete Product -------------
@seller_router.delete("/deleteProduct/{productId}")
async def deleteProduct(productId:str,user=Depends(isLogin)):
    return await seller_controller.deleteProduct(productId,user)

# ----------- My Orders -------------
@seller_router.get("/myorders")
async def myorders(user=Depends(isLogin)):
    return await seller_controller.myallorders(user)

# ----------- Order By Status ----------
@seller_router.get("/orderbystatus/{status}")
async def statusByOrder(status:str,user=Depends(isLogin)):
    return await seller_controller.orderByStatus(status,user)

# ----------- Total Orders ----------
@seller_router.get("/totalorder")
async def totalorders(user=Depends(isLogin)):
    return await seller_controller.totalOrders(user)

# ----------- Total Earnings ----------
@seller_router.get("/totalearning")
async def totalEarning(user=Depends(isLogin)):
    return await seller_controller.myEarnings(user)

# ----------- Coupon Add ----------
@seller_router.post("/addcoupon")
async def add_coupon(data:CouponModel,user=Depends(isLogin)):
    return await seller_controller.add_coupon(data,user)

# ----------- Get Coupon ---------
@seller_router.get("/getcoupon")
async def my_Coupons(user=Depends(isLogin)):
    return await seller_controller.get_coupons(user)

# ---------- Delete Coupon ----------
@seller_router.delete("/deletecoupon/{couponId}")
async def delete_coupon(couponId:str,user=Depends(isLogin)):
    return await seller_controller.coupon_delete(couponId,user)