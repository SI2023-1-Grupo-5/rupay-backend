from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas


from .database import SessionLocal, engine
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/home")
def root():
    return {"message":"Hello, World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/",response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_collegeId= user.collegeId)
    if db_user:
        raise HTTPException(status_code= 400, detail= 'Student already registered')
    return crud.create_user(db=db, user = user)

@app.get("/users/{user_collegeId}",response_model=schemas.User)
def read_user(user_collegeId: str, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_collegeId= user_collegeId)
    if db_user:
        raise HTTPException(status_code=404, detail='user not found')
    return db_user