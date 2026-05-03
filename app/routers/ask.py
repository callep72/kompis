import json
import anthropic
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.config import settings
from app.models.models import Component, Stock, Compartment, Drawer
from app.services import category_service

router = APIRouter(tags=["ask"])

SYSTEM_PROMPT = (
    "Du är en hjälpsam assistent för KOMPIS, ett lagerhanteringssystem för elektronikkomponenter. "
    "Svara alltid på svenska.\n\n"
    "Sökregler:\n"
    "- Sök alltid med ETT enkelt engelskt nyckelord per sökning, aldrig fraser. "
    "  'nixie driver' → sök 'nixie'. 'germaniumtransistorer' → sök 'germanium'. "
    "  'NPN darlington' → sök 'darlington'. 'kondensatorer' → sök 'capacitor'.\n"
    "- Gör hellre 2-3 separata enkelsökningar och resonera över resultaten "
    "  än att söka på en flerordsfras.\n"
    "- Filtrera och resonera över returnerade data.\n\n"
    "Svarsformat:\n"
    "- Vid 3 eller fler träffar: presentera alltid en Markdown-tabell som översikt först. "
    "  Välj kolumner relevanta för frågan (t.ex. Modell | Typ | Vceo | Ic max | Paket | Lagerplats). "
    "  Avsluta med kommentarer om urval, datablad och rekommendationer.\n"
    "- Vid 1–2 träffar: beskriv komponenterna direkt utan tabell.\n"
    "- Nämn alltid om en komponent har datablad tillgängligt.\n\n"
    "Platsfrågor:\n"
    "- För frågor om lådor (t.ex. 'vad finns i L21?' eller 'visa L21') → använd search_by_location med drawer='L21'.\n"
    "- För frågor om specifika fack (t.ex. 'vad är i F0128?') → använd search_by_location med compartment='F0128'.\n"
    "- Vid lådresultat: skriv ENBART en kort prosasammanfattning (2–4 meningar) om innehållet – "
    "  INGEN Markdown-tabell, INGA punktlistor med komponentnamn. "
    "  GUI:t visar automatiskt en klickbar tabell med alla fack."
)

TOOLS = [
    {
        "name": "search_components",
        "description": (
            "Sök efter komponenter i KOMPIS-lagret. "
            "Använd enkla engelska nyckelord: 'germanium', 'NPN', 'NAND', 'capacitor' etc. "
            "Svenska fraser matchar inte – sök på materialet eller komponenttypen på engelska. "
            "Returnerar komponenter med specs, lagerplatser och filer (datablad etc)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Fritextsökning på namn, artikelnummer, beskrivning eller taggar."},
                "category_id": {"type": "integer", "description": "Filtrera på kategori-ID (hämta IDs med list_categories)."},
                "in_stock": {"type": "boolean", "description": "Om true, returnera bara komponenter med lager > 0."},
                "limit": {"type": "integer", "description": "Max antal resultat (standard 20, max 100)."},
                "skip": {"type": "integer", "description": "Offset för paginering."},
            },
        },
    },
    {
        "name": "get_component",
        "description": "Hämta fullständiga detaljer för en specifik komponent via dess ID, inklusive alla specs, lagerplatser och filer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "component_id": {"type": "integer", "description": "Komponentens ID."},
            },
            "required": ["component_id"],
        },
    },
    {
        "name": "list_categories",
        "description": "Lista alla komponentkategorier med ID, namn, slug och parent_id. Använd ID:n med search_components för att filtrera.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "search_by_location",
        "description": (
            "Hitta komponenter på en specifik plats. "
            "Ange antingen en låda (t.ex. 'L21') eller ett fack (t.ex. 'F0128'). "
            "Lådfrågor returnerar en kompakt lista med alla fack och komponenter. "
            "Fackfrågor returnerar full komponentinfo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "drawer":      {"type": "string", "description": "Lådetikett, t.ex. 'L21'. Returnerar alla komponenter i lådan."},
                "compartment": {"type": "string", "description": "Facketikett, t.ex. 'F0128'. Returnerar komponenten i det facket."},
            },
        },
    },
]


class AskRequest(BaseModel):
    question: str


class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int


class AskResponse(BaseModel):
    answer: str
    components: list[dict]
    drawers: list[dict]
    usage: TokenUsage


