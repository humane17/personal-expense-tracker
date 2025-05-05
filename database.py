from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from Updated import secret

engine = create_engine(secret.database_connection, echo=True)

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

#Session Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()