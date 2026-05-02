import json
import anthropic
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.config import settings
from app.models.models import Component, Stock, Compartment
from app.services import category_service

router = APIRouter(tags=["ask"])

SYSTEM_PROMPT = (
    "Du är en hjälpsam assistent för KOMPIS, ett lagerhanteringssystem för elektronikkomponenter. "
    "Svara alltid på svenska. Använd verktygen för att söka i lagret och ge ett koncist, informativt svar. "
    "När du listar komponenter, ta med relevanta specifikationer. "
    "Om du hittar komponenter med datablad, nämn det."
)

TOOLS = [
    {
        "name": "search_components",
        "description": (
            "Sök efter komponenter i KOMPIS-lagret med fritext, kategori eller lagerstatus. "
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
]


class AskRequest(BaseModel):
    question: str


class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int


class AskResponse(BaseModel):
    answer: str
    components: list[dict]
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
    from sqlalchemy import or_, func, cast, Text
    from app.models.models import File

    q = db.query(Component).filter(Component.active == True)

    if query:
        q = q.filter(
            or_(
                Component.search_vector.op("@@")(func.websearch_to_tsquery("swedish", query)),
                Component.name.ilike(f"%{query}%"),
                Component.part_number.ilike(f"%{query}%"),
                func.array_to_string(Component.tags, " ").ilike(f"%{query}%"),
                cast(Component.specs, Text).ilike(f"%{query}%"),
            )
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


@router.post("/api/ask", response_model=AskResponse)
def ask(body: AskRequest, db: Session = Depends(get_db)):
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    components_found: dict[int, dict] = {}

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
        usage=TokenUsage(input_tokens=total_input_tokens, output_tokens=total_output_tokens),
    )
