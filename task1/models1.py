from sqlalchemy import Column, Integer, String
from .database1 import Base

class User(Base):
    __tablename__ = "users1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed Password
