from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas
from app.email_service import EmailService


from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        crud.create_user(db, user= user)
        return {"message": "success"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Student with the provided id already registered'
            )


@app.post("/users/login", status_code=status.HTTP_200_OK)
def read_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    try:
        crud.auth_user(db, user=user)
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login error"
            )

@app.get("/users/{user_collegeId}",response_model=schemas.User)
def read_user(user_collegeId: str, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_collegeId= user_collegeId)
    if db_user:
        raise HTTPException(status_code=404, detail='user not found')
    return db_user

@app.post("/email-service/{email}")
def send_email(email: str):
    email_service = EmailService()
    email_service.send_email(email)
