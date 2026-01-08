from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AdoptionQuestion, AdoptionRequest
from ..schemas import (
    AdoptionQuestionCreate,
    AdoptionQuestionUpdate,
    AdoptionQuestionResponse,
    AdoptionSubmitRequest,
    AdoptionRequestResponse
)
from typing import List, Optional, Dict
from datetime import datetime
import os
import json


async def send_adoption_email_notification(request: AdoptionRequest, custom_answers: Dict[str, str], db: Session):
    """Send email notification to admin about new adoption request."""
    # Get admin email from environment variable
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@lavandercats.com')

    # Get question texts for the email
    question_texts = {}
    questions = db.query(AdoptionQuestion).all()
    for q in questions:
        question_texts[str(q.id)] = q.question_text

    # Build email content
    subject = f"Cat Adoption Request - Litter {request.litter_code}"

    body = f"""
New Adoption Request Received

Customer Information:
- Name: {request.customer_name}
- Email: {request.customer_email}
- Phone: {request.phone or 'Not provided'}
- Litter Code: {request.litter_code}
- Submitted: {request.submitted_at}

Questionnaire Responses:
"""

    for question_id, answer in custom_answers.items():
        question_text = question_texts.get(
            question_id, f"Question {question_id}")
        body += f"- {question_text}: {answer}\n"

    body += f"""
Legal Agreements:
- Terms Agreed: {'Yes' if request.terms_agreed else 'No'}
- Privacy Consent: {'Yes' if request.privacy_consent else 'No'}
- Newsletter Subscription: {'Yes' if request.subscription else 'No'}

Please review this application in the admin panel.
"""

    # For now, just print the email (replace with actual email sending)
    print("=" * 50)
    print("ADOPTION REQUEST EMAIL NOTIFICATION")
    print("=" * 50)
    print(f"To: {admin_email}")
    print(f"Subject: {subject}")
    print(body)
    print("=" * 50)

    # TODO: Implement actual email sending with SMTP
    # import smtplib
    # from email.mime.text import MIMEText
    #
    # msg = MIMEText(body)
    # msg['Subject'] = subject
    # msg['From'] = 'noreply@lavandercats.com'
    # msg['To'] = admin_email
    #
    # # Send email using SMTP
    # # server = smtplib.SMTP('smtp.gmail.com', 587)
    # # server.starttls()
    # # server.login("your-email@gmail.com", "your-password")
    # # server.sendmail("your-email@gmail.com", admin_email, msg.as_string())
    # # server.quit()

router = APIRouter(prefix="/adoption")


@router.get("/requests/export")
async def export_adoption_requests(db: Session = Depends(get_db)):
    """Export adoption requests as CSV."""
    from fastapi.responses import StreamingResponse
    import csv
    import io

    requests = db.query(AdoptionRequest).order_by(
        AdoptionRequest.submitted_at.desc()).all()

    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'ID', 'Customer Name', 'Email', 'Phone', 'Litter Code',
        'Status', 'Submitted At', 'Terms Agreed', 'Privacy Consent',
        'Subscription', 'Custom Answers'
    ])

    # Write data
    for request in requests:
        writer.writerow([
            request.id,
            request.customer_name,
            request.customer_email,
            request.phone or '',
            request.litter_code or '',
            request.status,
            request.submitted_at.isoformat() if request.submitted_at else '',
            request.terms_agreed,
            request.privacy_consent,
            request.subscription,
            request.custom_answers or ''
        ])

    output.seek(0)
    response = StreamingResponse(
        io.StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=adoption_requests.csv"}
    )
    return response


@router.get("/requests", response_model=List[AdoptionRequestResponse])
async def get_adoption_requests(db: Session = Depends(get_db)):
    requests = db.query(AdoptionRequest).order_by(
        AdoptionRequest.submitted_at.desc()).all()
    return requests


@router.get("/requests/{request_id}", response_model=AdoptionRequestResponse)
async def get_adoption_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(AdoptionRequest).filter(
        AdoptionRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=404, detail="Adoption request not found")
    return request


