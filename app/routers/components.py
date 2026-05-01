from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import Component, ComponentCreate, ComponentUpdate, ComponentSummary
from app.services import component_service

router = APIRouter(prefix="/api/components", tags=["components"])


@router.get("", response_model=list[ComponentSummary])
def list_components(
    q: str | None = None,
    category_id: str | None = Query(default=None),
    in_stock: bool | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    cat_id = int(category_id) if category_id else None
    return component_service.get_all(db, q=q, category_id=cat_id, in_stock=in_stock, skip=skip, limit=limit)


@router.get("/{component_id}", response_model=Component)
def get_component(component_id: int, db: Session = Depends(get_db)):
    comp = component_service.get_by_id(db, component_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Komponent hittades inte")
    return comp


@router.post("", response_model=Component, status_code=201)
def create_component(data: ComponentCreate, db: Session = Depends(get_db)):
    return component_service.create(db, data)


@router.put("/{component_id}", response_model=Component)
def update_component(component_id: int, data: ComponentUpdate, db: Session = Depends(get_db)):
    comp = component_service.update(db, component_id, data)
    if not comp:
        raise HTTPException(status_code=404, detail="Komponent hittades inte")
    return comp


@router.delete("/{component_id}", status_code=204)
def delete_component(component_id: int, db: Session = Depends(get_db)):
    if not component_service.delete(db, component_id):
        raise HTTPException(status_code=404, detail="Komponent hittades inte")
