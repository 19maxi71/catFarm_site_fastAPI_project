from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.article import Article, ArticleImage
from ..schemas.article import ArticleImageResponse, CreateArticleImageRequest
from ..photo_utils import save_uploaded_photo
from typing import List
import shutil
import os

router = APIRouter()


@router.get("/articles/{article_id}/images/", response_model=List[ArticleImageResponse])
async def get_article_images(article_id: int, db: Session = Depends(get_db)) -> List[ArticleImageResponse]:
    """Get all images for a specific article."""
    images = db.query(ArticleImage).filter(
        ArticleImage.article_id == article_id).order_by(ArticleImage.display_order).all()

    # Format image URLs for proper display
    for image in images:
        if image.image_path and not image.image_path.startswith(('http://', 'https://')):
            image.image_path = f"/static/{image.image_path}"

    return images


@router.post("/articles/{article_id}/images/", response_model=ArticleImageResponse)
async def upload_article_image(
    article_id: int,
    file: UploadFile = File(...),
    caption: str = Form(None),
    display_order: int = Form(0),
    db: Session = Depends(get_db)
):
    """Upload an image for a specific article."""
    # Check if article exists
    from ..models.article import Article
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    try:
        # Save the uploaded photo
        full_path, thumb_path = await save_uploaded_photo(file, f"article_{article_id}", article_image=True)

        # Create ArticleImage record
        article_image = ArticleImage(
            article_id=article_id,
            image_path=full_path,
            caption=caption,
            display_order=display_order
        )

        db.add(article_image)
        db.commit()
        db.refresh(article_image)

        # Format URL for response
        article_image.image_path = f"/static/{article_image.image_path}"

        return article_image

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error uploading image: {str(e)}")


@router.post("/articles/{article_id}/images/clear/")
async def clear_article_images(article_id: int, db: Session = Depends(get_db)):
    """Clear all images for a specific article."""
    # Check if article exists
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    try:
        # Get all images for this article
        images = db.query(ArticleImage).filter(
            ArticleImage.article_id == article_id).all()

        # Delete physical files
        for image in images:
            try:
                if os.path.exists(f"static/{image.image_path}"):
                    os.remove(f"static/{image.image_path}")
            except Exception as e:
                print(
                    f"Warning: Could not delete file {image.image_path}: {e}")

        # Delete from database
        db.query(ArticleImage).filter(
            ArticleImage.article_id == article_id).delete()
        db.commit()

        return {"message": f"Cleared {len(images)} images for article {article_id}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error clearing images: {str(e)}")


@router.post("/articles/{article_id}/images/associate/", response_model=ArticleImageResponse)
async def associate_existing_image(
    article_id: int,
    image_data: CreateArticleImageRequest,
    db: Session = Depends(get_db)
):
    """Associate an existing uploaded image with an article."""
    # Check if article exists
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    try:
        # Create ArticleImage record with existing image path
        article_image = ArticleImage(
            article_id=article_id,
            image_path=image_data.image_path,
            caption=image_data.caption,
            display_order=image_data.display_order
        )

        db.add(article_image)
        db.commit()
        db.refresh(article_image)

        # Format URL for response
        if article_image.image_path and not article_image.image_path.startswith(('http://', 'https://')):
            article_image.image_path = f"/static/{article_image.image_path}"

        return article_image

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error associating image: {str(e)}")


@router.delete("/articles/{article_id}/images/{image_id}")
async def delete_article_image(article_id: int, image_id: int, db: Session = Depends(get_db)):
    """Delete an article image."""
    image = db.query(ArticleImage).filter(
        ArticleImage.id == image_id,
        ArticleImage.article_id == article_id
    ).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Delete the physical file
    try:
        if os.path.exists(f"static/{image.image_path}"):
            os.remove(f"static/{image.image_path}")
    except Exception as e:
        print(f"Warning: Could not delete file {image.image_path}: {e}")

    # Delete from database
    db.delete(image)
    db.commit()

    return {"message": "Image deleted successfully"}
