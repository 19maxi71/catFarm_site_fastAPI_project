from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.cat import Cat
from ..schemas.cat import CatSerializer, CreateCatRequest, CatApiResponse
from typing import List

router = APIRouter()

@router.get("/cats/", response_model=List[CatApiResponse]) # Get all cats
async def get_all_cats(db: Session = Depends(get_db)) -> List[CatApiResponse]:
    cats = db.query(Cat).all()
    return cats
