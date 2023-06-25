
from sqlalchemy.orm import Session
from app.database.models import Access as AccessModel

from random import randint

def get_id_by_college_id(db: Session, college_id: str):
    access = db.query(AccessModel).filter(AccessModel.user_college_id == college_id).first()
    
    return access.id

def create(db: Session, college_id: str):
    access_object = AccessModel(
        user_college_id=college_id,
        code=generate_code()
    )

    db.add(access_object)
    db.commit()
    db.refresh(access_object)

    return access_object

def get_code(db: Session, college_id: str):
    return db.query(AccessModel).filter(AccessModel.user_college_id == college_id).first()

def generate_code():
    return f"{randint(10000, 99999)}"

def delete(db: Session, college_id: str):
    db.query(AccessModel).filter(AccessModel.user_college_id == college_id).delete()
    