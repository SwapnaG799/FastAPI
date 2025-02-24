from fastapi import FastAPI,HTTPException,Depends
from . import models1
from .database1 import engine
from .routers import auth1,login, reset_password

models1.Base.metadata.create_all(bind=engine)  # Create database tables

task1 = FastAPI()

task1.include_router(auth1.routers)
task1.include_router(login.routers)
task1.include_router(reset_password.routers)
