#!/usr/bin/env python3
"""
Fix images for Render deployment by updating database paths to use persistent static images
instead of ephemeral uploaded images.
"""

from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.cat import Cat
from app.models.article import Article

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def fix_cat_images():
    """Update cat images to use persistent static files"""
    cats = db.query(Cat).all()

    # Map of sample image files (you'll need to add these to static/images/)
    sample_images = [
        "/static/images/sample_cat_1.jpg",
        "/static/images/sample_cat_2.jpg",
        "/static/images/sample_cat_3.jpg",
        "/static/images/logo.png"  # Fallback to existing logo
    ]

    for i, cat in enumerate(cats):
        if cat.photo_url and "/uploads/" in cat.photo_url:
            # Replace with persistent static image
            new_image = sample_images[i % len(sample_images)]
            cat.photo_url = new_image
            print(f"Updated {cat.name}: {new_image}")

    db.commit()
    print(f"✅ Updated {len(cats)} cat images")


def fix_article_images():
    """Update article images to use persistent static files"""
    articles = db.query(Article).all()

    sample_article_images = [
        "/static/images/logo.png",  # Use logo as placeholder
    ]

    for i, article in enumerate(articles):
        if article.featured_image and "/uploads/" in article.featured_image:
            # Replace with persistent static image
            new_image = sample_article_images[0]  # Use logo for now
            article.featured_image = new_image
            print(f"Updated article '{article.title}': {new_image}")

    db.commit()
    print(f"✅ Updated {len(articles)} article images")


if __name__ == "__main__":
    print("🔧 Fixing images for Render deployment...")
    try:
        fix_cat_images()
        fix_article_images()
        print("🎉 All images updated to use persistent static files!")
        print("\n📝 Note: Add sample images to static/images/ directory for better visuals")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()
