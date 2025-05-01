from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from Updated import expense, user
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import u_models, schemas
from .utils import hash_password,verify_hash_password
from .auth import create_access_token, get_current_user


app = FastAPI()


#Creates tables in postgres if they don't exist.
u_models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(expense.router)