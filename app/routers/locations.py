from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import (
    Drawer, DrawerCreate, DrawerWithCompartments,
    Compartment, CompartmentCreate, CompartmentUpdate, CompartmentWithStock,
)
from app.services import location_service

router = APIRouter(tags=["locations"])


@router.get("/api/drawers", response_model=list[Drawer])
def list_drawers(db: Session = Depends(get_db)):
    return location_service.get_all_drawers(db)


@router.get("/api/drawers/{drawer_id}", response_model=DrawerWithCompartments)
def get_drawer(drawer_id: int, db: Session = Depends(get_db)):
    drawer = location_service.get_drawer(db, drawer_id)
    if not drawer:
        raise HTTPException(status_code=404, detail="Låda hittades inte")
    return drawer


@router.post("/api/drawers", response_model=Drawer, status_code=201)
def create_drawer(data: DrawerCreate, db: Session = Depends(get_db)):
    return location_service.create_drawer(db, data)


@router.get("/api/compartments/{compartment_id}", response_model=CompartmentWithStock)
def get_compartment(compartment_id: int, db: Session = Depends(get_db)):
    comp = location_service.get_compartment(db, compartment_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Fack hittades inte")
    return comp


@router.post("/api/compartments", response_model=Compartment, status_code=201)
def create_compartment(data: CompartmentCreate, db: Session = Depends(get_db)):
    return location_service.create_compartment(db, data)


@router.put("/api/compartments/{compartment_id}", response_model=Compartment)
def update_compartment(compartment_id: int, data: CompartmentUpdate, db: Session = Depends(get_db)):
    comp = location_service.update_compartment(db, compartment_id, data)
    if not comp:
        raise HTTPException(status_code=404, detail="Fack hittades inte")
    return comp
