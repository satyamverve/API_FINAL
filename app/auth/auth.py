#app/auth/auth.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import session
from app.config.database import get_db
from app.models.user_tables import User
import utils
from app.oauth import oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter( )

@router.post('/login')

#now making the login by the help of fastapi inbuilt class(bydefault in payload it takes username and password)
def user_login(user_credentials : OAuth2PasswordRequestForm= Depends(), db : session= Depends(get_db)):
    #use this to login with email as username
    user = db.query(User).filter(User.email == user_credentials.username).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Invalid Credentials")
    #create token (remember this is the data(i.e, user_email) which I want to put in the payload you can take whatever you want)
    access_token= oauth2.create_access_token(data= {"user_email" : user.email})
    #Here bearer is the the declaration where we put our token to validate
    return {"access_token": access_token, "token_type" : "bearer"} 
     