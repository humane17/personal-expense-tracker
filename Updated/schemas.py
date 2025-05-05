from datetime import date
from unittest.mock import Base
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from . import u_models

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    email : EmailStr

class ExpenseCreate(BaseModel):
    date : date
    category : u_models.CategoryEnum
    description : str = None
    amount : float
    payment_method : u_models.PaymentMethodEnum
    balance : float

class ExpenseResponse(BaseModel):
    id : int
    amount : float

    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str