def _serialize(comp: Component) -> dict:
    stock_list = []
    for s in comp.stock:
        entry = {
            "id": s.id,
            "quantity": s.quantity,
            "minimum_qty": s.minimum_qty,
            "unit": s.unit,
            "notes": s.notes,
        }
        if s.compartment:
            entry["compartment"] = s.compartment.label
            if s.compartment.drawer:
                entry["drawer"] = s.compartment.drawer.label
        stock_list.append(entry)

    files_list = []
    for f in comp.files:
        files_list.append({
            "id": f.id,
            "file_type": f.file_type,
            "filename": f.filename,
            "filepath": f.filepath,
            "mime_type": f.mime_type,
            "is_primary": f.is_primary,
        })

    return {
        "id": comp.id,
        "name": comp.name,
        "description": comp.description,
        "manufacturer": comp.manufacturer,
        "part_number": comp.part_number,
        "tags": comp.tags or [],
        "specs": comp.specs or {},
        "category": {"id": comp.category.id, "name": comp.category.name, "slug": comp.category.slug} if comp.category else None,
        "stock": stock_list,
        "files": files_list,
    }


def _search_with_files(
    db: Session,
    query: str = "",
    category_id: int | None = None,
    in_stock: bool = False,
    limit: int = 20,
    skip: int = 0,
) -> list[Component]:
    from sqlalchemy import or_, and_, func, cast, Text

    q = db.query(Component).filter(Component.active == True)

    if query:
        words = [w for w in query.split() if len(w) > 1]
        conditions = [
            Component.search_vector.op("@@")(func.websearch_to_tsquery("swedish", query)),
            Component.name.ilike(f"%{query}%"),
            Component.part_number.ilike(f"%{query}%"),
            func.array_to_string(Component.tags, " ").ilike(f"%{query}%"),
            cast(Component.specs, Text).ilike(f"%{query}%"),
        ]
        # For multi-word queries: any word matching name/tags/specs is a candidate
        if len(words) > 1:
            conditions.extend([
                or_(
                    Component.name.ilike(f"%{w}%"),
                    func.array_to_string(Component.tags, " ").ilike(f"%{w}%"),
                    cast(Component.specs, Text).ilike(f"%{w}%"),
                )
                for w in words
            ])
        q = q.filter(or_(*conditions)
        )

    if category_id is not None:
        q = q.filter(Component.category_id == category_id)

    if in_stock:
        q = q.filter(Component.stock.any(Stock.quantity > 0))

    return (
        q.options(
            joinedload(Component.category),
            joinedload(Component.stock).joinedload(Stock.compartment).joinedload(Compartment.drawer),
            joinedload(Component.files),
        )
        .order_by(Component.name)
        .offset(skip)
        .limit(min(limit, 100))
        .all()
    )


def _get_component_with_files(db: Session, component_id: int) -> Component | None:
    return (
        db.query(Component)
        .options(
            joinedload(Component.category),
            joinedload(Component.stock).joinedload(Stock.compartment).joinedload(Compartment.drawer),
            joinedload(Component.files),
        )
        .filter(Component.id == component_id, Component.active == True)
        .first()
    )


def _short_desc(component) -> str:
    desc = (component.description or "").strip()
    if desc:
        return desc[:60] + "…" if len(desc) > 60 else desc
    specs = component.specs or {}
    parts = [v for k, v in [
        ("type",       specs.get("type", "")),
        ("material",   specs.get("material", "")),
        ("technology", specs.get("technology", "")),
        ("Vceo",       f"Vceo {specs['Vceo']}" if specs.get("Vceo") else ""),
        ("Vout",       specs.get("Vout", "")),
        ("Iout_max",   specs.get("Iout_max", "")),
        ("Vcc",        specs.get("Vcc", "")),
        ("package",    specs.get("package", "")),
    ] if v]
    return ", ".join(parts)[:60]


def _serialize_drawer(drawer: Drawer, compartments_data: list[dict]) -> dict:
    photos = [
        {"filepath": f.filepath, "filename": f.filename, "id": f.id}
        for f in (drawer.files or []) if f.file_type == "image"
    ]
    return {
        "id": drawer.id,
        "label": drawer.label,
        "description": drawer.description,
        "photos": photos,
        "compartments": compartments_data,
    }


from fastapi import HTTPException

@router.get("/api/drawers-overview")
def drawers_overview(db: Session = Depends(get_db)):
    from app.models.models import Category
    drawers = (
        db.query(Drawer)
        .options(
            joinedload(Drawer.compartments)
                .joinedload(Compartment.stock)
                .joinedload(Stock.component)
                .joinedload(Component.category),
            joinedload(Drawer.files),
        )
        .order_by(Drawer.label)
        .all()
    )
    result = []
    for d in drawers:
        cats: set[str] = set()
        count = 0
        for comp_obj in d.compartments:
            for s in comp_obj.stock:
                if s.component and s.component.active:
                    count += 1
                    if s.component.category:
                        cats.add(s.component.category.name)
        content = ", ".join(sorted(cats)) if cats else (d.description or "–")
        photo = next((f.filepath for f in d.files if f.file_type == "image"), None)
        result.append({
            "id": d.id,
            "label": d.label,
            "description": d.description,
            "content_summary": content,
            "component_count": count,
            "photo": photo,
        })
    return result


