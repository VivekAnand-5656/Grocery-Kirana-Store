from pydantic import BaseModel,EmailStr,FilePath
from typing import Optional
from src.Enums.enum import OrderStatus

class UpdateStatus(BaseModel):
    status:OrderStatus