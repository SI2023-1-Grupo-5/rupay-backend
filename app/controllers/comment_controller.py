from fastapi import APIRouter, Depends, HTTPException, status

from app.database.schemas import Comment as CommentSchemma
from app.database.schemas import CommentCreate as CommentCreateSchema

from app.services import comments_service as CommentService

from sqlalchemy.orm import Session
from app.database.init import SessionLocal

router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_all(db: Session = Depends(get_db)):
    return CommentService.get_all(db)

@router.get("/today")
def get_all_from_today(db: Session = Depends(get_db)):
    return CommentService.get_all_from_today(db)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_comment(user: CommentCreateSchema, db: Session = Depends(get_db)):
    try:
        CommentService.create_comment(db, user)
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= e.args
        )

@router.get("/menu-links")
def get_menu_links(db: Session = Depends(get_db)):
    return CommentService.get_menu_links(db)