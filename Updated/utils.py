from passlib.context import CryptContext


# Create a CryptContext for handling password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password : str):
    return pwd_context.hash(password)

def verify_hash_password(password,hash_password):
    return pwd_context.verify(password,hash_password)

