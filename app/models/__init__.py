from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base


class Cat(Base):
    __tablename__ = "cats"  # This will be the table name in database

    # Like a cat's ID card number
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # Cat's name (required)
    breed = Column(String(50))  # Cat's breed (optional)
    description = Column(Text)  # Long description (optional)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())  # When cat was added
    # When cat info was changed
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
