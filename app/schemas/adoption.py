from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class AdoptionQuestionCreate(BaseModel):
    question_text: str
    question_type: str
    options: Optional[str] = None
    is_required: bool = True
    order: int = 0

class AdoptionQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    options: Optional[str]
    is_required: bool
    order: int

    class Config:
        from_attributes = True

class AdoptionSubmitRequest(BaseModel):
    customer_email: str
    customer_name: str
    phone: Optional[str] = None
    custom_answers: Dict[str, str]
    terms_agreed: bool
    privacy_consent: bool
    subscription: bool = False

class AdoptionRequestResponse(BaseModel):
    id: int
    customer_email: str
    customer_name: str
    phone: Optional[str]
    custom_answers: Optional[str]
    terms_agreed: bool
    privacy_consent: bool
    subscription: bool
    submitted_at: datetime
    status: str
    notification_sent_at: Optional[datetime]

    class Config:
        from_attributes = True
