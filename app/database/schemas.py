from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    college_id: str
    name: str
    email: str
    password: str
    is_active: bool
    balance: float

class UserLogin(BaseModel):
    college_id: str
    password: str

class UserCreate(BaseModel):
    college_id: str
    name: str
    password: str

class UserUpdateInfo(BaseModel):
    name: str
    password: str
    is_active: bool

class User(UserBase):
    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str
    rating: int

class CommentCreate(CommentBase):
    user_college_id: str

class Comment(CommentBase):
    id: int
    user_college_id: str
    created_at: date

    class Config:
        orm_mode = True

class Comment(BaseModel):
    id: int
    user_college_id: str
    content: str
    created_at: date
    rating: int

class CardRecharge(BaseModel):
    number: str
    name: str
    security_code: str
    date: date
    value: int
