from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


# --- Category ---

class CategoryBase(BaseModel):
    name: str
    slug: str
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[int] = None


class Category(CategoryBase):
    id: int
    children: list["Category"] = []

    model_config = {"from_attributes": True}


# --- Drawer ---

class DrawerBase(BaseModel):
    label: str
    description: Optional[str] = None


class DrawerCreate(DrawerBase):
    pass


class Drawer(DrawerBase):
    id: int

    model_config = {"from_attributes": True}


class DrawerWithCompartments(Drawer):
    compartments: list["Compartment"] = []


# --- Compartment ---

class CompartmentBase(BaseModel):
    drawer_id: int
    label: str
    description: Optional[str] = None
    active: bool = True


class CompartmentCreate(CompartmentBase):
    pass


class CompartmentUpdate(BaseModel):
    description: Optional[str] = None
    active: Optional[bool] = None


class Compartment(CompartmentBase):
    id: int

    model_config = {"from_attributes": True}


class CompartmentWithStock(Compartment):
    stock: list["StockWithComponent"] = []


# --- Stock ---

class StockBase(BaseModel):
    component_id: int
    compartment_id: int
    quantity: int = 0
    minimum_qty: int = 0
    unit: str = "st"
    notes: Optional[str] = None


class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    quantity: Optional[int] = None
    minimum_qty: Optional[int] = None
    unit: Optional[str] = None
    notes: Optional[str] = None


class Stock(StockBase):
    id: int

    model_config = {"from_attributes": True}


class StockWithComponent(Stock):
    component: Optional["ComponentSummary"] = None
    compartment: Optional[Compartment] = None


# --- Component ---

class ComponentBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    tags: Optional[list[str]] = None
    specs: Optional[dict[str, Any]] = None


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    tags: Optional[list[str]] = None
    specs: Optional[dict[str, Any]] = None
    active: Optional[bool] = None


class ComponentSummary(ComponentBase):
    id: int
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Component(ComponentSummary):
    updated_at: datetime
    stock: list[StockWithComponent] = []
    category: Optional[Category] = None

    model_config = {"from_attributes": True}


# Update forward refs
Category.model_rebuild()
DrawerWithCompartments.model_rebuild()
CompartmentWithStock.model_rebuild()
StockWithComponent.model_rebuild()
Component.model_rebuild()
