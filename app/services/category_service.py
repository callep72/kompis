from sqlalchemy.orm import Session
from app.models.models import Category
from app.schemas.schemas import CategoryCreate, CategoryUpdate


def get_all(db: Session) -> list[Category]:
    return db.query(Category).all()


def get_by_id(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def create(db: Session, data: CategoryCreate) -> Category:
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update(db: Session, category_id: int, data: CategoryUpdate) -> Category | None:
    category = get_by_id(db, category_id)
    if not category:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category
