from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("postgres db url", echo=True)

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

#Session Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()