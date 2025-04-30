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

# #User Login
# @app.post("/login")
# def login(user_credentials : schemas.UserLogin, db : Session = Depends(get_db)):

#     user_data = db.query(u_models.User).filter_by(email = user_credentials.email).first()

#     if not user_data:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid User")
    
#     verified = verify_hash_password(user_credentials.password,user_data.hash_password)
    
#     if not verified:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Password")
    
#     token = create_access_token(data = {"id" : user_data.id, "email": user_data.email})
    
#     return {"access_token": token, "token_type":"bearer"}


# #Get All Users
# @app.get("/get/users")
# def get_users(db : Session = Depends(get_db)):

#     users = db.query(u_models.User).filter_by(is_active=True).all()
    
#     if not users:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There are no users present.")

#     return {"data" : users}

# #Get User By Id
# @app.get("/get/user/")
# def get_user_by_id(id : int, db : Session = Depends(get_db)):

#     user_data = db.query(u_models.User).filter_by(id = id).first()

#     if not user_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found for id {id}")
    
#     return user_data

# #Create a New User
# @app.post("/create/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
# def create_user(data : schemas.UserCreate, db : Session = Depends(get_db)):

#     try:
#         hash_pwd = hash_password(data.password)
#         user = u_models.User(email=data.email,hash_password=hash_pwd)

#         db.add(user)
#         db.commit()
#         db.refresh(user)

#         return user
    
#     except SQLAlchemyError as error:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error is {error}")

# #Update User by Id
# @app.post("/update/user/{id}")
# def update_user_by_id(id : int, db : Session = Depends(get_db), data = schemas.UserCreate):

#     user = db.query(u_models.User).filter_by(id = id)
#     user_data = user.first()

#     if not user_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found for id {id}")
    
#     user.update(email = data.email,password = data.password)
#     db.commit()

#     return db.refresh(user_data)
    
# #Delete a User. Soft deletes.
# @app.delete("/delete/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(id : int, db : Session = Depends(get_db)):

#     user = db.query(u_models.User).filter_by(id = id)
#     user_data = user.first()

#     if not user_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found for id {id}")
    
#     user.update(is_active=False)
#     db.commit()

#     return


# #Get All Expenses irrespective of User
# @app.get("/get/expenses")
# def get_expenses(db : Session = Depends(get_db)):

#     expenses = db.query(u_models.Expense).all()
    
#     if not expenses:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Expenses found.")

#     return {"data" : expenses}



# #Get User Expenses By Providing User's Id As Query Param.
# @app.get("/get/expense/")
# def get_user_expenses(id : int,db : Session = Depends(get_db)):

#     user_expenses = db.query(u_models.Expense).filter_by(user_id=id).all()

#     if not user_expenses:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid User OR No Expenses found.")

#     return {"data": user_expenses}


# #Get User Expenses Based on UserId Obtained from auth.
# @app.get("/get/expense/")
# def get_user_expenses(id : str = Depends(get_current_user), db : Session = Depends(get_db)):

#     user_expenses = db.query(u_models.Expense).filter_by(user_id=id).all()

#     if not user_expenses:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid User OR No Expenses found.")

#     return {"data": user_expenses}

# #Create a New Expense
# @app.post("/create/expense", status_code=status.HTTP_201_CREATED)
# def create_expense(expense_data : schemas.ExpenseCreate, db : Session = Depends(get_db), 
#                    user_id : str = Depends(get_current_user)):

#     print("User id",user_id)
#     new_expense = u_models.Expense(date = expense_data.date, category = expense_data.category,
#                                    description = expense_data.description,amount = expense_data.amount,
#                                    payment_method = expense_data.payment_method, balance = expense_data.balance,
#                                    user_id = user_id)
#     db.add(new_expense)

#     db.commit()
#     db.refresh(new_expense)

#     return {"data" : new_expense}


# #Delete an Expense
# @app.delete("/delete/expense/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_expense(id : int, db : Session = Depends(get_db), user_id : str = Depends(get_current_user)):

#     get_expense = db.query(u_models.Expense).filter_by(id=id).first()

#     if not get_expense:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'The expense with id {id} does not exist.')
    
#     db.delete(get_expense)
#     db.commit()
    
#     return


# #Update an Expense
# @app.post("/update/expense/{id}")
# def update_expense(id : int, expense_data : schemas.ExpenseCreate, db : Session = Depends(get_db), 
#                    user_id : str = Depends(get_current_user)):
    
#     expense = db.query(u_models.Expense).filter_by(id=id)
#     get_expense = expense.first()

#     if not get_expense:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'The expense with id {id} does not exist.')
    
#     expense.update(date = expense_data.date, category = expense_data.category,
#                    description = expense_data.description,amount = expense_data.amount,
#                    payment_method = expense_data.payment_method, balance = expense_data.balance,
#                                 synchronize_session=False)
    
#     db.commit()

#     return db.refresh(get_expense)