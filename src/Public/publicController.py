from fastapi import HTTPException
from src.Config.db import sellersCollection,productCollection,customerCollection
from src.Auths.auth import hasingPassword,verifyPassword,createToekn
from src.Public.publicSchema import CreateUser,LoginUser
from bson import ObjectId
from datetime import datetime
from fastapi.encoders import jsonable_encoder


# =============== Create User ===============
async def createUser(data):
    userExist = await sellersCollection.find_one(
        {"email":data.email}
    )
    if userExist:
        raise HTTPException(401,detail="User already signedup")
    
    hashpassword = hasingPassword(data.password)

    createuser = {
        "name":data.name,
        "email":data.email,
        "mobile":data.mobile,
        "password":hashpassword,
        "role":data.role
    }
    if data.role =="seller":
        await sellersCollection.insert_one(createuser)
    else:
        await customerCollection.insert_one(createuser)
    
    return {
        "msg":"Account Created Successfully"
    }

# ============= Login ================
async def loginUser(data):
    # ----------- Seller ----------
    seller = await sellersCollection.find_one(
        {"email":data.email}
    )
     
    # --------Customer ----------
    customer = await customerCollection.find_one(
        {"email":data.email}
    )
    if not customer and not seller:
        raise HTTPException(404,detail="User not Exist  !")
    
    if seller:
        isvalidPassword = verifyPassword(data.password,seller["password"])
        if not isvalidPassword:
            raise HTTPException(401,detail="Invalid Password")
        token = createToekn({
            "_id":str(seller["_id"]),
            "email":seller["email"],
            "role":seller["role"]
        })
    elif customer:
        validpassword  = verifyPassword(data.password,customer["password"])
        if not validpassword:
            raise HTTPException(401,detail="Invalid password")
        token = createToekn(
            {
                "_id":str(customer["_id"]),
                "email":customer["email"],
                "role":customer["role"]
            }
        )
    return jsonable_encoder(
        {
            "msg":"Login Successfully",
            "token":token
        },
        custom_encoder={ObjectId:str}
    )

# ============= All Products ===========
async def all_products():
    products = await productCollection.find(
        {},
        {
            "seller_id":0,
            "public_id":0, 
        }
    ).to_list(length=None)

    if not products:
        raise HTTPException(404,detail="Products not found")
    
    return jsonable_encoder(
        products,
        custom_encoder={ObjectId:str}
    )

# ========= Search Products ==========
async def serchProducts(search:str):
    products = await productCollection.find(
        {
            "productname":{
                "$regex":search,
                "$options":"i"
            }
        }
    ).to_list(length=None)
    if not products:
        raise HTTPException(404,detail="Product not found")
    return jsonable_encoder(
        products,
        custom_encoder={ObjectId:str}
    )
# =============== Filter Products =============
async def filterProducts(search:str):
    products = await productCollection.find(
        {
            "$text":{
                "$search":search
            }
        }
    ).to_list(length=None)

    if not products:
        raise HTTPException(404,detail="Empty Products")
    
    return jsonable_encoder(
        products,
        custom_encoder={ObjectId:str}
    )

# =============== Filter by Price ==========
async def filterByPrice(gtPrice:int,ltPrice:int):
    products = await productCollection.find(
        {
            "price":{
                "$gte":gtPrice,
                "$lte":ltPrice,
            }
        }
    ).sort({"price":1}).to_list(length=None)

    if not products:
        raise HTTPException(404,detail="Empty Products")
    
    return jsonable_encoder(
        products,
        custom_encoder={ObjectId:str}
    )