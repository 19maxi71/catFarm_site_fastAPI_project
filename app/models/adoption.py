from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class AdoptionQuestion(Base):
    __tablename__ = "adoption_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(500), nullable=False)
    question_type = Column(String(50), nullable=False)  # 'text', 'checkbox', 'select'
    options = Column(Text, nullable=True)  # JSON string for select options
    is_required = Column(Boolean, default=True)
    order = Column(Integer, default=0)


class AdoptionRequest(Base):
    __tablename__ = "adoption_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_email = Column(String(255), nullable=False)
    customer_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    custom_answers = Column(Text, nullable=True)  # JSON string
    terms_agreed = Column(Boolean, default=False)
    subscription = Column(Boolean, default=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="pending")  # 'pending', 'approved', 'rejected'
    notification_sent_at = Column(DateTime(timezone=True), nullable=True)
