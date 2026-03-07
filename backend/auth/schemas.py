from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "Employee"

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
