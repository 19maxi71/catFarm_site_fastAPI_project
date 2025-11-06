#!/usr/bin/env python3
"""
Script to add sample adoption requests to the database for testing
"""
from app.database import SessionLocal
from app.models.adoption import AdoptionRequest
import json
from datetime import datetime, timezone

def add_sample_adoption_requests():
    db = SessionLocal()

    # Sample adoption requests
    sample_requests = [
        {
            "customer_email": "john.doe@example.com",
            "customer_name": "John Doe",
            "phone": "+1-555-0123",
            "custom_answers": json.dumps({
                "1": "Yes, I have owned cats before",
                "2": "House",
                "3": "Yes",
                "4": "Less than 4 hours"
            }),
            "terms_agreed": True,
            "subscription": True,
            "status": "pending"
        },
        {
            "customer_email": "jane.smith@example.com",
            "customer_name": "Jane Smith",
            "phone": "+1-555-0124",
            "custom_answers": json.dumps({
                "1": "No, this would be my first cat",
                "2": "Apartment",
                "3": "No",
                "4": "4-8 hours"
            }),
            "terms_agreed": True,
            "subscription": False,
            "status": "approved"
        },
        {
            "customer_email": "mike.johnson@example.com",
            "customer_name": "Mike Johnson",
            "phone": None,
            "custom_answers": json.dumps({
                "1": "I have cared for cats but never owned one",
                "2": "Condo",
                "3": "Yes",
                "4": "8-12 hours"
            }),
            "terms_agreed": True,
            "subscription": True,
            "status": "pending"
        },
        {
            "customer_email": "sarah.wilson@example.com",
            "customer_name": "Sarah Wilson",
            "phone": "+1-555-0126",
            "custom_answers": json.dumps({
                "1": "Yes, I have owned cats before",
                "2": "House",
                "3": "No",
                "4": "Less than 4 hours"
            }),
            "terms_agreed": True,
            "subscription": False,
            "status": "rejected"
        }
    ]

    # Add each request to database
    for request_data in sample_requests:
        # Check if request already exists (by email)
        existing_request = db.query(AdoptionRequest).filter(AdoptionRequest.customer_email == request_data["customer_email"]).first()
        if not existing_request:
            new_request = AdoptionRequest(**request_data)
            db.add(new_request)
            print(f"Added adoption request for: {request_data['customer_name']} ({request_data['customer_email']}) - Status: {request_data['status']}")
        else:
            print(f"Adoption request already exists for: {request_data['customer_name']} ({request_data['customer_email']}), skipping...")

    db.commit()
    db.close()
    print("✅ Sample adoption requests added successfully!")

if __name__ == "__main__":
    add_sample_adoption_requests()
