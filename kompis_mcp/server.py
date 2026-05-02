"""KOMPIS MCP server — natural-language component search over the KOMPIS REST API."""

import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = os.environ.get("KOMPIS_URL", "https://kompis.duplo.cc").rstrip("/")

mcp = FastMCP(
    "KOMPIS",
    instructions=(
        "You have access to KOMPIS, an electronics component inventory system. "
        "Use search_components to find components by text query, category, or stock status. "
        "Use get_component to fetch full details including specs (JSONB) and stock locations. "
        "Use list_categories to understand the category tree. "
        "Specs are free-form JSONB — search broadly and reason over returned data to answer questions "
        "like 'NPN transistors rated >300V with hFE 50-200'."
    ),
)


def _get(path: str, params: dict | None = None) -> list | dict:
    url = f"{BASE_URL}{path}"
    with httpx.Client(timeout=15) as client:
        r = client.get(url, params=params)
        r.raise_for_status()
        return r.json()


@mcp.tool()
def search_components(
    query: str = "",
    category_id: int | None = None,
    in_stock: bool = False,
    limit: int = 20,
    skip: int = 0,
) -> list[dict]:
    """Search for components in KOMPIS.

    Args:
        query: Free-text search (name, part number, description, tags).
        category_id: Filter by category ID (use list_categories to find IDs).
        in_stock: If True, only return components with quantity > 0.
        limit: Max results (default 20, max 100).
        skip: Offset for pagination.

    Returns:
        List of component dicts with id, name, manufacturer, part_number,
        category, tags, specs, stock (location + quantity), and files.
    """
    params: dict = {"limit": min(limit, 100), "skip": skip}
    if query:
        params["q"] = query
    if category_id is not None:
        params["category_id"] = category_id
    if in_stock:
        params["in_stock"] = "true"
    return _get("/api/components", params)


@mcp.tool()
def get_component(component_id: int) -> dict:
    """Fetch full details for a single component by ID.

    Returns all fields: specs (JSONB), stock locations with drawer/compartment
    labels and quantities, associated files (datasheets, images), and category.
    """
    return _get(f"/api/components/{component_id}")


@mcp.tool()
def list_categories() -> list[dict]:
    """List all component categories with their IDs, names, slugs, and parent_id.

    Use the returned IDs with search_components(category_id=...) to narrow results.
    Example slugs: 'transistors/npn', 'ic/logic', 'ic/memory'.
    """
    return _get("/api/categories")


@mcp.tool()
def list_locations() -> list[dict]:
    """List all storage drawers with their compartments.

    Returns drawers (L01, L02, …) each containing compartments (F0001, F0002, …).
    Useful for answering 'what is stored in drawer L21?' type questions.
    """
    return _get("/api/drawers")


@mcp.tool()
def get_low_stock() -> list[dict]:
    """Return all stock entries where quantity is at or below the minimum threshold.

    Use this to answer 'what components are running low?' or 'what needs reordering?'
    """
    return _get("/api/stock", {"low_stock": "true"})


if __name__ == "__main__":
    mcp.run()
