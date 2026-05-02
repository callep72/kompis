#!/usr/bin/env python3
"""Seed drawer L20 (F0177-F0190) with voltage regulators + create category.

Run on rash:
  python3 scripts/seed_l20_vreg.py
"""
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

BASE = "http://localhost:8000"


def api_get(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}") as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"GET {path} → {e.code}: {e.read()[:200]}", file=sys.stderr)
        return None


def api_post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        f"{BASE}{path}", data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return None, e.code


COMPONENTS = {
    "78L05": {
        "name": "78L05",
        "manufacturer": None,
        "specs": {
            "Vout": "+5V",
            "Iout_max": "100mA",
            "Vin_min": "7V",
            "Vin_max": "30V",
            "dropout": "~1.7V",
            "package": "TO-92",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +5 V, lågströmsvariant (100 mA), TO-92-kapsel. "
            "Intern termisk och kortslutningsskydd. Vin 7–30 V. "
            "Används när lite ström räcker och plats är begränsad (t.ex. på kretskort "
            "som matas från en högresspänningskälla men bara behöver 5 V lokalt)."
        ),
        "tags": ["78L05", "5V regulator", "LDO", "TO-92", "positive regulator"],
    },
    "L7805CV": {
        "name": "L7805CV",
        "manufacturer": "STMicroelectronics",
        "specs": {
            "Vout": "+5V",
            "Iout_max": "1A",
            "Vin_min": "7V",
            "Vin_max": "35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +5 V, 1 A, TO-220 (STMicroelectronics). "
            "Intern termisk säkring, kortslutningsskydd och säker driftomkoppling. "
            "Vin 7–35 V. Standardkomponent för +5 V-försörjning i digitala kretsar. "
            "Kräver heatsink vid strömmar över ~500 mA."
        ),
        "tags": ["L7805CV", "7805", "5V regulator", "1A", "TO-220", "ST", "positive regulator"],
    },
    "7805": {
        "name": "7805",
        "manufacturer": None,
        "specs": {
            "Vout": "+5V",
            "Iout_max": "1A",
            "Vin_min": "7V",
            "Vin_max": "35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +5 V, 1 A, TO-220 (generisk beteckning). "
            "Intern termisk säkring och kortslutningsskydd. Vin 7–35 V. "
            "Industristandard; tillverkas av ST, Fairchild, ON Semi m.fl. "
            "Pin-kompatibel med L7805CV, µA7805 och liknande."
        ),
        "tags": ["7805", "5V regulator", "1A", "TO-220", "positive regulator"],
    },
    "79M05AHC": {
        "name": "79M05AHC",
        "manufacturer": None,
        "specs": {
            "Vout": "−5V",
            "Iout_max": "500mA",
            "Vin_min": "−7V",
            "Vin_max": "−35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "negativ",
        },
        "desc": (
            "Negativ fastspänningsregulator −5 V, 500 mA, TO-220 (79M-serie). "
            "79M-serien är mellannivå: 500 mA (79L = 100 mA, 79xx = 1 A). "
            "Används i dubbel ±5 V-matning tillsammans med en positiv 7805. "
            "AHC-suffix anger kvalitets- eller temperaturklass."
        ),
        "tags": ["79M05", "79M05AHC", "-5V regulator", "negative regulator", "500mA", "TO-220"],
    },
    "TS7809": {
        "name": "TS7809",
        "manufacturer": "SGS/STMicroelectronics",
        "specs": {
            "Vout": "+9V",
            "Iout_max": "1A",
            "Vin_min": "11.5V",
            "Vin_max": "35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +9 V, 1 A, TO-220 (SGS/STMicroelectronics TS-serie). "
            "Vin 11,5–35 V. Intern termisk skydd och kortslutningsskydd. "
            "Används i applikationer som kräver +9 V, t.ex. analoga effektsteg och äldre videokretsar."
        ),
        "tags": ["TS7809", "7809", "9V regulator", "1A", "TO-220", "SGS", "positive regulator"],
    },
    "L78S12CV": {
        "name": "L78S12CV",
        "manufacturer": "STMicroelectronics",
        "specs": {
            "Vout": "+12V",
            "Iout_max": "2A",
            "Vin_min": "14.5V",
            "Vin_max": "35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +12 V, 2 A, TO-220 (STMicroelectronics L78S-serie). "
            "S-serien levererar 2 A istället för standardserien 1 A. "
            "Vin 14,5–35 V. Kräver heatsink. "
            "Används när +12 V-matning måste leverera mer ström än 1 A."
        ),
        "tags": ["L78S12CV", "78S12", "12V regulator", "2A", "TO-220", "ST", "positive regulator"],
    },
    "7812C": {
        "name": "7812C",
        "manufacturer": None,
        "specs": {
            "Vout": "+12V",
            "Iout_max": "1A",
            "Vin_min": "14.5V",
            "Vin_max": "35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +12 V, 1 A, TO-220 (generisk beteckning med C-suffix). "
            "C-suffix anger vanligen kommersiell temperaturklass (0–70 °C). "
            "Vin 14,5–35 V. Intern termisk säkring och kortslutningsskydd."
        ),
        "tags": ["7812C", "7812", "12V regulator", "1A", "TO-220", "positive regulator"],
    },
    "LM340T12": {
        "name": "LM340T12",
        "manufacturer": "National Semiconductor",
        "specs": {
            "Vout": "+12V",
            "Iout_max": "1A",
            "Vin_min": "14.5V",
            "Vin_max": "27V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +12 V, 1 A, TO-220 (National Semiconductor LM340-serie). "
            "LM340 är National Semiconductors ursprungliga 78xx-ekvivalent; "
            "T-suffix = TO-220, 12 = utgångsspänning. "
            "Vin 14,5–27 V (lägre max-ingång än ST/Fairchild-varianter). "
            "Pin-kompatibel med 7812."
        ),
        "tags": ["LM340T12", "LM340", "12V regulator", "1A", "TO-220", "National Semi", "positive regulator"],
    },
    "GL7915": {
        "name": "GL7915",
        "manufacturer": "Motorola/ON Semiconductor",
        "specs": {
            "Vout": "−15V",
            "Iout_max": "1A",
            "Vin_min": "−17.5V",
            "Vin_max": "−35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "negativ",
        },
        "desc": (
            "Negativ fastspänningsregulator −15 V, 1 A, TO-220 (Motorola/ON Semi GL-prefix). "
            "Vin −17,5 till −35 V. Intern termisk säkring. "
            "Används i dubbel ±15 V-matning för operationsförstärkare och analoga kretsar. "
            "GL-prefix = Motorola (senare ON Semiconductor)."
        ),
        "tags": ["GL7915", "7915", "-15V regulator", "negative regulator", "1A", "TO-220", "Motorola"],
    },
    "L7818CV": {
        "name": "L7818CV",
        "manufacturer": "STMicroelectronics",
        "specs": {
            "Vout": "+18V",
            "Iout_max": "1A",
            "Vin_min": "21V",
            "Vin_max": "35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +18 V, 1 A, TO-220 (STMicroelectronics). "
            "Vin 21–35 V. Intern termisk säkring och kortslutningsskydd. "
            "Används i applikationer med högre matningsspänning, "
            "t.ex. för att mata drivkretsar till stegmotorer eller analogkretsar."
        ),
        "tags": ["L7818CV", "7818", "18V regulator", "1A", "TO-220", "ST", "positive regulator"],
    },
    "L7812CV": {
        "name": "L7812CV",
        "manufacturer": "STMicroelectronics",
        "specs": {
            "Vout": "+12V",
            "Iout_max": "1A",
            "Vin_min": "14.5V",
            "Vin_max": "35V",
            "dropout": "~2V",
            "package": "TO-220",
            "polarity": "positiv",
        },
        "desc": (
            "Fastspänningsregulator +12 V, 1 A, TO-220 (STMicroelectronics L78xx-serie). "
            "CV-suffix = kommersiell grad, TO-220-kapsel. "
            "Vin 14,5–35 V. Standard +12 V-regulator för de flesta applikationer."
        ),
        "tags": ["L7812CV", "7812", "12V regulator", "1A", "TO-220", "ST", "positive regulator"],
    },
    "UA78GU1C": {
        "name": "UA78GU1C",
        "manufacturer": "Texas Instruments",
        "specs": {
            "Vout": "+5 till +30V justerbar",
            "Iout_max": "1A",
            "Vin_min": "Vout + 2V",
            "Vin_max": "40V",
            "adjust_range": "5–30V",
            "package": "TO-66",
            "polarity": "positiv justerbar",
        },
        "desc": (
            "Justerbar positiv spänningsregulator +5 till +30 V, 1 A (Texas Instruments UA78G). "
            "Utgångsspänningen ställs in med en extern spänningsdelare. "
            "U1C-suffix anger paketet TO-66 (metallkapsel). "
            "Intern referens 5 V; Vin måste vara minst 2 V över Vout. "
            "Föregångare till LM317 med fast 5 V-referens istället för 1,25 V."
        ),
        "tags": ["UA78GU1C", "UA78G", "adjustable regulator", "justerbar regulator", "TO-66", "TI", "positive regulator"],
    },
    "TL783C": {
        "name": "TL783C",
        "manufacturer": "Texas Instruments",
        "specs": {
            "Vout": "+1.25 till +125V justerbar",
            "Iout_max": "700mA",
            "Vin_max": "125V över Vout (max 150V)",
            "dropout": "~2.5V",
            "adjust_range": "1.25–125V",
            "package": "TO-220",
            "polarity": "positiv justerbar",
        },
        "desc": (
            "Justerbar högspänningsregulator +1,25 till +125 V, 700 mA, TO-220 (Texas Instruments TL783). "
            "Klarar ingångsspänningar upp till 125 V över Vout (max 150 V). "
            "Utgångsspänningen ställs med extern spänningsdelare (liknande LM317 men för höga spänningar). "
            "Intern referens 1,25 V. C-suffix = kommersiell temperaturklass. "
            "Används i högspänningskällor, laboratorieaggregat och nixierörskretsar."
        ),
        "tags": ["TL783C", "TL783", "high voltage regulator", "adjustable regulator", "justerbar regulator", "125V", "TO-220", "TI"],
    },
}

