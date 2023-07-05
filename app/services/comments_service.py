from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import Comment as CommentModel
from app.database.schemas import CommentCreate as CommentCreateSchema
from app.database.schemas import Comment as CommentSchema

from app.services import user_service as UserService

import datetime

def create_comment(db: Session, comment: CommentCreateSchema):
    db_comment = CommentModel(**comment.dict())

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

def get_comments(db: Session, college_id: str):
    return db.query(CommentModel).filter(CommentModel.user_college_id == college_id).all()

def get_all(db: Session):
    comments = db.query(CommentModel).order_by(CommentModel.created_at).all()
    
    formatted_comments = []

    for comment in comments:
        formatted_comments.append(format_comment(db, comment))

    return formatted_comments

def get_all_from_today(db: Session):
    current_date = datetime.datetime.now().isoformat().split("T")[0]

    comments = db.query(CommentModel).filter(CommentModel.created_at > current_date).order_by(CommentModel.created_at).all()
    
    formatted_comments = []

    for comment in comments:
        formatted_comments.append(format_comment(db, comment))

    return formatted_comments

def format_comment(db: Session, comment: CommentSchema):
    user = UserService.get_user(db, comment.user_college_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    timestamp = str(comment.created_at).split()

    return {
        "author": user.name,
        "rating": comment.rating,
        "created_at_day": timestamp[0],
        "created_at_time": timestamp[1],
        "content": comment.content
    }