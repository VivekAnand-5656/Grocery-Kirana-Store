from pydantic import BaseModel,EmailStr, Field
from typing import Optional

class UpdateProfile(BaseModel):
    name:str
    email:EmailStr
    mobile:str
    address:str
    city:str
    state:str
    pincode:str
    
class AddressModel(BaseModel):
    house_no: str
    area: str
    landmark: Optional[str] = None

    city: str
    state: str
    pincode: str = Field(..., min_length=6, max_length=6)
 