@router.get("/api/drawers/{drawer_label}/summary")
def drawer_summary(drawer_label: str, db: Session = Depends(get_db)):
    drawer = (
        db.query(Drawer)
        .options(
            joinedload(Drawer.compartments)
                .joinedload(Compartment.stock)
                .joinedload(Stock.component),
            joinedload(Drawer.files),
        )
        .filter(Drawer.label == drawer_label.upper())
        .first()
    )
    if not drawer:
        raise HTTPException(status_code=404, detail="Låda hittades inte")
    compartments_data = []
    for comp_obj in sorted(drawer.compartments, key=lambda c: c.label):
        if not comp_obj.active:
            continue
        for s in comp_obj.stock:
            if s.component and s.component.active:
                compartments_data.append({
                    "label": comp_obj.label,
                    "component_id": s.component.id,
                    "component_name": s.component.name,
                    "quantity": s.quantity,
                    "unit": s.unit,
                    "description": _short_desc(s.component),
                })
    return _serialize_drawer(drawer, compartments_data)


@router.get("/api/components/{component_id}/card")
def get_component_card(component_id: int, db: Session = Depends(get_db)):
    comp = _get_component_with_files(db, component_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Komponent hittades inte")
    return _serialize(comp)


@router.post("/api/ask", response_model=AskResponse)
def ask(body: AskRequest, db: Session = Depends(get_db)):
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    components_found: dict[int, dict] = {}
    drawers_found: dict[int, dict] = {}

    def call_tool(name: str, inputs: dict):
        if name == "search_components":
            results = _search_with_files(
                db,
                query=inputs.get("query", ""),
                category_id=inputs.get("category_id"),
                in_stock=inputs.get("in_stock", False),
                limit=inputs.get("limit", 20),
                skip=inputs.get("skip", 0),
            )
            serialized = [_serialize(c) for c in results]
            for c in serialized:
                components_found[c["id"]] = c
            return serialized

        if name == "get_component":
            comp = _get_component_with_files(db, inputs["component_id"])
            if not comp:
                return {"error": "Komponent hittades inte"}
            s = _serialize(comp)
            components_found[s["id"]] = s
            return s

        if name == "list_categories":
            cats = category_service.get_all(db)
            return [{"id": c.id, "name": c.name, "slug": c.slug, "parent_id": c.parent_id} for c in cats]

        if name == "search_by_location":
            drawer_label = (inputs.get("drawer") or "").upper().strip()
            compartment_label = (inputs.get("compartment") or "").upper().strip()

            if compartment_label:
                comp_obj = db.query(Compartment).filter(Compartment.label == compartment_label).first()
                if not comp_obj:
                    return {"error": f"Fack {compartment_label} hittades inte"}
                results = []
                for s in db.query(Stock).filter(Stock.compartment_id == comp_obj.id).all():
                    c = _get_component_with_files(db, s.component_id)
                    if c:
                        ser = _serialize(c)
                        components_found[ser["id"]] = ser
                        results.append(ser)
                drawer_label_str = comp_obj.drawer.label if comp_obj.drawer else "?"
                return {"compartment": compartment_label, "drawer": drawer_label_str, "components": results}

            if drawer_label:
                drawer = (
                    db.query(Drawer)
                    .options(
                        joinedload(Drawer.compartments)
                            .joinedload(Compartment.stock)
                            .joinedload(Stock.component),
                        joinedload(Drawer.files),
                    )
                    .filter(Drawer.label == drawer_label)
                    .first()
                )
                if not drawer:
                    return {"error": f"Låda {drawer_label} hittades inte"}
                compartments_data = []
                for comp_obj in sorted(drawer.compartments, key=lambda c: c.label):
                    if not comp_obj.active:
                        continue
                    for s in comp_obj.stock:
                        if s.component and s.component.active:
                            compartments_data.append({
                                "label": comp_obj.label,
                                "component_id": s.component.id,
                                "component_name": s.component.name,
                                "quantity": s.quantity,
                                "unit": s.unit,
                                "description": _short_desc(s.component),
                            })
                result = _serialize_drawer(drawer, compartments_data)
                drawers_found[drawer.id] = result
                return result

            return {"error": "Ange 'drawer' (t.ex. 'L21') eller 'compartment' (t.ex. 'F0128')"}

        return {"error": f"Okänt verktyg: {name}"}

    messages = [{"role": "user", "content": body.question}]
    total_input_tokens = 0
    total_output_tokens = 0

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = call_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False, default=str),
                    })
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    answer = next((b.text for b in response.content if hasattr(b, "text")), "")
    return AskResponse(
        answer=answer,
        components=list(components_found.values()),
        drawers=list(drawers_found.values()),
        usage=TokenUsage(input_tokens=total_input_tokens, output_tokens=total_output_tokens),
    )
