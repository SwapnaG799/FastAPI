from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database1 import get_db
from .. import models1, utils1
from fastapi.security import OAuth2PasswordRequestForm
from .. import oauth2_1  

routers=APIRouter(prefix="/user", tags=["Authentication"])


@routers.post("/")
def login( db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models1.User).filter(models1.User.email == form_data.username).first()

    if not user or not utils1.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token = oauth2_1.create_access_token({"user_id": user.id})
    
    return {"access_token": token, "token_type": "bearer"}


