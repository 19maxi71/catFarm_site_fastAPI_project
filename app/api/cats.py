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

@router.post("/cats/", response_model=CatApiResponse)
async def create_cat(cat_data: CreateCatRequest, db: Session = Depends(get_db))->CatApiResponse:
    new_cat = Cat(**cat_data.dict())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat
