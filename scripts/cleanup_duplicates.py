#!/usr/bin/env python3
"""Remove duplicate components created by running seed_l06.py twice.

Strategy: for each component name that appears more than once,
keep the copy that has stock entries (the first run), soft-delete the rest.

Run on rash:
  python3 scripts/cleanup_duplicates.py
"""
import json
import sys
import urllib.request
import urllib.error

BASE = "http://localhost:8000"


def api_get(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"GET {path} fel: {e}", file=sys.stderr)
        return None


def api_delete(path):
    req = urllib.request.Request(f"{BASE}{path}", method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        print(f"DELETE {path} fel: {e}", file=sys.stderr)
        return None


def fetch_all_components():
    """Fetch all active components with pagination."""
    all_comps = []
    skip = 0
    limit = 200
    while True:
        page = api_get(f"/api/components?skip={skip}&limit={limit}")
        if not page:
            break
        all_comps.extend(page)
        if len(page) < limit:
            break
        skip += limit
    return all_comps


def main():
    print("=== Cleanup: tar bort dubbletter ===\n")

    components = fetch_all_components()
    print(f"Hittade {len(components)} aktiva komponenter totalt.\n")

    # Group by name
    by_name = {}
    for c in components:
        by_name.setdefault(c["name"], []).append(c)

    duplicates = {name: copies for name, copies in by_name.items() if len(copies) > 1}
    print(f"Namn med dubbletter: {len(duplicates)}\n")

    if not duplicates:
        print("Inga dubbletter hittades — inget att göra.")
        return

    deleted = 0
    for name, copies in sorted(duplicates.items()):
        # Sort: prefer the one with stock entries; otherwise keep lowest id
        def score(c):
            has_stock = len(c.get("stock", [])) > 0
            return (0 if has_stock else 1, c["id"])

        copies.sort(key=score)
        keeper = copies[0]
        to_delete = copies[1:]

        stock_info = f"{len(keeper.get('stock', []))} lagerplats(er)"
        print(f"  {name}")
        print(f"    Behåller: id={keeper['id']} ({stock_info})")
        for dup in to_delete:
            status = api_delete(f"/api/components/{dup['id']}")
            print(f"    Raderar:  id={dup['id']} → HTTP {status}")
            if status in (200, 204):
                deleted += 1

    print(f"\nKLART. {deleted} dubbletter borttagna (soft-delete, active=false).")


if __name__ == "__main__":
    main()
