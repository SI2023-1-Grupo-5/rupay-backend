
from sqlalchemy.orm import Session

from app.database.models import User as UserModel
from app.database.models import Access as AccessModel
from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserCreate as UserCreateSchema
from app.database.schemas import UserUpdateInfo as UserUpdateInfoSchema

import bcrypt


def create(db: Session, user: UserCreateSchema):
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    )

    db_user = UserModel(
        college_id=user.college_id,
        name=user.name,
        email=f"{user.college_id}@aluno.unb.br",
        password=hashed_password,
        is_active=False,
        balance=0.00
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get(db: Session, college_id: str):
    user = db.query(UserModel).filter(
        UserModel.college_id == college_id).first()
    if not user:
        raise Exception
    return user


def get_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def update_info(db: Session, user: UserUpdateInfoSchema, college_id: str):
    # TODO: hash password before saving

    db_user = get(db, college_id)

    db_user.name = user.name
    db_user.password = user.password
    db_user.is_active = user.is_active

    db.commit()


def update_balance(db: Session, value: float, college_id: str):

    user = get(db, college_id)
    user.balance += value
    db.commit()


def delete(db: Session, college_id: str):
    db.query(AccessModel).filter(
        AccessModel.user_college_id == college_id).delete()
    db.query(UserModel).filter(UserModel.college_id == college_id).delete()
    db.commit()


def auth_user(db: Session, user: UserBaseSchema):
    
    db_user = get(db=db, college_id=user.college_id)

    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise Exception("Login information is incorrect")

    return db_user
