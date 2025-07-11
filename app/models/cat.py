from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from ..database import Base

class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True) # Set up indexing for faster searches in db
    name = Column(String(50), nullable=False) # Cat's name (required)
    role = Column(String(20), nullable=False)  # e.g., 'king', 'queen', 'kitten'
    breed = Column(String(100))  # Cat's breed (optional)
    bio = Column(Text)  # Long description (optional)
    photo_url = Column(String(500))  # URL for cat's photo (optional)
    rabies_vaccinated = Column(Boolean, default=False)  # Is the cat vaccinated against rabies?
    award = Column(String(200), nullable=True)  # Optional field for awards or achievements
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # When cat was added
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # When cat info was changed

    def __repr__(self):
        return f'Cat(id={self.id}, name={self.name}, role={self.role}, breed={self.breed})'
