from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import secret


SECRET_KEY = secret.key
ALGORITHM = secret.algo
ACCESS_TOKEN_EXPIRE_MINUTES = 4

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
    """Decodes the received token and checks if its valid"""
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
