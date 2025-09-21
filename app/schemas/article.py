from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ArticleImageSerializer(BaseModel):
    image_path: str  # DEPRECATED - kept for compatibility
    image_base64: Optional[str] = None  # Base64 encoded image data
    caption: Optional[str] = None
    display_order: int = 0


class CreateArticleImageRequest(ArticleImageSerializer):
    pass


class ArticleImageResponse(ArticleImageSerializer):
    id: int
    article_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ArticleSerializer(BaseModel):
    title: str
    content: str
    author: str = "Admin"
    published: bool = False
    featured_image: Optional[str] = None  # DEPRECATED - kept for compatibility
    featured_image_base64: Optional[str] = None  # Base64 encoded featured image


class CreateArticleRequest(ArticleSerializer):
    pass


class ArticleApiResponse(ArticleSerializer):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        # Allows using SQLAlchemy ORM objects directly
