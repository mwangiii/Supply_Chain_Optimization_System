from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    firstname: str = Field(..., min_length=1, max_length=50)
    lastname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    userid: str
    
    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    oldPassword: str
    newPassword: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userid: Optional[str] = None