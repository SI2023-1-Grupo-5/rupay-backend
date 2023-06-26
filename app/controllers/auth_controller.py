from fastapi import APIRouter, Depends, HTTPException, status, Response

import bcrypt

from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserLogin as UserLoginSchema
from app.database.schemas import UserCreate as UserCreateSchema
from app.database.schemas import UserUpdateInfo as UserUpdateInfoSchema

from app.services import user_service as UserService
from app.services import access_service as AccessService
from app.services import auth_service as AuthService
from app.services.email_service import EmailService

from sqlalchemy.orm import Session
from app.database.init import SessionLocal

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreateSchema, db:Session = Depends(get_db)):
    college_id = user.college_id
    email = f"{college_id}@aluno.unb.br"
    code = 00000

    existent_user = UserService.get_user(db, college_id) 

    # If user doesn't exists, create it and generate access code
    if not existent_user:
        UserService.create_user(db, user)
        code = AccessService.create(db, college_id)

    # If user exists but it's not active yet, update it and generate new access code
    elif not existent_user.is_active:
        UserService.update_info(db, UserUpdateInfoSchema(
            name=user.name, 
            password=user.password,
            is_active=False
        ), college_id)
        code = AccessService.update_code(db, college_id)

    # If user exists and it is active, raise an exception
    else: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already registered!"
        )
    
    # Send email to user
    email_service = EmailService()
    email_service.send_email(email, user.name, code)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    expected_user = UserService.get_user(db, user.college_id)
    
    if not expected_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    # user_password = UserService.get_hashed_password(user.password)

    # if expected_user.password != user_password:
    if not bcrypt.checkpw(user.password.encode('utf-8'), expected_user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password"
        )

    token = AuthService.create_token({ "college_id": user.college_id })
    
    response.set_cookie(key="session", value=token)

    return "Usuário autenticado!"

@router.post("/request-access")
def request_access(college_id: str, access_code: str, response: Response, db: Session = Depends(get_db)):
    if not AccessService.get(db, college_id, access_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access code is not valid!"
        )
    
    UserService.activate(db, college_id)

    token = AuthService.create_token({ "college_id": college_id })
    
    response.set_cookie(key="session", value=token)

    return "Usuário autenticado!"