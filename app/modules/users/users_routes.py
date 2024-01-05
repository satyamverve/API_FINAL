# app/modules/users_routes.py

import sys

sys.path.append("..")
from fastapi import APIRouter, Depends, HTTPException, Path, status, Request, Form, Query
from sqlalchemy.orm import Session
from app.dto.users_schema import UserCreate, UserOut , UserChangePassword
from app.modules.users.users_service import create_user, get_user, update_user, delete_user, user_change_password, user_reset_password
from app.config.database import  get_db
from app.oauth import oauth2
from app.models.user_tables import User 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app import templates
from app.email_notifications.notify import send_registration_notification, send_reset_password_mail


templates_path = "templates"
templates = Jinja2Templates(directory=templates_path)

router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED ,response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/{user_id}",response_model=UserOut)
def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)



@router.put("/{user_id}")
def update_user_api(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


@router.patch("/change_password",summary="Change password for a logged in user")
def change_password(email: str, user_change_password_body: UserChangePassword, db: Session = Depends(get_db), user: User = Depends(oauth2.get_current_user),):
    """
    Changes password for a logged in user.
    """
    try:
        user_change_password(db, email, user_change_password_body)
        return {"result": f"{user.username} your password has been updated!"}
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")



@router.post("/reset_password",summary="Resets password for a user")
def reset_password(email: str, request: Request, new_password: str = Form(...), user: User = Depends(oauth2.get_current_user_via_temp_token),
                         db: Session = Depends(get_db)):
    """
    Resets password for a user.
    """
    try:
        result = user_reset_password(db, email, new_password)
        return templates.TemplateResponse(
            "reset_password_result.html",
            {
                "request": request,
                "success": result
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")

@router.get("/reset_password_template",response_class=HTMLResponse,summary="Reset password for a user")
def reset_password_template(request: Request, user: User = Depends(oauth2.get_current_user_via_temp_token)):
    """
    Resets password for a user.
    """
    try:
        token = request.query_params.get('access_token')
        return templates.TemplateResponse(
            "reset_password.html",
            {
                "request": request, 
                "user": user, 
                "access_token": token
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.post("/forgot_password", summary="Trigger forgot password mechanism for a user")
async def user_forgot_password(request: Request, user_email: str = Form(...),  db: Session = Depends(get_db)):
    """
    Triggers forgot password mechanism for a user.
    """
    TEMP_TOKEN_EXPIRE_MINUTES = 10
    try:
        user = oauth2.get_user_by_email(db=db, user_email=user_email)
        if user:
            access_token = oauth2.create_access_token(data={"user_email": user_email}, expire_minutes=TEMP_TOKEN_EXPIRE_MINUTES)
            url = f"{request.base_url}users/reset_password_template?access_token={access_token}"

            await send_reset_password_mail(
                recipient_email=user_email,
                user=user,
                url=url,
                expire_in_minutes=TEMP_TOKEN_EXPIRE_MINUTES
            )
        return {
            "result": f"An email has been sent to {user_email} with a link for password reset."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred. Report this message to support: {e}"
        )
