from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
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

    # Format image URLs for proper display (backward compatibility)
    for image in images:
        if image.image_path and not image.image_path.startswith(('http://', 'https://', '/static/')):
            image.image_path = f"/static/{image.image_path}"
        # Ensure base64 images are properly formatted
        if image.image_base64 and not image.image_base64.startswith('data:'):
            image.image_base64 = f"data:image/jpeg;base64,{image.image_base64}"

    return images


@router.post("/articles/{article_id}/images/", response_model=ArticleImageResponse)
async def upload_article_image(
    article_id: int,
    request: Request,
    file: UploadFile = File(None),
    image_base64: str = Form(None),
    caption: str = Form(None),
    display_order: int = Form(0),
    db: Session = Depends(get_db)
):
    """Upload an image for a specific article."""
    # Check if article exists
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Handle JSON requests (for base64 data)
    if request.headers.get('content-type') == 'application/json':
        try:
            json_data = await request.json()
            image_base64 = json_data.get('image_base64')
            caption = json_data.get('caption', '')
            display_order = json_data.get('display_order', 0)
            image_path = json_data.get('image_path', '')
        except:
            raise HTTPException(status_code=400, detail="Invalid JSON data")
    else:
        # Handle form data (for file uploads)
        image_path = ""

    try:
        base64_data = image_base64

        # If no base64 provided, convert uploaded file
        if not base64_data and file:
            from ..photo_utils import convert_image_to_base64
            base64_data = await convert_image_to_base64(file)

            # Also save to filesystem for backward compatibility (if needed)
            try:
                from ..photo_utils import save_uploaded_photo
                full_path, thumb_path = await save_uploaded_photo(file, f"article_{article_id}", article_image=True)
                image_path = full_path
            except:
                # If file save fails, still return base64 (this is for Render compatibility)
                image_path = ""
        elif not base64_data and not file:
            raise HTTPException(status_code=400, detail="No image data provided")

        # Create ArticleImage record
        article_image = ArticleImage(
            article_id=article_id,
            image_path=image_path,
            image_base64=base64_data,
            caption=caption,
            display_order=display_order
        )

        db.add(article_image)
        db.commit()
        db.refresh(article_image)

        # Format URL for response
        if article_image.image_path:
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
        # Create ArticleImage record with existing image path and base64
        article_image = ArticleImage(
            article_id=article_id,
            image_path=image_data.image_path,
            image_base64=image_data.image_base64,
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
