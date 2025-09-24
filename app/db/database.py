from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


