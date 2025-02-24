
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from task1.database1 import get_db
from .. import models1, schemas1, utils1


routers = APIRouter(prefix="/auth", tags=["Authentication"])

@routers.post("/register", response_model=schemas1.UserResponse)
def register_user(user_data: schemas1.UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_user = db.query(models1.User).filter(models1.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and create the user
    hashed_password = utils1.hash_password(user_data.password)
    new_user = models1.User(name=user_data.name, email=user_data.email, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
