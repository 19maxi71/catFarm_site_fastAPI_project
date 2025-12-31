from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class AdoptionQuestionCreate(BaseModel):
    question_text: str
    question_type: str
    options: Optional[str] = None
    is_required: bool = True
    display_order: int = 0


class AdoptionQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    options: Optional[str] = None
    is_required: Optional[bool] = None
    display_order: Optional[int] = None


class AdoptionQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    options: Optional[str]
    is_required: bool
    display_order: int

    class Config:
        from_attributes = True


class AdoptionSubmitRequest(BaseModel):
    customer_email: str
    customer_name: str
    phone: Optional[str] = None
    litter_code: Optional[str] = None
    custom_answers: Dict[str, str]
    terms_agreed: bool
    privacy_consent: bool
    subscription: bool = False
    website: Optional[str] = None  # Honeypot field for spam prevention


class AdoptionRequestResponse(BaseModel):
    id: int
    customer_email: str
    customer_name: str
    phone: Optional[str]
    litter_code: Optional[str]
    custom_answers: Optional[str]
    terms_agreed: Optional[bool]
    privacy_consent: Optional[bool]
    subscription: Optional[bool]
    submitted_at: datetime
    status: str
    rejection_reason: Optional[str]
    notification_sent_at: Optional[datetime]

    class Config:
        from_attributes = True
