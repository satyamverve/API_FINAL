# app/modules/users_service.py
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.user_tables import User 
from app.dto.users_schema import UserCreate, UserChangePassword, UserUpdateMe
import utils
from app.oauth import oauth2
from random import randint



def create_user(db: Session, user: UserCreate): #INSERT or CREATE
    
    #hash the password -- user.password
    hashed_password= utils.hash(user.password)
    user.password = hashed_password
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    # print("hello")
    user= db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



def update_user(db: Session, user_id: int, user: UserCreate):
    #hash the password -- user.password
    hashed_password= utils.hash(user.password)
    user.password = hashed_password
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")   


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)  
        db.commit()
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")



def user_change_password(db: Session, email: str, user_change_password_body: UserChangePassword, 
        current_user: int = Depends(oauth2.get_current_user), user: User = Depends(oauth2.get_current_user)):
    user = db.query(User).filter(User.email == email).first()

    if not utils.verify(user_change_password_body.old_password, user.password):
        raise ValueError(
            f"Old password provided doesn't match, please try again")
    user.password = utils.hash(user_change_password_body.new_password)
    db.commit()


def user_reset_password(db: Session, email: str, new_password: str):
    try:
        user = db.query(User).filter(User.email == email).first()
        user.password = utils.hash(new_password)
        db.commit()
    except Exception:
        return False
    return True


def update_me(db: Session, email: str, user_update: UserUpdateMe):
    user = db.query(User).filter(User.email == email).first()

    updated_user = user_update.dict(exclude_unset=True)
    for key, value in updated_user.items():
        setattr(user, key, value)
    db.commit()
    return user

def get_users(db: Session):
    users = list(db.query(User).all())
    return users



