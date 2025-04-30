from math import exp
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data : dict):
    """Creates a jwt token that has a validity of value mentioned against ACCESS_TOKEN_EXPIRE_MINUTES"""
    to_encode = data.copy()

    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) + timedelta(hours=5,minutes=30)
    print(expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(payload=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    try :
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])

        id = payload['id']
        email = payload['email']

        if id is None or email is None:
            raise credentials_exception
        

    except InvalidTokenError:
        raise credentials_exception
    
    return id

   
def get_current_user(token : str = Depends(oauth2_scheme)):
    """Validates if the current user logged in has valid token"""
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Token Expired Or Invalid Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token,credentials_exception)
