from fastapi import APIRouter, Depends, HTTPException, status

from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserCreate as UserCreateSchema
from app.database.schemas import UserUpdate as UserUpdateSchema

from app.services import user_service as UserService
from app.services import access_service as AccessService
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

    existent_user = UserService.get(db, college_id) 

    # If user doesn't exists, create it and generate access code
    if not existent_user:
        UserService.create(db, user)
        code = AccessService.create(db, college_id)

    # If user exists but it's not active yet, update it and generate new access code
    elif not existent_user.is_active:
        UserService.update(db, UserUpdateSchema(
            name=user.name, 
            password=user.password, 
            balance=0.00, 
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
def login(user: UserBaseSchema, db: Session = Depends(get_db)):
    try:
        UserService.auth_user(db, user=user)
        return "Usuário logado!"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login error"
        )

@router.post("/request-access")
def request_access(college_id: str, access_code: str, db: Session = Depends(get_db)):
    if not AccessService.get(db, college_id, access_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access code is not valid!"
        )
    
    UserService.activate(db, college_id)

    return "Usuário autenticado!"