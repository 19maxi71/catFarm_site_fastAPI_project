from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AdoptionQuestion, AdoptionRequest
from ..schemas import (
    AdoptionQuestionCreate,
    AdoptionQuestionResponse,
    AdoptionSubmitRequest,
    AdoptionRequestResponse
)
from typing import List, Optional, Dict
from datetime import datetime

router = APIRouter()

@router.get("/requests", response_model=List[AdoptionRequestResponse])
async def get_adoption_requests(db: Session = Depends(get_db)):
    requests = db.query(AdoptionRequest).order_by(AdoptionRequest.submitted_at.desc()).all()
    return requests

@router.get("/requests/{request_id}", response_model=AdoptionRequestResponse)
async def get_adoption_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(AdoptionRequest).filter(AdoptionRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Adoption request not found")
    return request

@router.put("/requests/{request_id}")
async def update_adoption_request(request_id: int, status: str, db: Session = Depends(get_db)):
    db_request = db.query(AdoptionRequest).filter(AdoptionRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Adoption request not found")

    db_request.status = status
    if status in ['approved', 'rejected']:
        from datetime import datetime
        db_request.notification_sent_at = datetime.utcnow()

    db.commit()
    db.refresh(db_request)
    return {"message": f"Request status updated to {status}"}

@router.get("/requests/export")
async def export_adoption_requests(db: Session = Depends(get_db)):
    """Export adoption requests as CSV."""
    from fastapi.responses import StreamingResponse
    import csv
    import io
    import json

    requests = db.query(AdoptionRequest).order_by(AdoptionRequest.submitted_at.desc()).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'ID', 'Customer Name', 'Email', 'Phone', 'Status', 'Submitted At',
        'Terms Agreed', 'Privacy Consent', 'Subscription', 'Notification Sent At'
    ])

    # Write data
    for request in requests:
        writer.writerow([
            request.id,
            request.customer_name,
            request.customer_email,
            request.phone or '',
            request.status,
            request.submitted_at.isoformat() if request.submitted_at else '',
            'Yes' if request.terms_agreed else 'No',
            'Yes' if request.privacy_consent else 'No',
            'Yes' if request.subscription else 'No',
            request.notification_sent_at.isoformat() if request.notification_sent_at else ''
        ])

    output.seek(0)

    # Return CSV file
    return StreamingResponse(
        io.StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=adoption_requests.csv"}
    )

@router.post("/submit")
async def submit_adoption_request(request: AdoptionSubmitRequest, db: Session = Depends(get_db)):
    if not request.terms_agreed:
        raise HTTPException(status_code=400, detail="You must read and agree to the terms to submit an adoption request.")

    if not request.privacy_consent:
        raise HTTPException(status_code=400, detail="You must consent to the privacy policy to submit an adoption request.")

    # Convert custom_answers dict to JSON string for storage
    import json
    custom_answers_json = json.dumps(request.custom_answers)

    db_request = AdoptionRequest(
        customer_email=request.customer_email,
        customer_name=request.customer_name,
        phone=request.phone,
        custom_answers=custom_answers_json,
        terms_agreed=request.terms_agreed,
        privacy_consent=request.privacy_consent,
        subscription=request.subscription
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    # TODO: Send email notification to admin
    return {"message": "Adoption request submitted successfully", "request_id": db_request.id}

@router.get("/form", response_model=List[AdoptionQuestionResponse])
async def get_adoption_form(db: Session = Depends(get_db)):
    """Get questions for the adoption form."""
    questions = db.query(AdoptionQuestion).order_by(AdoptionQuestion.order).all()
    return questions

@router.post("/questions", response_model=AdoptionQuestionResponse)
async def create_adoption_question(question: AdoptionQuestionCreate, db: Session = Depends(get_db)):
    db_question = AdoptionQuestion(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/questions/{question_id}", response_model=AdoptionQuestionResponse)
async def get_adoption_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(AdoptionQuestion).filter(AdoptionQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/questions/{question_id}", response_model=AdoptionQuestionResponse)
async def update_adoption_question(question_id: int, question: AdoptionQuestionCreate, db: Session = Depends(get_db)):
    db_question = db.query(AdoptionQuestion).filter(AdoptionQuestion.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question.dict().items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/questions/{question_id}")
async def delete_adoption_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(AdoptionQuestion).filter(AdoptionQuestion.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(db_question)
    db.commit()
    return {"message": "Question deleted successfully"}
