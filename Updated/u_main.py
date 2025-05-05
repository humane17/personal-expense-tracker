from fastapi import FastAPI
from . import u_models
from . import expense, user
from database import engine

app = FastAPI(title="Personal Expense Tracker.", 
              description="Current Version Only Accepts Expenses Not Income.", version="0.1.0")


#Creates tables in postgres if they don't exist.
u_models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(expense.router)