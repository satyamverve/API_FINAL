# app/dto/users_schema.py

from pydantic import BaseModel, EmailStr  ## used to valiadte the email format
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    
    
class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime
    
    class config:
        orm_mode=True

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str
    class config:
        orm_mode=True

class UserUpdateMe(BaseModel):
    username: Optional[str]
    class config:
        orm_mode=True
