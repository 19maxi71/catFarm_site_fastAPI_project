from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(50), default="Admin")
    featured_image = Column(String(500), nullable=True)  # DEPRECATED - use featured_image_base64
    featured_image_base64 = Column(Text, nullable=True)  # Base64 encoded featured image
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to ArticleImage
    images = relationship(
        "ArticleImage", back_populates="article", cascade="all, delete-orphan")

    def __repr__(self):  # Transforms the object into a string (for debugging)
        return f'Article(id={self.id}, title={self.title}, published={self.published})'


class ArticleImage(Base):
    __tablename__ = "article_images"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    image_path = Column(String(500), nullable=False)  # DEPRECATED - use image_base64
    image_base64 = Column(Text, nullable=True)  # Base64 encoded image data
    caption = Column(String(200), nullable=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to Article
    article = relationship("Article", back_populates="images")

    def __repr__(self):
        return f'ArticleImage(id={self.id}, article_id={self.article_id}, image_path={self.image_path})'
