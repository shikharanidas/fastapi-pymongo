from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name:str
    email:str

class UserCreate(UserBase):
    password:str

class User(UserBase):
    id:str

class UserUpdate(BaseModel):
    name:Optional[str]
    email:Optional[str]
