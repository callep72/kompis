import re
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services import component_service, location_service, stock_service, category_service, file_service
from app.schemas.schemas import (
    ComponentCreate, ComponentUpdate,
    DrawerCreate, CompartmentCreate, CompartmentUpdate,
    CategoryCreate, CategoryUpdate,
    StockCreate, StockUpdate,
)

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app/templates")


# --- Search ---

@router.get("/", response_class=HTMLResponse)
def search(request: Request):
    return templates.TemplateResponse("search.html", {
        "request": request,
        "active_page": "search",
    })


# --- Admin / Components ---

@router.get("/admin", response_class=HTMLResponse)
def index(
    request: Request,
    q: Optional[str] = None,
    category_id: Optional[str] = None,
    in_stock: Optional[str] = None,
    skip: int = 0,
    db: Session = Depends(get_db),
):
    cat_id = int(category_id) if category_id else None
    components = component_service.get_all(
        db, q=q, category_id=cat_id,
        in_stock=in_stock == "true",
        skip=skip, limit=50,
    )
    categories = category_service.get_all(db)
    return templates.TemplateResponse("components/list.html", {
        "request": request, "components": components, "categories": categories,
        "q": q, "category_id": cat_id, "in_stock": in_stock == "true",
        "active_page": "components",
    })


@router.get("/components/new", response_class=HTMLResponse)
def new_component_form(request: Request, db: Session = Depends(get_db)):
    categories = category_service.get_all(db)
    return templates.TemplateResponse("components/form.html", {
        "request": request, "component": None, "categories": categories,
        "active_page": "components",
    })


@router.post("/components/new")
async def create_component_post(
    request: Request,
    db: Session = Depends(get_db),
):
    form = await request.form()
    specs = _parse_specs(form.get("specs", ""))
    tags = _parse_tags(form.get("tags", ""))
    data = ComponentCreate(
        name=form["name"],
        manufacturer=form.get("manufacturer") or None,
        part_number=form.get("part_number") or None,
        category_id=int(form["category_id"]) if form.get("category_id") else None,
        description=form.get("description") or None,
        tags=tags or None,
        specs=specs or None,
    )
    comp = component_service.create(db, data)
    return RedirectResponse(f"/components/{comp.id}", status_code=303)


@router.get("/components/{component_id}", response_class=HTMLResponse)
def component_detail(request: Request, component_id: int, db: Session = Depends(get_db)):
    comp = component_service.get_by_id(db, component_id)
    if not comp:
        return RedirectResponse("/admin", status_code=303)
    svg, label = _component_symbol(comp)
    return templates.TemplateResponse("components/detail.html", {
        "request": request, "component": comp, "active_page": "components",
        "symbol_svg": svg, "symbol_label": label,
    })


def _load_symbol_svg(name: str) -> str | None:
    try:
        with open(f"symbols/{name}.svg") as f:
            return f.read()
    except OSError:
        return None


def _component_symbol(comp) -> tuple[str | None, str | None]:
    svg = _transistor_svg(comp)
    if svg:
        return svg, None
    name, label = _logic_svg(comp)
    if name:
        return _load_symbol_svg(name), label
    return None, None


def _transistor_svg(comp) -> str | None:
    cat_slug = (comp.category.slug if comp.category else "").lower()
    if "transistor" not in cat_slug:
        return None
    tags = [t.lower() for t in (comp.tags or [])]
    specs = comp.specs or {}
    if "darlington" in tags:
        return _load_symbol_svg("darlington")
    if "mosfet" in tags or "fet" in tags or specs.get("gate"):
        return _load_symbol_svg("mosfet")
    t = specs.get("type", "").upper()
    if t == "NPN":
        return _load_symbol_svg("npn")
    if t == "PNP":
        return _load_symbol_svg("pnp")
    return None


_SKIP = re.compile(
    r"\b(flip.flop|vippa|jk|shift.register|counter|räknare|latch|"
    r"register|comparator|komparator|mux|multiplexer|encoder|decoder|"
    r"transceiver|selector|select)\b"
)


def _has_gate(text: str, gate: str) -> bool:
    return bool(re.search(rf"\b{gate}\b|\b{gate}.gate\b|\b{gate}.grind\b", text))


def _gate_inputs(text: str, gate: str) -> int:
    if re.search(r"\b4(?:[- .]?input|[- .]?ingång)", text):
        return 4
    if re.search(r"\b3(?:[- .]?input|[- .]?ingång)", text):
        return 3
    if gate in ("nand", "nor") and "triple" in text:
        return 3
    return 2


