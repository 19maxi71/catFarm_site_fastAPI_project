#!/usr/bin/env python3
"""
Script to add sample gallery images to existing articles for testing the gallery functionality.
"""

import base64
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.article import Article, ArticleImage

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Get the first published article
    article = db.query(Article).filter(Article.published == True).first()

    if not article:
        print("No published articles found. Please run add_sample_articles.py first.")
        exit(1)

    print(f"Adding gallery images to article: {article.title}")

    # Sample base64 encoded images (using placeholder images)
    # These are small colored squares for testing purposes
    sample_images = [
        {
            "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5/hHgAHggJ/lcYLQAAAABJRU5ErkJggg==",  # Red square
            "caption": "Beautiful Siberian kitten",
            "display_order": 0
        },
        {
            "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",  # Green square
            "caption": "Cat enjoying the sunshine",
            "display_order": 1
        },
        {
            "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",   # Blue square
            "caption": "Playful cat with toys",
            "display_order": 2
        }
    ]

    # Add gallery images to the article
    for img_data in sample_images:
        article_image = ArticleImage(
            article_id=article.id,
            image_path="",  # Empty since we're using base64
            image_base64=img_data["image_base64"],
            caption=img_data["caption"],
            display_order=img_data["display_order"]
        )
        db.add(article_image)

    db.commit()
    print(f"Added {len(sample_images)} gallery images to article '{article.title}'")

except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()
