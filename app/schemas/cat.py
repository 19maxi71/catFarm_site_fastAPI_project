from pydantic import BaseModel, field_validator
from datetime import datetime, date, timezone
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def make_datetime_aware(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    class Config:
        from_attributes = True  # Allows using ORM objects directly
