from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.cat import Article
from ..schemas.cat import ArticleSerializer, CreateArticleRequest, ArticleApiResponse
from typing import List

router = APIRouter()

