#!/usr/bin/env python3
"""
Script to update cat photos with working URLs
"""
from app.database import SessionLocal
from app.models.cat import Cat


def update_cat_photos():
    db = SessionLocal()

    # Better photo URLs using different services
    photo_updates = {
        "LUNA": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=400&fit=crop&crop=faces",
        "MILO": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=400&fit=crop&crop=faces",
        "BELLA": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=400&fit=crop&crop=faces",
        "OLIVER": "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?w=400&h=400&fit=crop&crop=faces",
        "BOT": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=400&fit=crop&crop=faces",
        "BATYA": "https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=400&h=400&fit=crop&crop=faces"
    }

    # Update each cat's photo
    for cat_name, photo_url in photo_updates.items():
        cat = db.query(Cat).filter(Cat.name == cat_name).first()
        if cat:
            cat.photo_url = photo_url
            print(f"Updated {cat_name}'s photo")
        else:
            print(f"Cat {cat_name} not found")

    db.commit()
    db.close()
    print("✅ Cat photos updated successfully!")


if __name__ == "__main__":
    update_cat_photos()
