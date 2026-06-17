from fastapi import HTTPException, UploadFile
from src.Config.db import sellersCollection ,productCollection
from src.Public.publicSchema import CreateUser,LoginUser
from bson import ObjectId
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from src.Config.cloudinaryConfig import upload_image
from typing import Optional
from cloudinary import uploader
# =========== Update Profile =================
async def updateProfile(
        name:Optional[str] | None,
        email:Optional[str] | None,
        mobile:Optional[str] | None,
        shopname:str,
        address:str,
        city:str,
        state:str,
        pincode:int,
        file:Optional[UploadFile] | None,
        user

):
    if user["role"] != "seller":
        raise HTTPException(401,detail="UnAuthorized user")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not seller:
        raise HTTPException(404,detail="User not found")
    image = upload_image(file.file)

    await sellersCollection.update_one(
        {"_id":seller["_id"]},
        {
            "$set":{
                "name":name,
                "email":email,
                "mobile":mobile,
                "shopname":shopname,
                "address":address,
                "city":city,
                "state":state,
                "pincode":pincode,
                "image_url":image["url"],
                "public_id":image["public_id"]
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Profile Updated"
        },
        custom_encoder={ObjectId:str}
    )

# =================== My Profile ============
async def myprofile(user):
    if user["role"] != "seller":
        raise HTTPException(403,detail="UnAuthorized User")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not seller:
        raise HTTPException(404,detail="User not found")
    
    return jsonable_encoder(
        seller,
        custom_encoder={ObjectId:str}
    )

# ============= Add Product ===========
async def addProduct(
        productname:str,
        detail:str,
        category:str,
        brand:str,
        price:float,
        discount:int, 
        unit:str,
        isAvailable:bool,
        file,
        user
):
    if user["role"] != "seller":
        raise HTTPException(403,detail="UnAuthorized User")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not seller:
        raise HTTPException(404,detail="User not found")
    image = upload_image(file.file)
    discountPercent = price * (discount/100)
    discPrice = price - discountPercent
    newproduct = {
        "productname":productname,
        "detail":detail,
        "category":category,
        "brand":brand,
        "price":price,
        "discount":discount, 
        "discount_price":discPrice,
        "unit":unit,
        "isAvailable":isAvailable,
        "image_url":image["url"],
        "createdAt":datetime.utcnow(),
        "public_id":image["public_id"],
        "seller_id":seller["_id"]
    }
    result = await productCollection.insert_one(newproduct)
    # ------- Add in Seller id -----
    await sellersCollection.update_one(
        {"_id":seller["_id"]},
        {
            "$push":{
                "myproducts":result.inserted_id
            }
        }
    )
    product = await productCollection.find_one(
        {"_id":result.inserted_id}
    )

    return jsonable_encoder(
        {
            "msg":"Product Added Successfully",
            "product":product
        },
        custom_encoder={ObjectId:str}
    )

# ============ My Products =========
async def my_products(user):
    if user["role"] != "seller":
        raise HTTPException(403,detail="UnAuthorized User")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not seller:
        raise HTTPException(404,detail="User not found")
    
    products = await productCollection.find(
        {
            "_id":{
                "$in": seller["myproducts"]
            }
        }
    ).to_list(length=None)

    if not products:
        raise HTTPException(404,detail="Products not found")

    return jsonable_encoder(
        products,
        custom_encoder={ObjectId:str}
    )

# ====================== Update Products ===================
async def updateProduct(
        productId:str,
        productname:str,
        detail:str,
        category:str,
        brand:str,
        price:float,
        discount:int, 
        unit:str,
        isAvailable:bool,
        file,
        user
):
    if user["role"] != "seller":
        raise HTTPException(403,detail="UnAuthorized User")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    if not seller:
        raise HTTPException(404,detail="Seller not available")
    product = await productCollection.find_one(
        {"_id":ObjectId(productId)}
    )
    if not product:
        raise HTTPException(404,detail="Product not found")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    findMyProduct = await sellersCollection.find_one(
        {
            "_id": seller["_id"],
            "myproducts": product["_id"]
        }
    )

    if not findMyProduct:
        raise HTTPException(
            403,
            detail="You can not delete this product"
        )
    
    image = upload_image(file.file)
    discountPercent = price * (discount/100)
    discPrice = price - discountPercent
    await productCollection.update_one(
        {"_id":product["_id"]},
        {
            "$set":{
                "productname":productname,
                "detail":detail,
                "category":category,
                "brand":brand,
                "price":price,
                "discount":discount, 
                "discount_price":discPrice,
                "unit":unit,
                "isAvailable":isAvailable,
                "image_url":image["url"],
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Product Updated Successfully"
        },
        custom_encoder={ObjectId:str}
    )

# =============== Update IsAvailable ================
async def updateIsAvailable(productId:str,isAvailable:bool,user):
    if user["role"] != "seller":
        raise HTTPException(403,detail="UnAuthorized User")
    product = await productCollection.find_one(
        {"_id":ObjectId(productId)}
    )
    if not product:
        raise HTTPException(404,detail="Product not found")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    findMyProduct = await sellersCollection.find_one(
        {
            "_id": seller["_id"],
            "myproducts": product["_id"]
        }
    )

    if not findMyProduct:
        raise HTTPException(
            403,
            detail="You can not delete this product"
        )
    
    await productCollection.update_one(
        {"_id":product["_id"]},
        {
            "$set":{
                "isAvailable":isAvailable
            }
        }
    )
    return jsonable_encoder(
        {
            "msg":"Set Product Available"
        },
        custom_encoder={ObjectId:str}
    )

 
# ============ Delete Product ============
async def deleteProduct(productId:str,user):
    if user["role"] != "seller":
        raise HTTPException(403,detail="UnAuthorized User")
    product = await productCollection.find_one(
        {"_id":ObjectId(productId)}
    )
    if not product:
        raise HTTPException(404,detail="Product not found")
    seller = await sellersCollection.find_one(
        {"_id":ObjectId(user["_id"])}
    )
    findMyProduct = await sellersCollection.find_one(
        {
            "_id": seller["_id"],
            "myproducts": product["_id"]
        }
    )

    if not findMyProduct:
        raise HTTPException(
            403,
            detail="You can not delete this product"
        )
    
    await productCollection.delete_one({"_id":product["_id"]})
    await sellersCollection.update_one(
        {"_id":seller["_id"]},
        {
            "$pull":{
                "myproducts":product["_id"]
            }
        }
    )

    return jsonable_encoder(
        {
            "msg":"Product Deleted"
        },
        custom_encoder={ObjectId:str}
    )