def _logic_svg(comp) -> tuple[str | None, str | None]:
    text = " ".join([comp.name] + list(comp.tags or [])).lower()
    if _SKIP.search(text):
        return None, None

    if _has_gate(text, "nand"):
        gate = "nand"
    elif _has_gate(text, "xnor"):
        gate = "xnor"
    elif _has_gate(text, "xor"):
        gate = "xor"
    elif _has_gate(text, "nor"):
        gate = "nor"
    elif _has_gate(text, "and"):
        gate = "and"
    elif re.search(r"\binverter\b", text):
        gate = "inverter"
    elif re.search(r"\bbuffer\b", text):
        gate = "buffer"
    else:
        return None, None

    inputs = 2
    if gate in ("and", "nand", "nor", "xor", "xnor"):
        inputs = 2 if gate == "xnor" else _gate_inputs(text, gate)

    count = (8 if "octal" in text else 6 if "hex" in text else
             4 if "quad" in text else 3 if "triple" in text else
             2 if "dual" in text else None)

    svg_name = (f"logic_{gate}_{inputs}in" if gate in ("and", "nand", "nor", "xor", "xnor")
                else f"logic_{gate}")
    label = f"x{count}" if count and count > 1 else None
    return svg_name, label


@router.get("/components/{component_id}/edit", response_class=HTMLResponse)
def edit_component_form(request: Request, component_id: int, db: Session = Depends(get_db)):
    comp = component_service.get_by_id(db, component_id)
    if not comp:
        return RedirectResponse("/admin", status_code=303)
    categories = category_service.get_all(db)
    return templates.TemplateResponse("components/form.html", {
        "request": request, "component": comp, "categories": categories,
        "active_page": "components",
    })


