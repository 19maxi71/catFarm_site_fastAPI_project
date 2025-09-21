from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration - supports both local development and production
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"🔍 DATABASE_URL from environment: {DATABASE_URL}")

if not DATABASE_URL:
    # Fallback to local development (SQLite for simplicity in demo)
    DATABASE_URL = "sqlite:///./catfarm.db"
    print("⚠️  No DATABASE_URL found, using SQLite fallback")
else:
    print(f"✅ Using PostgreSQL: {DATABASE_URL[:50]}...")

print(f"🎯 Final DATABASE_URL: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=True  # Debug SQL queries
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
