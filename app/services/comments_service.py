from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import Comment as CommentModel
from app.database.schemas import CommentCreate as CommentCreateSchema
from app.database.schemas import Comment as CommentSchema

from app.services import user_service as UserService

import datetime
import urllib.request
import ssl
import re

def create_comment(db: Session, comment: CommentCreateSchema):
    current_date = datetime.datetime.now().isoformat()

    db_comment = CommentModel(
        content=comment.content,
        rating=comment.rating,
        user_college_id=comment.user_college_id,
        created_at=current_date,
        campus=comment.campus
    )

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

def get_all_from_today(db: Session, campus: str):
    current_date = datetime.datetime.now().isoformat().split("T")[0]

    comments = db.query(CommentModel).filter(
        CommentModel.created_at > current_date, 
        CommentModel.campus == campus
    ).order_by(CommentModel.created_at).all()
    
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
        "content": comment.content,
        "campus": comment.campus
    }

def get_menu_links(id: int = None):
    fp = urllib.request.urlopen("https://ru.unb.br/index.php/cardapio-refeitorio", context=ssl._create_unverified_context())
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    indexes = [m.start() for m in re.finditer('images/Artigos', mystr)]

    valid_links = []

    for idx in indexes:
        slice = mystr[idx:idx+200]

        if ">ISM" in slice:
            formatted_link = slice.split(">ISM")[0][:-18]
            valid_links.append(formatted_link)

    menus = [
        {
            "id": 1,
            "name": "Darcy Ribeiro",
            "link": f"https://ru.unb.br/{valid_links[0]}"
        },
        {
            "id": 2,
            "name": "Ceilândia",
            "link": f"https://ru.unb.br/{valid_links[1]}"
        },
        {
            "id": 3,
            "name": "Gama",
            "link": f"https://ru.unb.br/{valid_links[2]}"
        },
        {
            "id": 4,
            "name": "Planaltina",
            "link": f"https://ru.unb.br/{valid_links[3]}"
        }
    ]

    if id: 
        return [menus[id-1]]

    return menus