@router.post("/components/{component_id}/edit")
async def update_component_post(request: Request, component_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    specs = _parse_specs(form.get("specs", ""))
    tags = _parse_tags(form.get("tags", ""))
    data = ComponentUpdate(
        name=form.get("name"),
        manufacturer=form.get("manufacturer") or None,
        part_number=form.get("part_number") or None,
        category_id=int(form["category_id"]) if form.get("category_id") else None,
        description=form.get("description") or None,
        tags=tags or None,
        specs=specs or None,
        active=form.get("active") == "true",
    )
    component_service.update(db, component_id, data)
    return RedirectResponse(f"/components/{component_id}", status_code=303)


@router.post("/components/{component_id}/delete")
def delete_component_post(component_id: int, db: Session = Depends(get_db)):
    component_service.delete(db, component_id)
    return RedirectResponse("/admin", status_code=303)


@router.post("/components/{component_id}/files")
async def upload_file_post(request: Request, component_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    uploaded = form.get("file")
    file_type = form.get("file_type", "image")
    if uploaded:
        await file_service.save_upload(db, component_id, uploaded, file_type)
    return RedirectResponse(f"/components/{component_id}", status_code=303)


@router.post("/components/{component_id}/files/{file_id}/delete")
def delete_file_post(component_id: int, file_id: int, db: Session = Depends(get_db)):
    file_service.delete_file(db, file_id)
    return RedirectResponse(f"/components/{component_id}", status_code=303)


# --- Locations ---

@router.get("/locations", response_class=HTMLResponse)
def locations(request: Request, db: Session = Depends(get_db)):
    drawers = location_service.get_all_drawers(db)
    from sqlalchemy.orm import joinedload
    from app.models.models import Drawer
    drawers = db.query(Drawer).options(
        joinedload(Drawer.compartments)
    ).order_by(Drawer.label).all()
    return templates.TemplateResponse("locations/list.html", {
        "request": request, "drawers": drawers, "active_page": "locations",
    })


@router.get("/locations/drawers/new", response_class=HTMLResponse)
def new_drawer_form(request: Request):
    return templates.TemplateResponse("locations/drawer_form.html", {
        "request": request, "active_page": "locations",
    })


@router.post("/locations/drawers/new")
async def create_drawer_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    data = DrawerCreate(
        label=form["label"],
        description=form.get("description") or None,
    )
    drawer = location_service.create_drawer(db, data)
    return RedirectResponse(f"/locations/drawers/{drawer.id}", status_code=303)


@router.get("/locations/drawers/{drawer_id}", response_class=HTMLResponse)
def drawer_detail(request: Request, drawer_id: int, db: Session = Depends(get_db)):
    drawer = location_service.get_drawer(db, drawer_id)
    if not drawer:
        return RedirectResponse("/locations", status_code=303)
    return templates.TemplateResponse("locations/drawer_detail.html", {
        "request": request, "drawer": drawer, "active_page": "locations",
    })


@router.get("/locations/compartments/new", response_class=HTMLResponse)
def new_compartment_form(request: Request, drawer_id: Optional[int] = None, db: Session = Depends(get_db)):
    drawers = location_service.get_all_drawers(db)
    return templates.TemplateResponse("locations/compartment_form.html", {
        "request": request, "drawers": drawers, "drawer_id": drawer_id,
        "active_page": "locations",
    })


@router.post("/locations/compartments/new")
async def create_compartment_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    drawer_id = int(form.get("drawer_id") or form.get("drawer_id_select", 0))
    data = CompartmentCreate(
        drawer_id=drawer_id,
        label=form["label"],
        description=form.get("description") or None,
    )
    comp = location_service.create_compartment(db, data)
    return RedirectResponse(f"/locations/drawers/{comp.drawer_id}", status_code=303)


@router.get("/locations/compartments/{compartment_id}", response_class=HTMLResponse)
def compartment_detail(request: Request, compartment_id: int, db: Session = Depends(get_db)):
    comp = location_service.get_compartment(db, compartment_id)
    if not comp:
        return RedirectResponse("/locations", status_code=303)
    return templates.TemplateResponse("locations/drawer_detail.html", {
        "request": request, "drawer": comp.drawer, "active_page": "locations",
    })


# --- Categories ---

@router.get("/categories", response_class=HTMLResponse)
def categories(request: Request, db: Session = Depends(get_db)):
    all_cats = category_service.get_all(db)
    root_cats = [c for c in all_cats if c.parent_id is None]
    return templates.TemplateResponse("categories/list.html", {
        "request": request, "categories": all_cats, "root_categories": root_cats,
        "active_page": "categories",
    })


@router.get("/categories/new", response_class=HTMLResponse)
def new_category_form(request: Request, db: Session = Depends(get_db)):
    categories = category_service.get_all(db)
    return templates.TemplateResponse("categories/form.html", {
        "request": request, "category": None, "categories": categories,
        "active_page": "categories",
    })


@router.post("/categories/new")
async def create_category_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    data = CategoryCreate(
        name=form["name"],
        slug=form["slug"],
        parent_id=int(form["parent_id"]) if form.get("parent_id") else None,
    )
    category_service.create(db, data)
    return RedirectResponse("/categories", status_code=303)


@router.get("/categories/{category_id}/edit", response_class=HTMLResponse)
def edit_category_form(request: Request, category_id: int, db: Session = Depends(get_db)):
    cat = category_service.get_by_id(db, category_id)
    if not cat:
        return RedirectResponse("/categories", status_code=303)
    categories = category_service.get_all(db)
    return templates.TemplateResponse("categories/form.html", {
        "request": request, "category": cat, "categories": categories,
        "active_page": "categories",
    })


@router.post("/categories/{category_id}/edit")
async def update_category_post(request: Request, category_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    data = CategoryUpdate(
        name=form.get("name"),
        slug=form.get("slug"),
        parent_id=int(form["parent_id"]) if form.get("parent_id") else None,
    )
    category_service.update(db, category_id, data)
    return RedirectResponse("/categories", status_code=303)


# --- Stock ---

@router.get("/stock", response_class=HTMLResponse)
def stock_low(request: Request, db: Session = Depends(get_db)):
    items = stock_service.get_all(db, low_stock=True)
    return templates.TemplateResponse("stock/list.html", {
        "request": request, "stock_items": items, "active_page": "stock",
    })


@router.get("/stock/new", response_class=HTMLResponse)
def new_stock_form(request: Request, component_id: Optional[int] = None, db: Session = Depends(get_db)):
    from app.models.models import Component, Compartment
    components = db.query(Component).filter(Component.active == True).order_by(Component.name).all()
    compartments = db.query(Compartment).filter(Compartment.active == True).order_by(Compartment.label).all()
    return templates.TemplateResponse("stock/form.html", {
        "request": request, "stock": None, "components": components,
        "compartments": compartments, "selected_component_id": component_id,
        "active_page": "stock",
    })


@router.post("/stock/new")
async def create_stock_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    data = StockCreate(
        component_id=int(form["component_id"]),
        compartment_id=int(form["compartment_id"]),
        quantity=int(form.get("quantity", 0)),
        minimum_qty=int(form.get("minimum_qty", 0)),
        unit=form.get("unit", "st"),
        notes=form.get("notes") or None,
    )
    stock = stock_service.create(db, data)
    return RedirectResponse(f"/components/{stock.component_id}", status_code=303)


@router.get("/stock/{stock_id}/edit", response_class=HTMLResponse)
def edit_stock_form(request: Request, stock_id: int, db: Session = Depends(get_db)):
    s = stock_service.get_by_id(db, stock_id)
    if not s:
        return RedirectResponse("/admin", status_code=303)
    return templates.TemplateResponse("stock/form.html", {
        "request": request, "stock": s, "components": [], "compartments": [],
        "selected_component_id": None, "active_page": "stock",
    })


@router.post("/stock/{stock_id}/edit")
async def update_stock_post(request: Request, stock_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    data = StockUpdate(
        quantity=int(form.get("quantity", 0)),
        minimum_qty=int(form.get("minimum_qty", 0)),
        unit=form.get("unit", "st"),
        notes=form.get("notes") or None,
    )
    s = stock_service.update(db, stock_id, data)
    component_id = s.component_id if s else None
    if component_id:
        return RedirectResponse(f"/components/{component_id}", status_code=303)
    return RedirectResponse("/admin", status_code=303)


# --- Helpers ---

def _parse_specs(raw: str) -> dict:
    specs = {}
    for line in raw.strip().splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip()
            if k:
                specs[k] = v
    return specs


def _parse_tags(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]
