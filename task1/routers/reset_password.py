from fastapi import Depends,HTTPException,APIRouter
from .. import models1,schemas1, utils1
from sqlalchemy.orm import Session
from ..database1 import get_db
from ..protector_route import get_current_user


routers = APIRouter(prefix="/change-password")
@routers.put("/")
def change_password(change_pass: schemas1.ChangePassword, db: Session = Depends(get_db), current_user: models1.User = Depends(get_current_user)):
    user = db.query(models1.User).filter(models1.User.id == current_user["user_id"]).first()

    if not user or not utils1.verify_password(change_pass.old_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user.password = utils1.hash_password(change_pass.new_password)
    db.commit()

    return {"message": "Password changed successfully"}
