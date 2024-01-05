#app/auth/auth_schema.py

from typing import Optional
from pydantic import BaseModel, EmailStr
class UserAuth(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id : Optional[str] = None
    password: str | None= None
    email: Optional[EmailStr] = None  #added to use email as username

