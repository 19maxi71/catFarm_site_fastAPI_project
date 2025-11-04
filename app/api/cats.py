from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from ..models.cat import Cat
from ..schemas.cat import CatSerializer, CreateCatRequest, CatApiResponse
from typing import List

router = APIRouter()


@router.get("/cats/", response_model=List[CatApiResponse])  # Get all cats
async def get_all_cats(db: Session = Depends(get_db)) -> List[CatApiResponse]:
    cats = db.query(Cat).all()
    # Format photo URLs for proper display (backward compatibility)
    for cat in cats:
        if cat.photo_url and not cat.photo_url.startswith(('http://', 'https://')):
            cat.photo_url = f"/static/{cat.photo_url}"
        # Ensure base64 images are properly formatted
        if cat.photo_base64 and not cat.photo_base64.startswith('data:'):
            cat.photo_base64 = f"data:image/jpeg;base64,{cat.photo_base64}"
    return cats


@router.post("/cats/")
async def create_cat(cat_data: CreateCatRequest, db: Session = Depends(get_db)):
    # Unpack dictionary to keyword arguments
    new_cat = Cat(**cat_data.model_dump())
    try:
        db.add(new_cat)
        db.commit()
        # Return as dict to avoid serialization issues
        result = {
            "id": new_cat.id,
            "name": new_cat.name,
            "gender": new_cat.gender,
            "litter_code": new_cat.litter_code,
            "date_of_birth": new_cat.date_of_birth,
            "description": new_cat.description,
            "photo_url": new_cat.photo_url,
            "photo_base64": new_cat.photo_base64,
            "is_available": new_cat.is_available,
        }
        if new_cat.created_at:
            result["created_at"] = new_cat.created_at
        if new_cat.updated_at:
            result["updated_at"] = new_cat.updated_at
        return result
    except IntegrityError as e:
        db.rollback()
        if "litter_code" in str(e):
            raise HTTPException(status_code=400, detail="Litter code already exists. Please choose a different litter code.")
        raise HTTPException(status_code=400, detail="A database constraint was violated.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the cat.")


@router.get("/cats/{cat_id}", response_model=CatApiResponse)
async def get_cat(cat_id: int, db: Session = Depends(get_db)) -> CatApiResponse:
    cat = db.query(Cat).filter(Cat.id == cat_id).first()

    if not cat:
        raise HTTPException(
            status_code=404, detail="Cat not found, provide a valid id")

    return cat


@router.put("/cats/{cat_id}", response_model=CatApiResponse)
async def update_cat(cat_id: int, cat_data: CreateCatRequest, db: Session = Depends(get_db)) -> CatApiResponse:
    from datetime import datetime, timezone
    cat = db.query(Cat).filter(Cat.id == cat_id).first()

    if not cat:
        raise HTTPException(
            status_code=404, detail="Cat not found, provide a valid id")

    # Update cat fields
    for key, value in cat_data.model_dump().items():
        setattr(cat, key, value)

    # Update timestamp manually
    cat.updated_at = datetime.now(timezone.utc)

    try:
        # Save changes
        db.commit()
        return cat
    except IntegrityError as e:
        db.rollback()
        if "litter_code" in str(e):
            raise HTTPException(status_code=400, detail="Litter code already exists. Please choose a different litter code.")
        raise HTTPException(status_code=400, detail="A database constraint was violated.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the cat.")


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
