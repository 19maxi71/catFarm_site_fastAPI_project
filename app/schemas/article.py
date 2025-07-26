from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ArticleSerializer(BaseModel):
    title: str
    content: str
    author: str = "Admin"
    published: bool = False
    featured_image: Optional[str] = None


class CreateArticleRequest(ArticleSerializer):
    pass

class ArticleApiResponse(ArticleSerializer):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        # Allows using SQLAlchemy ORM objects directly
