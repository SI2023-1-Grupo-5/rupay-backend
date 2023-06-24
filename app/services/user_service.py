
from sqlalchemy.orm import Session

from app.database.models import User as UserModel
from app.database.models import Access as AccessModel
from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserCreate as UserCreateSchema
from app.database.schemas import UserUpdate as UserUpdateSchema

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
    return db.query(UserModel).filter(UserModel.college_id == college_id).first()

def get_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def update(db: Session, user: UserUpdateSchema, college_id: str):
    # TODO: hash password before saving

    db.query(UserModel).filter(UserModel.college_id == college_id).update({
        'name': user.name,
        'password': user.password,
        'is_active': user.is_active,
        'balance': user.balance
    })

    db.commit()

def delete(db: Session, college_id: str):
    db.query(AccessModel).filter(AccessModel.user_college_id == college_id).delete()
    db.query(UserModel).filter(UserModel.college_id == college_id).delete()
    db.commit()

def auth_user(db: Session, user: UserBaseSchema):
    query_user = get(db=db, college_id=user.college_id)
    
    if not query_user or not bcrypt.checkpw(user.password.encode('utf-8'), query_user.password.encode('utf-8')):
        raise Exception
    
    return query_user