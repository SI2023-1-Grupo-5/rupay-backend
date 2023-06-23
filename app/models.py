from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, SmallInteger, Date
from sqlalchemy.orm import relationship

from .database import Base
import bcrypt


class User(Base):
    __tablename__ = 'users'
    collegeId = Column(String(9), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    balance = Column(Float)

    # def hash_password(password: str)-> str:
    #     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    #     return hashed_password.decode('utf-8')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    rating = Column(SmallInteger)
    createdAt = Column(Date)

    userCollegeId = Column(String(9), ForeignKey("users.collegeId"))
