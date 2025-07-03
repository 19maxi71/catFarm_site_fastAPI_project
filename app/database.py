from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get your Mac username automatically
username = os.getenv('USER')

# Use your Mac username (no password needed for local development)
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}@localhost/catfarm"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
