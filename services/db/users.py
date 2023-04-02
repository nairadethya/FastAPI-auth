from sqlalchemy.orm import Session
from sqlalchemy import select

from models.users import User
from schemas.users import CreateUserSchema

def create_user(session:Session, user:CreateUserSchema):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(session:Session, email:str):
    return session.query(User).filter(User.email==email).one()