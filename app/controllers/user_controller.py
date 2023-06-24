from fastapi import APIRouter, Depends, HTTPException, status

from app.database.schemas import User as UserSchema
from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserCreate as UserCreateSchema
from app.database.schemas import UserUpdate as UserUpdateSchema

from app.services import user_service

from sqlalchemy.orm import Session
from app.database.init import SessionLocal

router = APIRouter(
    prefix='/user',
    tags=['User']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_college_id}", response_model=UserSchema)
def get(college_id: str, db:Session = Depends(get_db)):
    db_user = user_service.get(db, college_id)
    
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    
    return db_user

@router.post("", status_code=status.HTTP_201_CREATED)
def create(user: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        user_service.create(db, user)
        return {"message": "success"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Student with the provided id already registered'
        )
    
@router.put("/{college_id}")
def update(college_id: str, user: UserUpdateSchema, db: Session = Depends(get_db)):
    # TODO: Check if user exists before updating
    
    try:
        user_service.update(db, user, college_id)
        return {"message": "success"}
    except Exception as e:
        # Log the error, so we can understand exactly what happened
        print(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Student couldn't be deleted!"
        )

@router.delete("/{college_id}")
def delete(college_id: str, db: Session = Depends(get_db)):
    # TODO: Check if user exists before deleting

    try:
        user_service.delete(db, college_id)
        return {"message": "success"}
    except Exception as e:
        # Log the error, so we can understand exactly what happened
        print(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Student couldn't be deleted!"
        )


# TODO: Exceptions should be in services, not in controllers (?)
# TODO: Add proper response type/model for each route
# TODO: Add proper response for each route, i.e REST patterns for HTTP methods