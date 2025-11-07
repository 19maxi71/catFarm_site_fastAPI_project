🐱 Adoption Request
Ready to welcome a Siberian cat into your home? Please fill out this form so we can learn more about you and ensure the best match.

Contact Information
Email Address *
vtr03@tutamail.com
Full Name *
HUAREZ
Phone Number
Cat Selection
Which litter are you interested in? *

Litter L004
Additional Information
11111TEST111111 *
Why do you want to adopt a cat? *
What is your email address? *
DO YOU HAVE OTHER ANIMALS AT HOME? WHICH ONE? *
WHAT OTHER ANIMALS DO YOU HAVE AT HOME? *
Do you have experience with cats? *
What is your full name? *
What is your phone number?
Do you have any previous experience with cats? *

Select an option
Do you have any allergies to cats? *

Yes

No
What type of home do you live in? *

Select an option
What type of cat are you interested in? *

Select an option
How many hours per day will the cat be left alone? *

Select an option
Do you agree to provide regular veterinary care? *

Yes

No
Any additional comments or questions?

I have read and agree to the terms of adoption *

I consent to the collection and use of my personal information as described in the privacy policy *

Subscribe to updates about new kittens and farm news
Submit Adoption Request#!/usr/bin/env python3
"""
Script to add sample adoption questions to the database for testing
"""
from app.database import SessionLocal
from app.models.adoption import AdoptionQuestion

def add_sample_questions():
    db = SessionLocal()

    # Sample adoption questions
    sample_questions = [
        {
            "question_text": "What is your full name?",
            "question_type": "text",
            "options": None,
            "is_required": True,
            "order": 1
        },
        {
            "question_text": "What is your email address?",
            "question_type": "text",
            "options": None,
            "is_required": True,
            "order": 2
        },
        {
            "question_text": "What is your phone number?",
            "question_type": "text",
            "options": None,
            "is_required": False,
            "order": 3
        },
        {
            "question_text": "Do you have any previous experience with cats?",
            "question_type": "select",
            "options": "Yes, I have owned cats before\nNo, this would be my first cat\nI have cared for cats but never owned one",
            "is_required": True,
            "order": 4
        },
        {
            "question_text": "Do you have any allergies to cats?",
            "question_type": "checkbox",
            "options": None,
            "is_required": True,
            "order": 5
        },
        {
            "question_text": "What type of home do you live in?",
            "question_type": "select",
            "options": "House\nApartment\nCondo\nOther",
            "is_required": True,
            "order": 6
        },
        {
            "question_text": "Do you have a fenced yard?",
            "question_type": "checkbox",
            "options": None,
            "is_required": False,
            "order": 7
        },
        {
            "question_text": "How many hours per day will the cat be left alone?",
            "question_type": "select",
            "options": "Less than 4 hours\n4-8 hours\n8-12 hours\nMore than 12 hours",
            "is_required": True,
            "order": 8
        },
        {
            "question_text": "Do you agree to provide regular veterinary care?",
            "question_type": "checkbox",
            "options": None,
            "is_required": True,
            "order": 9
        },
        {
            "question_text": "Any additional comments or questions?",
            "question_type": "text",
            "options": None,
            "is_required": False,
            "order": 10
        }
    ]

    # Add each question to database
    for question_data in sample_questions:
        # Check if question already exists (by text)
        existing_question = db.query(AdoptionQuestion).filter(AdoptionQuestion.question_text == question_data["question_text"]).first()
        if not existing_question:
            new_question = AdoptionQuestion(**question_data)
            db.add(new_question)
            print(f"Added question: {question_data['question_text'][:50]}...")
        else:
            print(f"Question already exists: {question_data['question_text'][:50]}..., skipping...")

    db.commit()
    db.close()
    print("✅ Sample adoption questions added successfully!")

if __name__ == "__main__":
    add_sample_questions()
