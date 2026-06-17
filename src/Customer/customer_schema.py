from pydantic import BaseModel,EmailStr
from typing import Optional

class UpdateProfile(BaseModel):
    name:str
    email:EmailStr
    mobile:str
    address:str
    city:str
    state:str
    pincode:str
    