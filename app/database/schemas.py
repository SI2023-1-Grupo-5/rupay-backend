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

class UserUpdate(BaseModel):
    name: str
    password: str
    balance: float
    is_active: bool

class User(UserBase):
    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str
    rating: str
    createdAt: str

class CommentCreate(CommentBase):
    userCollegeId: str

class Comment(CommentBase):
    id: int
    user: User

    class Config:
        orm_mode = True

class CardRecharge(BaseModel):
    number: str
    name: str
    security_code: str
    date: date
    valor: int
