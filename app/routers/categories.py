from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import Category, CategoryCreate, CategoryUpdate
from app.services import category_service

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[Category])
def list_categories(db: Session = Depends(get_db)):
    return category_service.get_all(db)


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = category_service.get_by_id(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Kategori hittades inte")
    return cat


@router.post("", response_model=Category, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create(db, data)


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    cat = category_service.update(db, category_id, data)
    if not cat:
        raise HTTPException(status_code=404, detail="Kategori hittades inte")
    return cat
