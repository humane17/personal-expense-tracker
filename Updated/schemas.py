from datetime import date
from typing import Optional
from unittest.mock import Base
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
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
    category : str
    date : date 
    payment_method : u_models.PaymentMethodEnum
    description : Optional[str] = None

    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str