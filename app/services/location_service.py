from sqlalchemy.orm import Session, joinedload
from app.models.models import Drawer, Compartment, Stock, Component
from app.schemas.schemas import DrawerCreate, CompartmentCreate, CompartmentUpdate


def get_all_drawers(db: Session) -> list[Drawer]:
    return db.query(Drawer).order_by(Drawer.label).all()


def get_drawer(db: Session, drawer_id: int) -> Drawer | None:
    return (
        db.query(Drawer)
        .options(
            joinedload(Drawer.compartments)
                .joinedload(Compartment.stock)
                .joinedload(Stock.component),
            joinedload(Drawer.files),
        )
        .filter(Drawer.id == drawer_id)
        .first()
    )


def create_drawer(db: Session, data: DrawerCreate) -> Drawer:
    drawer = Drawer(**data.model_dump())
    db.add(drawer)
    db.commit()
    db.refresh(drawer)
    return drawer


def get_compartment(db: Session, compartment_id: int) -> Compartment | None:
    return (
        db.query(Compartment)
        .options(joinedload(Compartment.stock))
        .filter(Compartment.id == compartment_id)
        .first()
    )


def create_compartment(db: Session, data: CompartmentCreate) -> Compartment:
    compartment = Compartment(**data.model_dump())
    db.add(compartment)
    db.commit()
    db.refresh(compartment)
    return compartment


def update_compartment(db: Session, compartment_id: int, data: CompartmentUpdate) -> Compartment | None:
    compartment = db.query(Compartment).filter(Compartment.id == compartment_id).first()
    if not compartment:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(compartment, field, value)
    db.commit()
    db.refresh(compartment)
    return compartment
