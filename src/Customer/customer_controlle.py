from fastapi import HTTPException
from src.Config.db import productCollection,sellersCollection,customerCollection,ordersCollection, couponCollection
from src.Customer.customer_schema import AddressModel
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
    order = {
        "customer_id": customer["_id"],
        "seller_id": ObjectId(product["seller_id"]),
        "items": [{
            "product_id": product["_id"],
            "productname": product["productname"],
            "discount_price": product["discount_price"],
            "quantity": quantity,
            "status": "Pending"
        }],
        "totalAmount": totalprice,
        "status": "Pending"
    }
    result = await ordersCollection.insert_one(order)
 

    # Add order id into customer myOrders
    await customerCollection.update_one(
        {"_id": customer["_id"]},
        {
            "$push": {
                "myorders": result.inserted_id
            }
        }
    )

    # Add order id into seller myOrders
    await sellersCollection.update_one(
        {"_id":ObjectId(product["seller_id"])},
        {
            "$push": {
                "myorders": result.inserted_id
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
    
    orders = await ordersCollection.find(
        {
            "customer_id":customer["_id"]
        }
    ).to_list(length=None)
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
                "carts":{
                    "_id":ObjectId(),
                    "product_id":ObjectId(productId),
                    "quantity":1
                }
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
                "localField":"carts.product_id",
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
                "allcarts":1 ,
                "_id":"$carts._id",
                "quantity":"$carts.quantity"
            }
        }
    ]).to_list(length=None)
    if not carts:
        raise HTTPException(404,detail="Empty Carts")

    return jsonable_encoder(
        carts,
        custom_encoder={ObjectId:str}
    )

