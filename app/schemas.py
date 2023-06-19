from pydantic import BaseModel


class UserBase(BaseModel):
    collegeId: str
    name: str
    email: str
    balance: float

class UserCreate(UserBase):
    password: str

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
