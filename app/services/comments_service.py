
from sqlalchemy.orm import Session

from app.database.models import Comment
from app.database.schemas import CommentCreate as CommentCreateSchema


def create_comment(db: Session, comment: CommentCreateSchema):
    db_comment = Comment(**comment.dict())

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)


def get_comments(db: Session, college_id: str):
    return db.query(Comment).filter(Comment.user_college_id == college_id).all()
