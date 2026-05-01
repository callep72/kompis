from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import Stock, StockCreate, StockUpdate, StockWithComponent
from app.services import stock_service

router = APIRouter(prefix="/api/stock", tags=["stock"])


@router.get("", response_model=list[StockWithComponent])
def list_stock(low_stock: bool = False, db: Session = Depends(get_db)):
    return stock_service.get_all(db, low_stock=low_stock)


@router.post("", response_model=Stock, status_code=201)
def create_stock(data: StockCreate, db: Session = Depends(get_db)):
    return stock_service.create(db, data)


@router.put("/{stock_id}", response_model=Stock)
def update_stock(stock_id: int, data: StockUpdate, db: Session = Depends(get_db)):
    stock = stock_service.update(db, stock_id, data)
    if not stock:
        raise HTTPException(status_code=404, detail="Lagerrad hittades inte")
    return stock