# ================ Update Cart Quantity By Cart id =============
async def increaseQuantity(productId:str,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")

    await customerCollection.update_one(
        {
            "_id":ObjectId(user["_id"]),
            "carts.product_id":ObjectId(productId)
        },
        {
            "$inc":{
                "carts.$.quantity":1
            }
        }
    )       
    return jsonable_encoder(
        {
            "msg":"Increase Cart Quantity"
        },
        custom_encoder={ObjectId:str}
    )
# ================ Update Minus Cart Quantity By Cart id =============
async def decreaseQuantity(productId:str,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="You are not authorized")
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")

    await customerCollection.update_one(
        {
            "_id":ObjectId(user["_id"]),
            "carts.product_id":ObjectId(productId)
        },
        {
            "$inc":{
                "carts.$.quantity":-1
            }
        }
    )
    await customerCollection.update_one(
        {
            "_id": ObjectId(user["_id"])
        },
        {
            "$pull": {
                "carts": {
                    "product_id": ObjectId(productId),
                    "quantity": 0
                }
            }
        }
    )
    return jsonable_encoder(
        {
            "msg":"Decrease Cart Quantity"
        },
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

# # ============= Order By Cart ============
 
async def placeOrder(code:str,user):
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
    
    seller_orders={}

    total_cart_price = 0
    for item in customer["carts"]:
        product = await productCollection.find_one(
            {
                "_id":ObjectId(item["product_id"])
            }
        )
        if not product:
            continue
        total_cart_price += (product["discount_price"] * item["quantity"])
    
        seller_id = ObjectId(product["seller_id"])

        if seller_id not in seller_orders:
            seller_orders[seller_id] = []
        seller_orders[seller_id].append({
            "product_id": product["_id"],
            "productname": product["productname"],
            "discount_price": product["discount_price"],
            "quantity": item["quantity"],
            "status": "Pending"
        })
    # ----------- Apply Coupon ------------- yaha kuch gadbad hai bhai 
    final_price = 0
    discount = 0
    if code:
        coupon = await couponCollection.find_one(
            {
                "code":code,
                "is_Active":True
            }
        )
        if not coupon:
            raise HTTPException(400,detail="Invalid Coupon")
        
        if coupon["expiry_time"] < datetime.utcnow():
            raise HTTPException(400,detail="Coupon Expired")
        
        if total_cart_price < coupon["minimum_value"]:
            raise HTTPException(400,detail="Minimum order ammount not reached")
        
        if coupon["type_discount"] == "percentage":
            discount = (total_cart_price * coupon["discount"]) / 100
        else:
            discount = coupon["discount"]
    final_price = total_cart_price - discount

    create_orders = []
    for seller_id, items in seller_orders.items(): 
        
        order = {
            "customer_id": customer["_id"],
            "seller_id": ObjectId(seller_id),
            "items": items,
            "totalAmount": final_price,
            "status": "Pending",
            "coupon_code":code
        }

        result = await ordersCollection.insert_one(order)

        create_orders.append(str(result.inserted_id))

        # Add order id into customer myOrders
        await customerCollection.update_one(
            {"_id": customer["_id"]},
            {
                "$push": {
                    "myorders": result.inserted_id
                }
            }
        )

        # Add order id into seller myOrders
        await sellersCollection.update_one(
            {"_id": ObjectId(seller_id)},
            {
                "$push": {
                    "myorders": result.inserted_id
                }
            }
        )

    # Clear cart after successful order
    await customerCollection.update_one(
        {"_id": customer["_id"]},
        {
            "$set": {
                "carts": []
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Order Placed Successfully",
            "orders":create_orders
        },
        custom_encoder={ObjectId:str}
    )

# =========  Rating ===========
async def rate_product(rate:int,productId:str,user):
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
    
    if rate > 5:
        raise HTTPException(401,detail="Please select under 5")
    
    await productCollection.update_one(
        {"_id":product["_id"]},
        {
            "$set":{
                "rating":rate
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Rating successfully"
        },
        custom_encoder={ObjectId:str}
    )
    
# ========== Get Coupons ========
async def get_coupons(user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="UnAuthorized User") 
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not customer:
        raise HTTPException(404,detail="Customer not found")
    
    my_coupons = await couponCollection.find().to_list(length=None)

    if not my_coupons:
        raise HTTPException(404,detail="Empty Coupons")
    
    return jsonable_encoder(
        my_coupons,
        custom_encoder={ObjectId:str}
    )

# ========= Apply Coupons =====
async def apply_coupon(code:str,user):

    if user["role"] != "customer":
        raise HTTPException(403,detail="UnAuthorized User") 
    
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )

    if not customer:
        raise HTTPException(404,detail="Customer not found")
    
    carts = customer.get("carts",[])
    if not carts:
        raise HTTPException(400,detail="Empty Cart")
    
    total_cart_price = 0
    for cart in customer["carts"]:
        product = await productCollection.find_one(
            {
                "_id":ObjectId(cart["product_id"])
            }
        ) 
        if not product:
            continue
        total_cart_price += (product["discount_price"] * cart["quantity"])
         
    
    final_price = 0
    discount = 0
    if code:
        coupon = await couponCollection.find_one(
            {
                "code":code,
                "is_Active":True
            }
        )
        if not coupon:
            raise HTTPException(400,detail="Invalid Coupon")
        
        if coupon["expiry_time"] < datetime.utcnow():
            raise HTTPException(400,detail="Coupon Expired")
        
        if total_cart_price < coupon["minimum_value"]:
            raise HTTPException(400,detail="Minimum order ammount not reached")
        
        if coupon["type_discount"] == "percentage":
            discount = (total_cart_price * coupon["discount"]) / 100
        else:
            discount = coupon["discount"]
    
    final_price = total_cart_price - discount

    return jsonable_encoder(
        {
            "total_cart": total_cart_price,
            "discount": discount,
            "final_price": final_price,
            "coupon": coupon["code"]
        },
        custom_encoder={ObjectId:str}
    )
 
#  ============ Add Address ===========
async def add_address(data:AddressModel,user):
    if user["role"] != "customer":
        raise HTTPException(403,detail="UnAuthorized User") 
    
    customer = await customerCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )

    if not customer:
        raise HTTPException(404,detail="Customer not found")

    # ---------- Add address ------
    address = {
        "house_no":data.house_no,
        "area":data.area,
        "landmark":data.landmark,
        "city":data.city,
        "state":data.state,
        "pincode":data.pincode
    }

    await customerCollection.update_one(
        {"_id":customer["_id"]},
        {
            "$push":{
                "addresses":address
            }
        }
    )

    return  jsonable_encoder(
        {
            "msg":"Address Updated"
        },
        custom_encoder={ObjectId:str}
    )