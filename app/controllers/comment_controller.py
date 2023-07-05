from fastapi import APIRouter, Depends, HTTPException, status

from app.database.schemas import Comment as CommentSchemma
from app.database.schemas import CommentCreate as CommentCreateSchema

from app.services import comments_service as CommentService

from sqlalchemy.orm import Session
from app.database.init import SessionLocal

CAMPUS = ['planaltina', 'darcy', 'ceilandia', 'gama']

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

@router.get("/today/{campus}")
def get_all_from_today(campus: str, db: Session = Depends(get_db)):
    if campus not in CAMPUS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campus inválido!")

    return CommentService.get_all_from_today(db, campus)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreateSchema, db: Session = Depends(get_db)):
    if comment.campus not in CAMPUS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campus inválido!")
    
    try:
        CommentService.create_comment(db, comment)
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= e.args
        )

@router.get("/menu-links/{id}")
def get_menu_links(id: int):
    return CommentService.get_menu_links(id)

@router.get("/menu-links")
def get_menu_links():
    return CommentService.get_menu_links()