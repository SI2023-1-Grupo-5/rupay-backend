from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.database.schemas import User as UserSchema
from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserCreate as UserCreateSchema
from app.database.schemas import UserUpdateInfo as UserUpdateInfoSchema

from app.services import user_service as UserService

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

@router.get("/{college_id}", status_code=status.HTTP_200_OK)
def get(college_id: str, db:Session = Depends(get_db)):
    db_user = UserService.get_user(db, college_id)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found!"
        )

    return JSONResponse(
        content={"name": db_user.name, "email": db_user.email, "balance": str(db_user.balance) }, 
        status_code=200
    )
    
@router.post("", status_code=status.HTTP_201_CREATED)
def create(user: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        created_user = UserService.create_user(db, user)
        return JSONResponse(content=created_user, status_code=201)
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with the provided college id already registered"
        )

@router.put("/{college_id}", status_code=status.HTTP_200_OK)
def update(college_id: str, user: UserUpdateInfoSchema, db: Session = Depends(get_db)):
    if not UserService.get_user(db, college_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    try:
        updated_user = UserService.update(db, user, college_id)
        return JSONResponse(content=updated_user, status_code=200)
    
    except Exception as e:
        # Log the error, so we can understand exactly what happened
        print(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Student couldn't be deleted!"
        )

@router.delete("/{college_id}", status_code=status.HTTP_200_OK)
def delete(college_id: str, db: Session = Depends(get_db)):
    if not UserService.get_user(db, college_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    try:
        UserService.delete(db, college_id)
        return JSONResponse(content="Usuário deletado com sucesso!", status_code=200)
    
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