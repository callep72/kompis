from sqlalchemy import cast, or_, and_, func, Text
from sqlalchemy.orm import Session, joinedload
from app.models.models import Component, Compartment, Stock
from app.schemas.schemas import ComponentCreate, ComponentUpdate


def get_all(
    db: Session,
    q: str | None = None,
    category_id: int | None = None,
    in_stock: bool | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Component]:
    query = db.query(Component).filter(Component.active == True)

    if q:
        words = [w for w in q.split() if len(w) > 1]
        conditions = [
            Component.search_vector.op("@@")(func.websearch_to_tsquery("swedish", q)),
            Component.name.ilike(f"%{q}%"),
            Component.part_number.ilike(f"%{q}%"),
            func.array_to_string(Component.tags, " ").ilike(f"%{q}%"),
            cast(Component.specs, Text).ilike(f"%{q}%"),
        ]
        if len(words) > 1:
            conditions.append(and_(*[
                or_(
                    Component.name.ilike(f"%{w}%"),
                    func.array_to_string(Component.tags, " ").ilike(f"%{w}%"),
                    cast(Component.specs, Text).ilike(f"%{w}%"),
                )
                for w in words
            ]))
        query = query.filter(or_(*conditions))

    if category_id is not None:
        query = query.filter(Component.category_id == category_id)

    if in_stock:
        query = query.filter(
            Component.stock.any(Stock.quantity > 0)
        )

    return (
        query.options(
            joinedload(Component.category),
            joinedload(Component.stock)
            .joinedload(Stock.compartment)
            .joinedload(Compartment.drawer),
        )
        .order_by(Component.name)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_id(db: Session, component_id: int) -> Component | None:
    return (
        db.query(Component)
        .options(
            joinedload(Component.category),
            joinedload(Component.stock).joinedload(Stock.compartment),
            joinedload(Component.files),
        )
        .filter(Component.id == component_id, Component.active == True)
        .first()
    )


def create(db: Session, data: ComponentCreate) -> Component:
    component = Component(**data.model_dump())
    db.add(component)
    db.commit()
    db.refresh(component)
    return component


def update(db: Session, component_id: int, data: ComponentUpdate) -> Component | None:
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(component, field, value)
    db.commit()
    db.refresh(component)
    return component


def delete(db: Session, component_id: int) -> bool:
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        return False
    component.active = False
    db.commit()
    return True
