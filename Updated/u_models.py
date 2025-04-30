from sqlalchemy import  Boolean, Column, DateTime, Integer, Float, String, func, text, ForeignKey, Date, Enum as SqlEnum
from sqlalchemy.orm import DeclarativeBase
from enum import Enum

class Base(DeclarativeBase):
    pass

class CategoryEnum(Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    EMERGENCY = "Emergency"
    UTILITY = "Utility"
    OTHER = "Other"

class PaymentMethodEnum(Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    CASH = "Cash"
    UPI = "UPI"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text('true'))
    

class Expense(Base):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    category = Column(SqlEnum(CategoryEnum), nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False, server_default=text('0.0'))
    payment_method = Column(SqlEnum(PaymentMethodEnum), nullable=False)
    recurring = Column(Boolean, nullable=False, server_default=text('false'))
    balance = Column(Float, nullable=False, server_default=text('0.0'))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    