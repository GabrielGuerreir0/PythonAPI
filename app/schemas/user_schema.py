from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from fastapi import UploadFile
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=50)

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    profile_image: Optional[UploadFile] = None

    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    profile_image: Optional[str] = None  # Suporta Base64
    

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
