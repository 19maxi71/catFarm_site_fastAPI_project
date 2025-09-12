#!/usr/bin/env python3
"""
Script to add sample cats to the database for testing
"""
from app.database import SessionLocal
from app.models.cat import Cat

def add_sample_cats():
    db = SessionLocal()

    # Sample cats with real cat photos (using placeholder services)
    sample_cats = [
        {
            "name": "LUNA",
            "role": "queen",
            "breed": "Siberian",
            "bio": "Luna is a gentle and loving queen with the most beautiful blue eyes. She loves to sit by the window and watch birds.",
            "photo_url": "https://placekitten.com/400/400",
            "rabies_vaccinated": True,
            "award": "Best in Show 2024"
        },
        {
            "name": "MILO",
            "role": "kitten",
            "breed": "Siberian Mix",
            "bio": "Playful little Milo is always ready for an adventure! He loves toys and cuddling with his siblings.",
            "photo_url": "https://placekitten.com/401/401",
            "rabies_vaccinated": False,
            "award": None
        },
        {
            "name": "BELLA",
            "role": "queen",
            "breed": "Siberian",
            "bio": "Bella is the sweetest cat you'll ever meet. She purrs constantly and loves belly rubs.",
            "photo_url": "https://placekitten.com/402/402",
            "rabies_vaccinated": True,
            "award": "Most Affectionate Cat 2024"
        },
        {
            "name": "OLIVER",
            "role": "kitten",
            "breed": "Siberian",
            "bio": "Oliver is a curious little explorer who loves to climb and discover new hiding spots.",
            "photo_url": "https://placekitten.com/403/403",
            "rabies_vaccinated": False,
            "award": None
        }
    ]

    # Add each cat to database
    for cat_data in sample_cats:
        # Check if cat already exists
        existing_cat = db.query(Cat).filter(Cat.name == cat_data["name"]).first()
        if not existing_cat:
            new_cat = Cat(**cat_data)
            db.add(new_cat)
            print(f"Added {cat_data['name']} ({cat_data['role']})")
        else:
            print(f"{cat_data['name']} already exists, skipping...")

    db.commit()
    db.close()
    print("✅ Sample cats added successfully!")

if __name__ == "__main__":
    add_sample_cats()