@router.put("/requests/{request_id}")
async def update_adoption_request(request_id: int, request_data: dict, db: Session = Depends(get_db)):
    db_request = db.query(AdoptionRequest).filter(
        AdoptionRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(
            status_code=404, detail="Adoption request not found")

    status = request_data.get("status")
    rejection_reason = request_data.get("rejection_reason")

    if status:
        db_request.status = status
        if status in ['approved', 'rejected']:
            from datetime import datetime, timezone
            db_request.notification_sent_at = datetime.now(timezone.utc)

    if rejection_reason is not None:
        db_request.rejection_reason = rejection_reason

    db.commit()
    db.refresh(db_request)
    return {"message": f"Request status updated to {status}"}


@router.delete("/requests/{request_id}")
async def delete_adoption_request(request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(AdoptionRequest).filter(
        AdoptionRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(
            status_code=404, detail="Adoption request not found")

    db.delete(db_request)
    db.commit()
    return {"message": "Adoption request deleted successfully"}


@router.get("/requests/export")
async def export_adoption_requests(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'ID', 'Customer Name', 'Email', 'Phone', 'Litter Code', 'Status', 'Rejection Reason', 'Submitted At',
        'Terms Agreed', 'Privacy Consent', 'Subscription', 'Notification Sent At'
    ])

    # Write data
    for request in requests:
        writer.writerow([
            request.id,
            request.customer_name,
            request.customer_email,
            request.phone or '',
            request.litter_code,
            request.status,
            request.rejection_reason or '',
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
    # Honeypot validation - reject if the hidden field is filled (bot detection)
    if request.website:
        raise HTTPException(
            status_code=400, detail="Invalid submission detected.")

    if not request.terms_agreed:
        raise HTTPException(
            status_code=400, detail="You must read and agree to the terms to submit an adoption request.")

    if not request.privacy_consent:
        raise HTTPException(
            status_code=400, detail="You must consent to the privacy policy to submit an adoption request.")

    # Convert custom_answers dict to JSON string for storage
    import json
    custom_answers_json = json.dumps(request.custom_answers)

    db_request = AdoptionRequest(
        customer_email=request.customer_email,
        customer_name=request.customer_name,
        phone=request.phone,
        litter_code=request.litter_code,
        custom_answers=custom_answers_json,
        terms_agreed=request.terms_agreed,
        privacy_consent=request.privacy_consent,
        subscription=request.subscription
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    # Send email notification to admin
    try:
        await send_adoption_email_notification(db_request, request.custom_answers, db)
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        # Don't fail the request if email fails

    return {"message": "Adoption request submitted successfully", "request_id": db_request.id}


@router.get("/form", response_model=List[AdoptionQuestionResponse])
async def get_adoption_form(db: Session = Depends(get_db)):
    """Get questions for the adoption form."""
    questions = db.query(AdoptionQuestion).order_by(
        AdoptionQuestion.display_order).all()
    return questions


@router.get("/questions/", response_model=List[AdoptionQuestionResponse])
async def get_adoption_questions(db: Session = Depends(get_db)):
    questions = db.query(AdoptionQuestion).order_by(
        AdoptionQuestion.display_order).all()
    return questions


@router.post("/questions/", response_model=AdoptionQuestionResponse)
async def create_adoption_question(question: AdoptionQuestionCreate, db: Session = Depends(get_db)):
    db_question = AdoptionQuestion(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.get("/questions/{question_id}", response_model=AdoptionQuestionResponse)
async def get_adoption_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(AdoptionQuestion).filter(
        AdoptionQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.put("/questions/{question_id}", response_model=AdoptionQuestionResponse)
async def update_adoption_question(question_id: int, question: AdoptionQuestionUpdate, db: Session = Depends(get_db)):
    db_question = db.query(AdoptionQuestion).filter(
        AdoptionQuestion.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    update_data = question.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)
    return db_question


@router.delete("/questions/{question_id}")
async def delete_adoption_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(AdoptionQuestion).filter(
        AdoptionQuestion.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(db_question)
    db.commit()
    return {"message": "Question deleted successfully"}


@router.post("/questions/renumber")
async def renumber_questions(db: Session = Depends(get_db)):
    """Renumber all questions sequentially starting from 0."""
    questions = db.query(AdoptionQuestion).order_by(
        AdoptionQuestion.display_order, AdoptionQuestion.id).all()

    for i, question in enumerate(questions):
        question.display_order = i

    db.commit()
    return {"message": f"Renumbered {len(questions)} questions"}
