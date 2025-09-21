from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CatSerializer(BaseModel):
    name: str
    role: str
    breed: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None  # DEPRECATED - kept for compatibility
    photo_base64: Optional[str] = None  # Base64 encoded image data
    rabies_vaccinated: bool = False
    award: Optional[str] = None


class CreateCatRequest(CatSerializer):
    pass


class CatApiResponse(CatSerializer):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Allows using ORM objects directly
