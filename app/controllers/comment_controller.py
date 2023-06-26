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

@router.get("/{college_id}", response_model=list[CommentSchemma])
def get_comment_by_user(college_id: str, db:Session = Depends(get_db)):  
    try:
        return CommentService.get_comments(db, college_id)
    except:
        raise HTTPException(status_code=404, detail='User not found')
    

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


# TODO: Exceptions should be in services, not in controllers (?)
# TODO: Add proper response type/model for each route
# TODO: Add proper response for each route, i.e REST patterns for HTTP methods