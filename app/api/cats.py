from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.cat import Cat
from ..schemas.cat import CatSerializer, CreateCatRequest, CatApiResponse
from typing import List

router = APIRouter()


@router.get("/cats/", response_model=List[CatApiResponse])  # Get all cats
async def get_all_cats(db: Session = Depends(get_db)) -> List[CatApiResponse]:
    cats = db.query(Cat).all()
    # Format photo URLs for proper display
    for cat in cats:
        if cat.photo_url and not cat.photo_url.startswith(('http://', 'https://')):
            cat.photo_url = f"/static/{cat.photo_url}"
    return cats


@router.post("/cats/", response_model=CatApiResponse)
async def create_cat(cat_data: CreateCatRequest, db: Session = Depends(get_db)) -> CatApiResponse:
    # Unpack dictionary to keyword arguments
    new_cat = Cat(**cat_data.model_dump())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


@router.get("/cats/{cat_id}", response_model=CatApiResponse)
async def get_cat(cat_id: int, db: Session = Depends(get_db)) -> CatApiResponse:
    cat = db.query(Cat).filter(Cat.id == cat_id).first()

    if not cat:
        raise HTTPException(
            status_code=404, detail="Cat not found, provide a valid id")

    return cat


@router.put("/cats/{cat_id}", response_model=CatApiResponse)
async def update_cat(cat_id: int, cat_data: CreateCatRequest, db: Session = Depends(get_db)) -> CatApiResponse:
    cat = db.query(Cat).filter(Cat.id == cat_id).first()

    if not cat:
        raise HTTPException(
            status_code=404, detail="Cat not found, provide a valid id")

    # Update cat fields
    for key, value in cat_data.model_dump().items():
        setattr(cat, key, value)

    # Save changes
    db.commit()
    db.refresh(cat)
    return cat


# Delete a cat, no need of 'response_model' since returs simple message, don't need to validate through Pydantic schemas
@router.delete("/cats/{cat_id}")
async def delete_cat(cat_id: int, db: Session = Depends(get_db)) -> dict:
    cat = db.query(Cat).filter(Cat.id == cat_id).first()

    if not cat:
        raise HTTPException(
            status_code=404, detail="Cat not found, provide a valid id")

    db.delete(cat)
    db.commit()
    return {"message": "Cat deleted"}
