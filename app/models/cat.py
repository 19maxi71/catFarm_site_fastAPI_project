from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from ..database import Base


class Cat(Base):
    __tablename__ = "cats"

    # Set up indexing for faster searches in db
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # Cat's name (required)
    # e.g., 'king', 'queen', 'kitten'
    role = Column(String(20), nullable=False)
    breed = Column(String(100))  # Cat's breed (optional)
    bio = Column(Text)  # Long description (optional)
    # URL for cat's photo (optional) - DEPRECATED
    photo_url = Column(String(500))
    # Base64 encoded image data for persistent storage
    photo_base64 = Column(Text)
    # Is the cat vaccinated against rabies?
    rabies_vaccinated = Column(Boolean, default=False)
    # Optional field for awards or achievements
    award = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())  # When cat was added
    # When cat info was changed
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):  # Transforms the object into a string (for debugging)
        return f'Cat(id={self.id}, name={self.name}, role={self.role}, breed={self.breed})'
