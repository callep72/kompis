from datetime import datetime
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Text, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, TSVECTOR
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Drawer(Base):
    __tablename__ = "drawers"

    id = Column(Integer, primary_key=True)
    label = Column(String(10), unique=True, nullable=False)
    description = Column(Text)

    compartments = relationship("Compartment", back_populates="drawer")
    files = relationship("File", back_populates="drawer", foreign_keys="File.drawer_id")


class Compartment(Base):
    __tablename__ = "compartments"

    id = Column(Integer, primary_key=True)
    drawer_id = Column(Integer, ForeignKey("drawers.id"), nullable=False)
    label = Column(String(10), unique=True, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    description = Column(Text)

    drawer = relationship("Drawer", back_populates="compartments")
    stock = relationship("Stock", back_populates="compartment")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)

    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    components = relationship("Component", back_populates="category")


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    manufacturer = Column(String(100))
    part_number = Column(String(100))
    tags = Column(ARRAY(Text))
    specs = Column(JSONB)
    active = Column(Boolean, default=True, nullable=False)
    search_vector = Column(TSVECTOR)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    category = relationship("Category", back_populates="components")
    stock = relationship("Stock", back_populates="component")
    files = relationship("File", back_populates="component")


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey("components.id"), nullable=False)
    compartment_id = Column(Integer, ForeignKey("compartments.id"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    minimum_qty = Column(Integer, default=0, nullable=False)
    unit = Column(String(20), default="st", nullable=False)
    notes = Column(Text)

    component = relationship("Component", back_populates="stock")
    compartment = relationship("Compartment", back_populates="stock")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey("components.id"), nullable=True)
    drawer_id = Column(Integer, ForeignKey("drawers.id"), nullable=True)
    file_type = Column(String(20))
    source = Column(String(20), default="upload", nullable=False)
    filename = Column(String(255), nullable=False)
    filepath = Column(Text, nullable=False)
    mime_type = Column(String(100))
    is_primary = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    component = relationship("Component", back_populates="files", foreign_keys=[component_id])
    drawer = relationship("Drawer", back_populates="files", foreign_keys=[drawer_id])
