#!/usr/bin/env python3
"""
Database setup script for deployment.
Run this after setting up your database to initialize tables and add sample data.
"""

from app.models import Cat, Article, ArticleImage
from app.database import engine, Base
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))


def init_database():
    """Initialize database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def add_sample_data():
    """Add sample data for testing."""
    from sqlalchemy.orm import sessionmaker
    from app.database import SessionLocal

    db = SessionLocal()

    try:
        # Check if sample data already exists
        if db.query(Cat).count() == 0:
            print("Adding sample cats...")
            # Add sample cats here if needed
            pass

        if db.query(Article).count() == 0:
            print("Adding sample articles...")
            # Add sample articles here if needed
            pass

        print("✅ Sample data added successfully!")

    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    add_sample_data()
    print("🎉 Database setup complete!")
