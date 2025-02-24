from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models1, oauth2_1, database1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database1.get_db)):
    payload = oauth2_1.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(models1.User).filter(models1.User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {"user_id": user.id, "email": user.email}