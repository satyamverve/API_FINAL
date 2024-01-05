#app/oauth/oauth2.py

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.auth.auth_schema import TokenData
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user_tables import User
from app.data.data_class import settings
import utils

# credentials_exceptions= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                                           detail="Could not validate credentials",
#                                           headers={"WWW-Authenticate": "Bearer"})

# class BearAuthException(Exception):
#     def __init__(self, detail: str = "Bearer authentication failed"):
#         self.detail = detail
#         super().__init__(self.detail)


oauth2_schema= OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
    if not isinstance(data, dict):
        raise ValueError("Input data should be a dictionary")

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire, "email": to_encode.get("email")})
    to_encode["user_email"] = str(to_encode.get("user_email"))

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("user_email")
        if email is None:
            raise credentials_exceptions
        token_data = TokenData(email=email)
    except JWTError as e:
        raise credentials_exceptions from e
    return token_data

def get_user_by_email(db: Session, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_email} not found",
        )
    return user

def get_current_user(token:str = Depends(oauth2_schema),db : Session = Depends(get_db) ):
    credentials_exceptions= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    #logic to get the db details(email-id, user, etc) of the current logged user
    token = verify_access_token(token, credentials_exceptions)
    user= db.query(User).filter(User.email == token.email).first()
    return user


def get_current_user_via_temp_token(temp_token: str, db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Using the verify_access_token function for decoding
    token_data = verify_access_token(temp_token, credentials_exceptions)

    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {token_data.email} not found",
        )

    return user
