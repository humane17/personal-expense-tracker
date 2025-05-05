from typing import List
from fastapi import HTTPException, status, Depends, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import schemas, u_models, auth, utils
from database import get_db



router = APIRouter(tags=["Authentication & User"])

#User Login For Devs
@router.post("/login-json", include_in_schema=False)
def login(user_credentials : schemas.UserLogin , db : Session = Depends(get_db)):
    """Returns A Access Token If Given Credentials Are Valid"""

    user_data = db.query(u_models.User).filter_by(email = user_credentials.email).first()
    print(user_data)
    print("User credentials is in /login-json flow",user_credentials)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid User")
    
    verified = utils.verify_hash_password(user_credentials.password,user_data.hash_password)
    
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Password")
    
    token = auth.create_access_token(data = {"id" : user_data.id, "email": user_data.email})
    
    return {"access_token": token, "token_type":"bearer"}

#User Login For Clients
@router.post("/login")
def login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    """Returns A Access Token If Given Credentials Are Valid"""

    user_data = db.query(u_models.User).filter_by(email = user_credentials.username).first()
    print(user_data)
    print("User credentials is in /login flow ",user_credentials)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid User")
    
    verified = utils.verify_hash_password(user_credentials.password,user_data.hash_password)
    
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Password")
    
    token = auth.create_access_token(data = {"id" : user_data.id, "email": user_data.email})
    
    return {"access_token": token, "token_type":"bearer"}


#Get All Users
@router.get("/get/users", response_model=List[schemas.UserResponse])
def get_users(db : Session = Depends(get_db)):
    """Returns All Active Users"""

    users = db.query(u_models.User).filter_by(is_active=True).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There are no users present.")

    return users

#Get User By Id
@router.get("/get/user", response_model=schemas.UserResponse)
def get_user_by_id(id : int, db : Session = Depends(get_db)):
    """Returns Particular User By Id"""

    user_data = db.query(u_models.User).filter_by(id = id).first()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found for id {id}")
    
    return user_data

#Create a New User
@router.post("/create/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(data : schemas.UserCreate, db : Session = Depends(get_db)):
    """Creates A New User And Returns Their Id"""

    try:
        hash_pwd = utils.hash_password(data.password)
        user = u_models.User(email=data.email,hash_password=hash_pwd)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error is {error}")

#Update User by Id
@router.post("/update/user/{id}", status_code=status.HTTP_200_OK)
def update_user_by_id(id : int  = Depends(auth.get_current_user), db : Session = Depends(get_db),
                      req_body : schemas.UserCreate = Body()):
    """Updates User Password Based On Id and Email"""

    user = db.query(u_models.User).filter_by(id = id)
    user_data = user.first()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user found for id {id}")
    
    if user_data.email != req_body.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user found with email - {req_body.email}")
    
    hash_pwd = utils.hash_password(req_body.password)
    user.update({"hash_password" : hash_pwd,"email" : req_body.email}, synchronize_session=False)
    db.commit()
    db.refresh(user_data)

    return {"message": "Data Updated Successfully."}
    
#Delete a User - Soft deletes.
@router.delete("/delete/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id : int = Depends(auth.get_current_user), db : Session = Depends(get_db)):
    """Soft Deletes A User Based On Given Id"""

    user = db.query(u_models.User).filter_by(id = id)
    user_data = user.first()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found for id {id}")
    
    user.update({"is_active" : False}, synchronize_session=False)
    db.commit()

    return {"message" : "User Deleted"}
