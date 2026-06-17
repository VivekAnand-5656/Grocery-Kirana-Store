from fastapi import HTTPException
from src.Config.db import productCollection,sellersCollection,customerCollection
from src.Customer.customer_schema import UpdateProfile
from bson import ObjectId
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from src.Config.cloudinaryConfig import upload_image
from typing import Optional

# =========== Update Profile =========
async def updateProfile(data,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    await customerCollection.update_one(
        {"_id":customer["_id"]},
        {
            "$set":{
                "name":data.name,
                "email":data.email,
                "mobile":data.mobile,
                "address":data.address,
                "city":data.city,
                "state":data.state,
                "pincode":data.pincode
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Profile Updated"
        },
        custom_encoder={ObjectId:str}
    )

# ============ My Profile ==========
async def myProfile(user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    
    return jsonable_encoder(
        customer,
        custom_encoder={ObjectId:str}
    )

# ============ Buy Product By Id ================
async def buyProduct(productId:str,quantity:int | None,user=None):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    product = await productCollection.find_one(
        {"_id":ObjectId(productId)}
    )
    if not product:
        raise HTTPException(404,detail="Product not found")
    if quantity is None:
        quantity = 1
    totalprice = quantity * product["discount_price"]
    await customerCollection.update_one(
        {"_id":customer["_id"]},
        {
            "$push":{
                "myorders":{
                    "product_id":product["_id"],
                    "totalPrice":totalprice,
                    "quantity":quantity
                }
            }
        }
    )
    return jsonable_encoder(
        {
            "msg":"Product Buy Successfully"
        },
        custom_encoder={ObjectId:str}
    )

# ================ My Orders ===========
async def myorders(user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    
    orders = await customerCollection.aggregate([
        {
            "$match":{
                "_id":customer["_id"]
            }
        },
        {
            "$unwind":"$myorders"
        },
        {
            "$lookup":{
                "from":"products",
                "localField":"myorders.product_id",
                "foreignField":"_id",
                "as":"allOrders"
            }
        },
        {
            "$unwind":"$allOrders"
        },
        {
            "$project":{
                "_id":0,
                "quantity":"$myorders.quantity",
                "totalPrice":"$myorders.totalPrice",
                "allOrders":1
            }
        }
    ]).to_list(length=None)
    if not orders:
        raise HTTPException(404,detail="Empty Orders")
    return jsonable_encoder(
        orders,
        custom_encoder={ObjectId:str}
    )

# ===================== Add To Wishlist =================
async def addToWishlist(productId:str,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    product = await productCollection.find_one(
        {"_id":ObjectId(productId)}
    )
    if not product:
        raise HTTPException(404,detail="Product not found")
    # ---------------------------------------------------- 
    await customerCollection.update_one(
        {
            "_id":customer["_id"]
        },
        {
            "$addToSet":{
                "wishlist":product["_id"]
            } 
        } 
    )

    return jsonable_encoder(
        {
            "msg":"Add to wishlist"
        },
        custom_encoder={ObjectId:str}
    )

# ====================== My Wishlists ============
async def myWishlists(user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    
    wishlists = await customerCollection.aggregate([
        {
            "$match":{
                "_id":customer["_id"]
            }
        },
        {
            "$unwind":"$wishlist"
        },
        {
            "$lookup":{
                "from":"products",
                "localField":"wishlist",
                "foreignField":"_id",
                "as":"allwishlists"
            }
        },
        {
            "$unwind":"$allwishlists"
        },
        {
            "$project":{
                "_id":0,
                "allwishlists":1
            }
        }
    ]).to_list(length=None)

    if not wishlists:
        raise HTTPException(404,detail="Empty Wishlist")
    
    return jsonable_encoder(
        wishlists,
        custom_encoder={ObjectId:str}
    )

# ============== Remove From Wishlist =============
async def removeWishlist(productId:str,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    product = await customerCollection.find_one(
        {
            "_id":customer["_id"],
            "wishlist":ObjectId(productId)
        }
    )
    if not product:
        raise HTTPException(404,detail="Product not in wishlist")
    await customerCollection.update_one(
        {"_id":customer["_id"]},
        {
            "$pull":{
                "wishlist":ObjectId(productId)
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Removed from wishlist"
        },
        custom_encoder={ObjectId:str}
    )

# ============ Add to Cart ==============
async def addtocart(productId:str,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    product = await productCollection.find_one(
        {"_id":ObjectId(productId)}
    )
    if not product:
        raise HTTPException(404,detail="Product not found")
    # -----------------------------------------------------
    await customerCollection.update_one(
        {"_id":customer["_id"]},
        {
            "$addToSet":{
                "carts":ObjectId(productId)
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Added to Cart Successfully"
        },
        custom_encoder={ObjectId:str}
    )

# =============== My Carts ==========
async def mycarts(user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    
    carts = await customerCollection.aggregate([
        {
            "$match":{
                "_id":customer["_id"]
            }
        },
        {
            "$unwind":"$carts"
        },
        {
            "$lookup":{
                "from":"products",
                "localField":"carts",
                "foreignField":"_id",
                "as":"allcarts"
            }
        },
        {
            "$unwind":"$allcarts"
        },
        {
            "$project":{
                "_id":0,
                "allcarts":1
            }
        }
    ]).to_list(length=None)
    if not carts:
        raise HTTPException(404,detail="Empty Carts")

    return jsonable_encoder(
        carts,
        custom_encoder={ObjectId:str}
    )

# =============== Cart Total ==========
async def cartTotal(user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    
    carts = await customerCollection.aggregate([
        {
            "$match":{
                "_id":customer["_id"]
            }
        },
        {
            "$unwind":"$carts"
        },
        {
            "$lookup":{
                "from":"products",
                "localField":"carts",
                "foreignField":"_id",
                "as":"allcarts"
            }
        },
        {
            "$unwind":"$allcarts"
        },
        {
            "$project":{
                "_id":0,
                "allcarts":1
            }
        }
    ]).to_list(length=None)
    if not carts:
        raise HTTPException(404,detail="Empty Carts")
    totalCartPrice = 0
    for cart in carts:
        totalCartPrice += cart["allcarts"]["discount_price"]
    return jsonable_encoder(
        {"total":totalCartPrice},
        custom_encoder={ObjectId:str}
    )

# =========== Remove From Cart =============
async def removeCart(productId:str,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    product = await customerCollection.find_one(
        {
            "_id":customer["_id"],
            "carts":ObjectId(productId)
        }
    )
    if not product:
        raise HTTPException(404,detail="Product not in Cart")
    
    await customerCollection.update_one(
        {
            "_id":customer["_id"]
        },
        {
            "$pull":{
                "carts":ObjectId(productId)
            }
        }
    )
    return jsonable_encoder(
        {
            "msg":"Cart Removed"
        },
        custom_encoder={ObjectId:str}
    )

# ============= Order By Cart ============
async def placeOrder(user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    cart = customer.get("carts",[])
    if not cart:
        raise HTTPException(400,detail="Empty Cart")
    await customerCollection.update_one(
        {"_id":customer["_id"]},
        {
            "$push":{
                "myorders":{
                    "$each":cart
                }
            },
            "$set":{
                "carts":[]
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Order Placed Successfully"
        },
        custom_encoder={ObjectId:str}
    )