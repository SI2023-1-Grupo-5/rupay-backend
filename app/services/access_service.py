
from sqlalchemy.orm import Session
from app.database.models import Access as AccessModel

from random import randint

def get(db: Session, college_id: str, code: str):
    return db.query(AccessModel).filter(
        AccessModel.user_college_id == college_id, 
        AccessModel.code == code
    ).first()

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

    return access_object.code

def get_code(db: Session, college_id: str):
    return db.query(AccessModel).filter(AccessModel.user_college_id == college_id).first()

def update_code(db: Session, college_id: str):
    new_code = generate_code()

    db.query(AccessModel).filter(AccessModel.user_college_id == college_id).update({
        'code': new_code
    })

    db.commit()

    return new_code 

def delete(db: Session, college_id: str):
    db.query(AccessModel).filter(AccessModel.user_college_id == college_id).delete()
    db.commit()

def generate_code():
    return f"{randint(10000, 99999)}"
