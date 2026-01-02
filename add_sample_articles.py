#!/usr/bin/env python3
"""
Script to add sample articles to the database for testing the article system.
"""

from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.article import Article

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Sample articles
    sample_articles = [
        {
            "title": "Welcome to LavanderCats Cattery!",
            "content": """Welcome to LavanderCats Cattery, your premier destination for beautiful Siberian cats!

Our cattery is dedicated to breeding healthy, happy, and well-socialized Siberian cats. We believe in ethical breeding practices and prioritize the health and well-being of our cats above all else.

Our Siberian cats are known for their stunning blue eyes, luxurious triple coat, and affectionate personalities. Whether you're looking for a new family member or a show-quality cat, we have something special for everyone.

Visit us to meet our current litter of kittens and learn more about the wonderful world of Siberian cats!""",
            "author": "LavanderCats Team",
            "featured_image": "",
            "published": True
        },
        {
            "title": "Siberian Cat Care Guide",
            "content": """Taking care of a Siberian cat is a rewarding experience. Here's what you need to know:

**Grooming:**
Siberian cats have a luxurious triple coat that requires regular brushing (2-3 times per week) to prevent matting and reduce shedding. They are semi-longhaired cats with a dense undercoat.

**Diet:**
Feed your Siberian a high-quality cat food appropriate for their age and activity level. They tend to be active cats, so they may need more calories than sedentary breeds.

**Health:**
Siberian cats are generally healthy, but regular veterinary check-ups are essential. Watch for signs of hypertrophic cardiomyopathy, which can affect some cats.

**Personality:**
Siberians are known for being affectionate, intelligent, and playful. They often form strong bonds with their owners and enjoy interactive play.

Remember, every cat is unique, so observe your cat's individual needs and preferences!""",
            "author": "LavanderCats Team",
            "featured_image": "",
            "published": True
        },
        {
            "title": "New Kitten Arrivals - Spring 2025",
            "content": """We're excited to announce the arrival of our newest litter of Siberian kittens!

Born on March 15th, 2025, this beautiful litter consists of:
- 3 stunning blue-eyed kittens
- 2 classic Siberian tabby patterns
- 1 rare solid color kitten

All kittens come from championship bloodlines and will be ready for their new homes starting May 2025. Each kitten will be:
- Fully vaccinated
- Microchipped
- Vet checked
- Socialized with children and other pets

If you're interested in reserving a kitten from this litter, please contact us as soon as possible. Spaces fill up quickly!

We also have several adult cats available for adoption, including some beautiful adults from previous litters.""",
            "author": "LavanderCats Team",
            "featured_image": "",
            "published": True
        },
        {
            "title": "Cat Health Tips for New Owners",
            "content": """Congratulations on your new cat! Here are some essential health tips to keep your feline friend happy and healthy:

**Vaccinations:**
Keep up with your cat's vaccination schedule. Core vaccines include rabies, feline distemper, and feline leukemia.

**Dental Care:**
Cats need regular dental care. Brush their teeth 2-3 times per week and provide dental treats.

**Weight Management:**
Monitor your cat's weight and body condition. Obesity can lead to many health problems.

**Parasite Prevention:**
Use flea and heartworm prevention year-round, even for indoor cats.

**Regular Check-ups:**
Schedule annual veterinary visits for wellness exams and early disease detection.

**Emergency Kit:**
Keep a pet first aid kit handy with bandages, antiseptic, and your vet's contact information.

Remember, prevention is the best medicine! A healthy lifestyle now means fewer vet visits later.""",
            "author": "Dr. Michael Chen",
            "featured_image": "",
            "published": False  # This is a draft
        }
    ]

    # Add articles to database
    for article_data in sample_articles:
        article = Article(**article_data)
        db.add(article)

    db.commit()
    print(f"✅ Successfully added {len(sample_articles)} sample articles!")

    # Print summary
    articles = db.query(Article).all()
    published = sum(1 for a in articles if a.published)
    drafts = sum(1 for a in articles if not a.published)

    print(f"📊 Database now contains:")
    print(f"   • {len(articles)} total articles")
    print(f"   • {published} published articles")
    print(f"   • {drafts} draft articles")

except Exception as e:
    print(f"❌ Error adding sample articles: {e}")
    db.rollback()

finally:
    db.close()
