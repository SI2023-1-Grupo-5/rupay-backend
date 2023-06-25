
from sqlalchemy.orm import Session

from app.database.schemas import CardRecharge as CardRecharge
from app.services.user_service import update_balance


def card_payment(db: Session, college_id: str, card: CardRecharge):
    if card.value <= 0:
        raise Exception("Credit recharge value must be greater than 0")
    update_balance(db, card.value, college_id)    

# TODO: Add credit card info validation
