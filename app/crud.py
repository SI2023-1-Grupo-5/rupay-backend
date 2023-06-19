from sqlalchemy.orm import Session
from .import models, schemas
import bcrypt


def get_user(db:Session, user_collegeId: str):
    return db.query(models.User).filter(models.User.collegeId == user_collegeId).first()

# def get_users(db:Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offseat(skip)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db:Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(collegeId=user.collegeId,
                          name = user.name,
                          email = user.email,
                          password = hashed_password,
                          balance = 0.0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