# F0188 är tomt fack – hoppas över
LAYOUT = [
    (177, "78L05"),
    (178, "L7805CV"),
    (179, "7805"),
    (180, "79M05AHC"),
    (181, "TS7809"),
    (182, "L78S12CV"),
    (183, "7812C"),
    (184, "LM340T12"),
    (185, "GL7915"),
    (186, "L7818CV"),
    (187, "L7812CV"),
    # (188, tomt)
    (189, "UA78GU1C"),
    (190, "TL783C"),
]

DRAWER_LABEL = "L20"
CATEGORY_NAME = "Spänningsregulatorer"
CATEGORY_SLUG = "spanningsregulatorer"


def get_or_create_category(categories):
    match = next((c for c in categories if c["slug"] == CATEGORY_SLUG), None)
    if match:
        print(f"  Kategori '{CATEGORY_NAME}' finns redan (id={match['id']})")
        return match["id"]
    result, status = api_post("/api/categories", {
        "name": CATEGORY_NAME,
        "slug": CATEGORY_SLUG,
        "parent_id": None,
    })
    if result:
        print(f"  Skapade kategori '{CATEGORY_NAME}' (id={result['id']})")
        return result["id"]
    print(f"FEL: Kunde inte skapa kategori (status={status})", file=sys.stderr)
    return None


