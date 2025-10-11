from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date
from sqlalchemy.sql import func
from ..database import Base


class Cat(Base):
    __tablename__ = "cats"

    # Set up indexing for faster searches in db
    id = Column(Integer, primary_key=True, index=True)
    # Cat's name (for admin reference)
    name = Column(String(50), nullable=False)
    # Gender: 'Male' or 'Female'
    gender = Column(String(10), nullable=False)
    # Unique litter code given by breeder
    litter_code = Column(String(20), nullable=False, unique=True)
    # Date of birth
    date_of_birth = Column(Date, nullable=False)
    # Description of the kitten
    description = Column(Text)
    # URL for cat's photo (optional) - DEPRECATED
    photo_url = Column(String(500))
    # Base64 encoded image data for persistent storage
    photo_base64 = Column(Text)
    # Availability status
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())  # When cat was added
    # When cat info was changed
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):  # Transforms the object into a string (for debugging)
        return f'Cat(id={self.id}, name={self.name}, litter_code={self.litter_code}, gender={self.gender})'
