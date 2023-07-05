from fastapi import APIRouter, Depends, HTTPException, status

from app.services import payment_service

from app.database.schemas import CardRecharge as CardRechargeSchema

from sqlalchemy.orm import Session
from app.database.init import SessionLocal

router = APIRouter(
    prefix='/payment',
    tags=['Payment']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/card/{college_id}", status_code=status.HTTP_200_OK)
def card_recharge(college_id: str, card: CardRechargeSchema, db: Session = Depends(get_db)):

    try:
        payment_service.card_payment(db, college_id, card)
        return {"message": "success"}
    except Exception as e:

        print(e.args)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User or card information are incorrect'
        )
