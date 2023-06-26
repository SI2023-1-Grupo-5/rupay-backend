
from sqlalchemy.orm import Session

from app.database.models import User as UserModel
from app.database.models import Access as AccessModel
from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserCreate as UserCreateSchema
from app.database.schemas import UserUpdateInfo as UserUpdateInfoSchema

import bcrypt


def create_user(db: Session, user: UserCreateSchema):
    db_user = UserModel(
        college_id=user.college_id,
        name=user.name,
        email=f"{user.college_id}@aluno.unb.br",
        password=get_hashed_password(user.password),
        is_active=False,
        balance=0.00
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(db: Session, college_id: str):
    return db.query(UserModel).filter(UserModel.college_id == college_id).first()

def get_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def update_info(db: Session, user: UserUpdateInfoSchema, college_id: str):
    db_user = get_user(db, college_id)

    db_user.name = user.name
    db_user.password = get_hashed_password(user.password)
    db_user.is_active = user.is_active

    db.commit()


def update_balance(db: Session, value: float, college_id: str):
    user = get_user(db, college_id)
    user.balance += value
    db.commit()


def delete(db: Session, college_id: str):
    db.query(AccessModel).filter(
        AccessModel.user_college_id == college_id).delete()
    db.query(UserModel).filter(UserModel.college_id == college_id).delete()
    db.commit()

def activate(db: Session, college_id: str):
    db.query(UserModel).filter(UserModel.college_id == college_id).update({
        'is_active': True
    })

    db.commit()

def deactivate(db: Session, college_id: str):
    db.query(UserModel).filter(UserModel.college_id == college_id).update({
        'is_active': False
    })

    db.commit()

def get_hashed_password(password: str):
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )  
