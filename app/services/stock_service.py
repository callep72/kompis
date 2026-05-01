from sqlalchemy.orm import Session, joinedload
from app.models.models import Stock
from app.schemas.schemas import StockCreate, StockUpdate


def get_all(db: Session, low_stock: bool = False) -> list[Stock]:
    q = db.query(Stock).options(
        joinedload(Stock.component),
        joinedload(Stock.compartment),
    )
    if low_stock:
        q = q.filter(Stock.quantity <= Stock.minimum_qty, Stock.minimum_qty > 0)
    return q.all()


def get_by_id(db: Session, stock_id: int) -> Stock | None:
    return db.query(Stock).filter(Stock.id == stock_id).first()


def create(db: Session, data: StockCreate) -> Stock:
    stock = Stock(**data.model_dump())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


def update(db: Session, stock_id: int, data: StockUpdate) -> Stock | None:
    stock = get_by_id(db, stock_id)
    if not stock:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(stock, field, value)
    db.commit()
    db.refresh(stock)
    return stock
