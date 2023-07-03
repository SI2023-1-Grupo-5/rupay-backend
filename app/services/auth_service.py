from typing import Union, Any
from datetime import datetime, timedelta
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
# ACCESS_TOKEN_EXPIRE_MINUTES = 1  # 1 minute
ALGORITHM = "HS256"

# TODO: get this from environment
JWT_SECRET_KEY = "$3CR3T $3CR3T0"

def create_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = { "exp": expires_delta, "sub": str(subject) }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    
    return encoded_jwt

def is_cookie_valid(token):
    try:
        jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    except Exception as e:
        print(e)

        return False
    
    return True
    