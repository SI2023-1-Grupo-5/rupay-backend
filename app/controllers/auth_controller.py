from fastapi import APIRouter, Depends, HTTPException, status

from app.database.schemas import UserBase as UserBaseSchema
from app.database.schemas import UserCreate as UserCreateSchema

from app.services import user_service

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
    # Verifica se o usuário já existe e está inativo (código ainda não utilizado)
    college_id = user.college_id
    name = user.name
    password = user.password

    _user = user_service.get_user(db, college_id)

    # Caso exista, gere um novo código e atualize.

    # Criar um usuário com is_active = false
    # createdUser = crud.create_user(db, user)
    print(_user.password)

    # Gerar um código aleatório de acesso
    # Cadastrar o código na tabela
    # accessCode = crud.create_access_code(db, college_id)
    _accessCode = user_service.get_access_code(db, college_id)
    print(_accessCode.code)

    print(f">>>>>>>> DELETANDO CÓDIGO DE ACESSO DO USUÁRIO.....")
    user_service.delete_access_code(db, college_id)
    print(f">>>>>>>> CÓDIGO DE ACESSO DO USUÁRIO DELETADO!")

    _accessCode = user_service.get_access_code(db, college_id)
    print(_accessCode.code)
    # Envia o email para o usuário
    # email_service = EmailService()
    # email_service.send_email(f"{college_id}@aluno.unb.br")

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserBaseSchema, db: Session = Depends(get_db)):
    try:
        user_service.auth_user(db, user=user)
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login error"
        )

@router.post("/request-access")
def request_access():
    # Verifica código de acesso
    #     Caso não bata com o armazenado, lance um erro.
    # Seta o is_active do usuário para true
    pass