from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, SmallInteger, DECIMAL, VARCHAR, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .init import Base


class User(Base):
    __tablename__ = 'users'
    college_id = Column(VARCHAR(9), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(128), nullable=False)
    is_active = Column(Boolean, nullable=False, default=0)
    balance = Column(DECIMAL(5, 2), nullable=False, default=0.00)
    comments = relationship('Comment', backref='users')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    rating = Column(SmallInteger, nullable=False, default=0)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    user_college_id = Column(VARCHAR(9), ForeignKey("users.college_id"))

class Access(Base):
    __tablename__ = 'access'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(5), nullable=False)
    user_college_id = Column(VARCHAR(9), ForeignKey("users.college_id"))
