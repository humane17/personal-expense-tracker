from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from . auth import get_current_user
from . import u_models, schemas

router = APIRouter(tags=["Expense"])

#Get User Expenses Based on UserId Obtained from auth.
@router.get("/get/expense/")
def get_user_expenses(user_id : str = Depends(get_current_user), db : Session = Depends(get_db)):
    """Post Authentication, Gets All Expenses Of A User Based On Their Id"""

    user_expenses = db.query(u_models.Expense).filter_by(user_id=user_id).all()

    if not user_expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid User OR No Expenses found.")

    return {"data": user_expenses}

#Create a New Expense
@router.post("/create/expense", status_code=status.HTTP_201_CREATED)
def create_expense(expense_data : schemas.ExpenseCreate, db : Session = Depends(get_db), 
                   user_id : str = Depends(get_current_user)):
    """Post Authentication, Creates And Stores An Expense Against User Id"""

    print("User id",user_id)
    new_expense = u_models.Expense(date = expense_data.date, category = expense_data.category,
                                   description = expense_data.description,amount = expense_data.amount,
                                   payment_method = expense_data.payment_method, balance = expense_data.balance,
                                   user_id = user_id)
    db.add(new_expense)

    db.commit()
    db.refresh(new_expense)

    return {"data" : new_expense}


#Delete an Expense
@router.delete("/delete/expense/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id : int, db : Session = Depends(get_db), user_id : str = Depends(get_current_user)):
    """Post Authentication, Deletes An Expense Based On Id Given"""

    get_expense = db.query(u_models.Expense).filter_by(id=id).first()

    if not get_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The expense with id {id} does not exist.')
    
    db.delete(get_expense)
    db.commit()
    
    return


#Update an Expense
@router.post("/update/expense/{id}")
def update_expense(id : int, expense_data : schemas.ExpenseCreate, db : Session = Depends(get_db),
                   user_id : str = Depends(get_current_user)):
    """Post Authentication, Updates Data Fields Of A Given Expense"""
    
    expense = db.query(u_models.Expense).filter_by(id=id)
    get_expense = expense.first()

    if not get_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The expense with id {id} does not exist.')
    
    expense.update(date = expense_data.date, category = expense_data.category,
                   description = expense_data.description,amount = expense_data.amount,
                   payment_method = expense_data.payment_method, balance = expense_data.balance,
                                synchronize_session=False)
    
    db.commit()

    return db.refresh(get_expense)