from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.article import Article
from ..schemas.article import CreateArticleRequest, ArticleApiResponse
from typing import List

router = APIRouter()


@router.get("/test")
async def test_endpoint(db: Session = Depends(get_db)):
    try:
        count = db.query(Article).count()
        return {"message": f"Database working, {count} articles"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/articles/", response_model=List[ArticleApiResponse])
async def get_all_articles(db: Session = Depends(get_db)) -> List[ArticleApiResponse]:
    articles = db.query(Article).filter(Article.published ==
                                        True).order_by(Article.created_at.desc()).all()

    # Format photo URLs for proper display (backward compatibility)
    for article in articles:
        if article.featured_image and not article.featured_image.startswith(('http://', 'https://', '/static/')):
            article.featured_image = f"/static/{article.featured_image}"
        # Ensure base64 images are properly formatted
        if article.featured_image_base64 and not article.featured_image_base64.startswith('data:'):
            article.featured_image_base64 = f"data:image/jpeg;base64,{article.featured_image_base64}"

    return articles


@router.post("/articles/", response_model=ArticleApiResponse)
async def create_article(article_data: CreateArticleRequest, db: Session = Depends(get_db)) -> ArticleApiResponse:
    new_article = Article(**article_data.model_dump())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.get("/articles/{article_id}", response_model=ArticleApiResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)) -> ArticleApiResponse:
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(
            status_code=404, detail="Article not found, provide a valid id")

    # Format photo URL for proper display
    if article.featured_image and not article.featured_image.startswith(('http://', 'https://')):
        article.featured_image = f"/static/{article.featured_image}"

    return article


@router.put("/articles/{article_id}", response_model=ArticleApiResponse)
async def update_article(article_id: int, article_data: CreateArticleRequest, db: Session = Depends(get_db)) -> ArticleApiResponse:
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(
            status_code=404, detail="Article not found, provide a valid id")

    # Update article fields
    update_data = article_data.model_dump(exclude_unset=True)

    # Ensure featured_image is stored as relative path
    if 'featured_image' in update_data and update_data['featured_image'] and update_data['featured_image'].startswith('/static/'):
        update_data['featured_image'] = update_data['featured_image'].replace(
            '/static/', '', 1)

    for key, value in update_data.items():
        setattr(article, key, value)

    # Save changes
    db.commit()
    db.refresh(article)
    return article


# Delete an article, no need of 'response_model' since returs simple message, don't need to validate through Pydantic schemas
@router.delete("/articles/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)) -> dict:
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(
            status_code=404, detail="Article not found, provide a valid id")

    db.delete(article)
    db.commit()
    return {"message": "Article deleted"}