def main():
    print("=== KOMPIS L20 Spänningsregulatorer ===\n")

    print("Hämtar kategorier...")
    categories = api_get("/api/categories")
    if not categories:
        print("FEL: Kan inte hämta kategorier.", file=sys.stderr)
        sys.exit(1)

    cat_id = get_or_create_category(categories)
    if not cat_id:
        sys.exit(1)

    print(f"\nSöker efter låda {DRAWER_LABEL}...")
    drawers = api_get("/api/drawers")
    drawer = next((d for d in drawers if d["label"] == DRAWER_LABEL), None)
    if not drawer:
        print(f"FEL: Hittade inte {DRAWER_LABEL}!", file=sys.stderr)
        sys.exit(1)
    drawer_id = drawer["id"]
    print(f"  {DRAWER_LABEL} id={drawer_id}")

    print(f"\nHämtar befintliga fack...")
    drawer_detail = api_get(f"/api/drawers/{drawer_id}")
    existing = {c["label"]: c["id"] for c in (drawer_detail or {}).get("compartments", [])}

    print(f"\nSkapar fack F0177–F0190 (F0188 hoppas över – tomt)...")
    compartment_ids = {}
    for fack_num, _ in LAYOUT:
        label = f"F{fack_num:04d}"
        if label in existing:
            compartment_ids[fack_num] = existing[label]
            continue
        result, status = api_post("/api/compartments", {
            "drawer_id": drawer_id, "label": label, "description": None,
        })
        if result:
            compartment_ids[fack_num] = result["id"]
            print(f"  Skapade {label} (id={result['id']})")
        else:
            print(f"  FEL: {label} (status={status})", file=sys.stderr)

    # Skapa även F0188 som tomt fack
    label_188 = "F0188"
    if label_188 not in existing:
        api_post("/api/compartments", {"drawer_id": drawer_id, "label": label_188, "description": "Tomt fack"})
        print(f"  Skapade {label_188} (tomt)")

    print(f"\nSkapar komponenter...")
    created = {}
    for fack_num, key in LAYOUT:
        if key in created:
            continue
        comp = COMPONENTS[key]
        target_name = comp["name"]

        existing_comps = api_get(f"/api/components?q={urllib.parse.quote(target_name)}&limit=20")
        if existing_comps:
            match = next((c for c in existing_comps if c["name"].lower() == target_name.lower()), None)
            if match:
                created[key] = match["id"]
                print(f"  [{match['id']:4d}] {target_name} (finns redan)")
                continue

        result, status = api_post("/api/components", {
            "name": target_name,
            "description": comp["desc"],
            "category_id": cat_id,
            "manufacturer": comp.get("manufacturer"),
            "part_number": None,
            "tags": comp.get("tags") or None,
            "specs": comp.get("specs") or None,
        })
        if result:
            created[key] = result["id"]
            print(f"  [{result['id']:4d}] {target_name} (ny)")
        else:
            print(f"  FEL: '{target_name}' (status={status})", file=sys.stderr)

    print(f"\nSkapar lagerplatser...")
    stock_count = 0
    for fack_num, key in LAYOUT:
        if key not in created or fack_num not in compartment_ids:
            continue
        result, status = api_post("/api/stock", {
            "component_id": created[key],
            "compartment_id": compartment_ids[fack_num],
            "quantity": 1, "minimum_qty": 0, "unit": "st", "notes": None,
        })
        if result:
            stock_count += 1
        elif status != 422:
            print(f"  FEL: lager F{fack_num:04d} (status={status})", file=sys.stderr)

    print(f"  {stock_count} lagerplatser skapade")
    print(f"\nKLART! {len(created)} komponenter, kategori '{CATEGORY_NAME}' skapad.")


if __name__ == "__main__":
    main()
