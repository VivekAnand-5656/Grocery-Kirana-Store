from fastapi import APIRouter,Depends
from src.Dependencies.check import isLogin
from src.Customer import customer_controlle
from src.Customer.customer_schema import UpdateProfile
from typing import Optional

customer_route = APIRouter(prefix="/customer",tags=["Customer"])

# --------------- Update Profile -----------
@customer_route.put("/updateprofile")
async def profileUpdate(data:UpdateProfile,user=Depends(isLogin)):
    return await customer_controlle.updateProfile(data,user)

# ---------------- My Profile -------------
@customer_route.get("/myprofile")
async def myprofile(user=Depends(isLogin)):
    return await customer_controlle.myProfile(user)

# --------------- Buy Product By Id ---------------
@customer_route.put("/buyProduct/{productId}")
async def productBuy(productId:str,quantity:int | None = None ,user=Depends(isLogin)):
    return await customer_controlle.buyProduct(productId,quantity,user)

# ------------------- My Orders ------------
@customer_route.get("/myorders")
async def myOrders(user=Depends(isLogin)):
    return await customer_controlle.myorders(user)

# ------------------- Add To Wishlist --------------
@customer_route.put("/addtowishlist/{productId}")
async def addtowishlist(productId:str,user=Depends(isLogin)):
    return await customer_controlle.addToWishlist(productId,user)

# ------------------ My Wishlists --------------
@customer_route.get("/mywishlist")
async def mywishlists(user=Depends(isLogin)):
    return await customer_controlle.myWishlists(user)

# ------------------- Remove From Wishlist --------------
@customer_route.put("/removewishlist/{productId}")
async def removewishlist(productId:str,user=Depends(isLogin)):
    return await customer_controlle.removeWishlist(productId,user)

# ------------ Add to Cart ----------------
@customer_route.put("/addtocart/{productId}")
async def addToCart(productId:str,user=Depends(isLogin)):
    return await customer_controlle.addtocart(productId,user)

# ---------------------- My Carts ---------------
@customer_route.get("/mycarts")
async def myCarts(user=Depends(isLogin)):
    return await customer_controlle.mycarts(user)

# ---------------- Cart Total ------------
@customer_route.get("/carttotal")
async def totaOfCart(user=Depends(isLogin)):
    return await customer_controlle.cartTotal(user)

# ----------------- Update Cart Quantity ---------
@customer_route.put("/increasecartquantity/{productId}")
async def increaseQuantity(productId:str,user=Depends(isLogin)):
    return await customer_controlle.increaseQuantity(productId,user)
# ----------------- Update Decrease Cart Quantity ---------
@customer_route.put("/decreasecartquantity/{productId}")
async def decreaseQuantity(productId:str,user=Depends(isLogin)):
    return await customer_controlle.decreaseQuantity(productId,user)

# ---------- Remove Cart ----------
@customer_route.put("/removeCart/{productId}")
async def cartRemove(productId:str,user=Depends(isLogin)):
    return await customer_controlle.removeCart(productId,user)

# --------- Order Place ---------------
@customer_route.put("/placeorder")
async def orderplace(user=Depends(isLogin)):
    return await customer_controlle.placeOrder(user)
