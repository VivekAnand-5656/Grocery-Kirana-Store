from pydantic import BaseModel,EmailStr,FilePath
from typing import Optional
from src.Enums.enum import OrderStatus
from datetime import datetime

class UpdateStatus(BaseModel):
    status:OrderStatus

# ======= Coupon Schema  ==========
class CouponModel(BaseModel):
    code:str
    type_discount:str
    discount:float
    minimum_value:float = 0
    expiry_time : datetime
    is_Active:bool = True
    created_at:datetime