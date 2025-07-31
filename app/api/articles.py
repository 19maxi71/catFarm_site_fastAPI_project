from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.article import Article
from ..schemas.article import CreateArticleRequest, ArticleApiResponse
from typing import List

router = APIRouter()


@router.get("/articles/", response_model=List[ArticleApiResponse])  # Fixed
async def get_all_articles(db: Session = Depends(get_db)) -> List[ArticleApiResponse]:
    articles = db.query(Article).all()
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

    return article


@router.put("/articles/{article_id}", response_model=ArticleApiResponse)
async def update_article(article_id: int, article_data: CreateArticleRequest, db: Session = Depends(get_db)) -> ArticleApiResponse:
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(
            status_code=404, detail="Article not found, provide a valid id")

    # Update article fields
    for key, value in article_data.model_dump().items():
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
