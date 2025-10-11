from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class CatSerializer(BaseModel):
    name: str
    gender: str  # 'Male' or 'Female'
    litter_code: str
    date_of_birth: date
    description: Optional[str] = None
    photo_url: Optional[str] = None  # DEPRECATED - kept for compatibility
    photo_base64: Optional[str] = None  # Base64 encoded image data
    is_available: bool = True


class CreateCatRequest(CatSerializer):
    pass


class CatApiResponse(CatSerializer):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Allows using ORM objects directly
