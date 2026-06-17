from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name:str
    email:EmailStr
    mobile:str
    password:str
    role:str

class LoginUser(BaseModel):
    email:EmailStr
    password:str 