from secrets import token_urlsafe
import statistics
import fastapi 
from fastapi import Body, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm



from db_initializer import get_db
from models import users as user_model         
from schemas.users import CreateUserSchema, UserSchema, UserLoginSchema
from services.db import users as user_db_services
from typing import Dict
import cloudinary
import cloudinary.uploader


app = fastapi.FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post('/signup', response_model=UserSchema)
def signup(
    payload: CreateUserSchema = Body(),
    session: Session = Depends(get_db)
):
    payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
    return user_db_services.create_user(session, user=payload)

@app.post('/login', response_model=Dict)
def login(
    payload: UserLoginSchema = Body(),
    session: Session = Depends(get_db)
):
    try:
        user:user_model.User = user_db_services.get_user(
            session=session, email=payload.username
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    
    is_validated:bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    
    return user.generate_token()

@app.get('/profile/{id}', response_model=UserSchema)
def profile(id:int, 
            token: str = Depends(oauth2_scheme),
            session:Session=Depends(get_db)
        ):
    return user_db_services.get_user_by_id(session=session, id=id)

# @app.get('/logout')
# def logout(response: Response, 
#            request: Request,
#            token: str = Depends(oauth2_scheme),
#            user_db_services: Session = Depends(get_db)
#         ):
