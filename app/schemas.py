from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    collegeId: str
    password: str


class UserCreate(UserBase):
    name: str
    email: str
    balance: float


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
