#!/usr/bin/env python3
"""Seed drawer L05 with new compartments F1001-F1032.

Run on rash:
  python3 scripts/seed_l05_new.py
"""
import json, sys, urllib.request, urllib.error, urllib.parse

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
    req = urllib.request.Request(f"{BASE}{path}", data=body,
                                  headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        print(f"POST {path} → {e.code}: {e.read()[:200]}", file=sys.stderr)
        return None, e.code

# cat_id 1=Transistorer, 6=Timer och oscillator
COMPONENTS = {
    "Okänd_F1001": {
        "name": "Okänd (F1001)",
        "cat": 1,
        "manufacturer": None,
        "specs": {},
        "desc": "Okänd komponent i fack F1001. Beteckning och funktion har ej kunnat identifieras.",
        "tags": [],
    },
    "AD131": {
        "name": "AD131",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "PNP", "material": "Ge", "Vceo": "-32V", "Ic_max": "3A",
                  "Pt_max": "15W", "package": "TO-3"},
        "desc": ("Germanium PNP effekttransistor ur den europeiska AD-serien. "
                 "Äldre komponent med låg spänning och medium effekt. "
                 "Används i vintage-förstärkare och analogelektronik."),
        "tags": ["AD131", "germanium", "PNP", "TO-3"],
    },
    "MJ2955": {
        "name": "MJ2955",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "PNP", "material": "Si", "Vceo": "-60V", "Ic_max": "-15A",
                  "Pt_max": "115W", "hFE": "20-70", "package": "TO-3"},
        "desc": ("PNP komplementtransistor till 2N3055. Silicon, TO-3. "
                 "115 W effektutveckling med heatsink. Används i symmetriska "
                 "effektsteg och spänningsregulatorer med hög strömkapacitet."),
        "tags": ["MJ2955", "PNP", "power transistor", "TO-3", "complement 2N3055"],
    },
    "BDX92": {
        "name": "BDX92",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "PNP Darlington", "material": "Si", "Vceo": "-80V",
                  "Ic_max": "-8A", "Pt_max": "60W", "package": "TO-66"},
        "desc": ("PNP Darlington-effekttransistor. TO-66. Hög strömförstärkning tack vare "
                 "Darlington-kopplingen. Används i motorstyrning och effektdrivkretsar."),
        "tags": ["BDX92", "PNP", "darlington", "TO-66"],
    },
    "2N4912": {
        "name": "2N4912",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "Vceo": "80V", "Ic_max": "15A",
                  "Pt_max": "100W", "package": "TO-3"},
        "desc": ("NPN kisel-effekttransistor. TO-3. Vceo 80 V, 15 A, 100 W. "
                 "Används i effektsteg och switchande applikationer."),
        "tags": ["2N4912", "NPN", "power transistor", "TO-3"],
    },
    "2N3767": {
        "name": "2N3767",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "Vceo": "60V", "Ic_max": "15A",
                  "Pt_max": "117W", "package": "TO-3"},
        "desc": ("NPN kisel-effekttransistor. TO-3, 60 V, 15 A. "
                 "Äldre komponent för effektsteg och motorstyrning."),
        "tags": ["2N3767", "NPN", "power transistor", "TO-3"],
    },
    "ASZ16": {
        "name": "ASZ16",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "PNP", "material": "Ge", "Vceo": "-32V", "Ic_max": "-5A",
                  "Pt_max": "25W", "package": "TO-3"},
        "desc": ("Germanium PNP effekttransistor ur ASZ-serien. TO-3 metallkapsel. "
                 "Liknande ASZ18 men med lägre max-ström. "
                 "Används i vintage-förstärkareprojekt och restaureringsarbeten."),
        "tags": ["ASZ16", "germanium", "PNP", "TO-3"],
    },
    "MJ4030": {
        "name": "MJ4030",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "NPN Darlington", "material": "Si", "Vceo": "60V",
                  "Ic_max": "8A", "Pt_max": "50W", "package": "TO-3"},
        "desc": ("NPN Darlington effekttransistor. TO-3. "
                 "Hög strömförstärkning (Darlington) och 60 V spänning. "
                 "Typisk användning: motorstyrning, relädrivning, effektsteg."),
        "tags": ["MJ4030", "NPN", "darlington", "TO-3"],
    },
    "2N4347": {
        "name": "2N4347",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "Vceo": "350V", "Ic_max": "10A",
                  "Pt_max": "150W", "package": "TO-3"},
        "desc": ("Högspännings-NPN kisel-effekttransistor. TO-3, Vceo 350 V, 10 A. "
                 "Används i switchade nätaggregat och drivkretsar för höga spänningar."),
        "tags": ["2N4347", "NPN", "high voltage", "power transistor", "TO-3"],
    },
    "MJ15004": {
        "name": "MJ15004",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "NPN", "material": "Si", "Vceo": "140V", "Ic_max": "15A",
                  "Pt_max": "150W", "hFE": "25-100", "package": "TO-3"},
        "desc": ("NPN audioeffekttransistor. TO-3, 140 V, 15 A. "
                 "Komplementparet MJ15003/MJ15004 är klassiska val för "
                 "hifi-effektsteg (Class AB). Lågt brus och god linjäritet."),
        "tags": ["MJ15004", "NPN", "audio", "power transistor", "TO-3", "hifi"],
    },
    "MJ15003": {
        "name": "MJ15003",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "PNP", "material": "Si", "Vceo": "-140V", "Ic_max": "-15A",
                  "Pt_max": "150W", "hFE": "25-100", "package": "TO-3"},
        "desc": ("PNP audioeffekttransistor, komplement till MJ15004. TO-3, -140 V, -15 A. "
                 "Klassisk komponent i hifi-slutsteg. Används i par med MJ15004 "
                 "för symmetrisk Class-AB-drift."),
        "tags": ["MJ15003", "PNP", "audio", "power transistor", "TO-3", "hifi",
                 "complement MJ15004"],
    },
    "2N5886": {
        "name": "2N5886",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "PNP", "material": "Si", "Vceo": "-80V", "Ic_max": "-15A",
                  "Pt_max": "150W", "package": "TO-3"},
        "desc": ("PNP kisel-effekttransistor. TO-3, -80 V, -15 A. "
                 "Komplement till 2N5885 (NPN). Används i symmetriska effektsteg "
                 "och spänningsregulatorer."),
        "tags": ["2N5886", "PNP", "power transistor", "TO-3"],
    },
    "MJ3001": {
        "name": "MJ3001",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "NPN Darlington", "material": "Si", "Vceo": "80V",
                  "Ic_max": "10A", "Pt_max": "80W", "hFE_min": 750, "package": "TO-3"},
        "desc": ("NPN Darlington effekttransistor. TO-3, 80 V, 10 A. "
                 "Mycket hög strömförstärkning (hFE >750). "
                 "Används för relädrivning, motorstyrning och effektsteg med "
                 "logik- eller mikrokontrollerstyrning."),
        "tags": ["MJ3001", "NPN", "darlington", "TO-3"],
    },
    "2N3631": {
        "name": "2N3631",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "Vceo": "80V", "Ic_max": "1A",
                  "package": "TO-39"},
        "desc": ("NPN kisel-transistor, medeleffekt. TO-39 metallkapsel. "
                 "Vceo 80 V. Används i drivsteg och reläkretsar."),
        "tags": ["2N3631", "NPN", "TO-39"],
    },
    "2N3773": {
        "name": "2N3773",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "NPN", "material": "Si", "Vceo": "160V", "Ic_max": "16A",
                  "Pt_max": "150W", "package": "TO-3"},
        "desc": ("NPN kisel-effekttransistor för audio. TO-3, 160 V, 16 A. "
                 "Vanlig i hifi-slutsteg med höga matningsspänningar. "
                 "Komplementparet är 2N3771 (PNP)."),
        "tags": ["2N3773", "NPN", "audio", "power transistor", "TO-3", "hifi"],
    },
    "BDX67C": {
        "name": "BDX67C",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN Darlington", "material": "Si", "Vceo": "100V",
                  "Ic_max": "8A", "Pt_max": "60W", "package": "TO-3"},
        "desc": ("NPN Darlington effekttransistor (C-variant = högre spänning). "
                 "TO-3, 100 V, 8 A. Intern basmotstånd och skyddsdiod. "
                 "Används i motorstyrning och effektregulering."),
        "tags": ["BDX67C", "BDX67", "NPN", "darlington", "TO-3"],
    },
    "TIP33": {
        "name": "TIP33",
        "cat": 1,
        "manufacturer": "Texas Instruments",
        "specs": {"type": "NPN", "material": "Si", "Vceo": "60V", "Ic_max": "10A",
                  "Pt_max": "80W", "package": "TO-218"},
        "desc": ("NPN kisel-effekttransistor. TO-218, 60 V, 10 A. "
                 "Grundvarianten av TIP33-serien (TIP33A/B/C). "
                 "Används i effektsteg, motorstyrning och switchande kretsar."),
        "tags": ["TIP33", "NPN", "power transistor", "TO-218", "TI"],
    },
    "TIP35C": {
        "name": "TIP35C",
        "cat": 1,
        "manufacturer": "Texas Instruments",
        "specs": {"type": "NPN", "material": "Si", "Vceo": "100V", "Ic_max": "25A",
                  "Pt_max": "125W", "package": "TO-218"},
        "desc": ("NPN kisel-effekttransistor (C = 100 V-variant). TO-218, 100 V, 25 A. "
                 "Komplementparet är TIP36C (PNP). Används i hifi-slutsteg "
                 "och switchade nätaggregat med höga strömmar."),
        "tags": ["TIP35C", "TIP35", "NPN", "power transistor", "TO-218", "TI"],
    },
    "TIP140": {
        "name": "TIP140",
        "cat": 1,
        "manufacturer": "Texas Instruments",
        "specs": {"type": "NPN Darlington", "material": "Si", "Vceo": "60V",
                  "Ic_max": "10A", "Pt_max": "125W", "hFE_min": 1000, "package": "TO-218"},
        "desc": ("NPN Darlington effekttransistor. TO-218, 60 V, 10 A. "
                 "hFE >1000 tack vare Darlington-kopplingen. "
                 "Inbyggd flyback-diod. Komplement: TIP145 (PNP). "
                 "Vanlig i motorstyrning och reläkretsar drivna från logik."),
        "tags": ["TIP140", "NPN", "darlington", "TO-218", "TI"],
    },
    "TIP36C": {
        "name": "TIP36C",
        "cat": 1,
        "manufacturer": "Texas Instruments",
        "specs": {"type": "PNP", "material": "Si", "Vceo": "-100V", "Ic_max": "-25A",
                  "Pt_max": "125W", "package": "TO-218"},
        "desc": ("PNP kisel-effekttransistor, komplement till TIP35C. TO-218, -100 V, -25 A. "
                 "Används i symmetriska hifi-slutsteg och switchade kretsar "
                 "med höga strömmar."),
        "tags": ["TIP36C", "TIP36", "PNP", "power transistor", "TO-218", "TI",
                 "complement TIP35C"],
    },
    "2N1596": {
        "name": "2N1596",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "SCR", "Vdrm": "200V", "It_av": "1.6A", "package": "TO-48"},
        "desc": ("Silicon Controlled Rectifier (SCR/tyristor), inte en bipolär transistor. "
                 "Vdrm 200 V, genomsnittlig framåtström 1,6 A. TO-48 metallkapsel. "
                 "Används för fasreglering av AC och motorhastighetsstyrning."),
        "tags": ["2N1596", "SCR", "thyristor", "silicon controlled rectifier", "TO-48"],
    },
    "2N2907A": {
        "name": "2N2907A",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "PNP", "material": "Si", "Vceo": "-60V", "Ic_max": "-600mA",
                  "Pt_max": "625mW", "hFE": "100-300", "fT": "200MHz", "package": "TO-18"},
        "desc": ("PNP small-signal transistor, TO-18. Klassisk komponent; "
                 "komplement till 2N2222. Vceo -60 V, 600 mA. "
                 "Allround-transistor för drivsteg, inverterkretsar och analogbearbetning."),
        "tags": ["2N2907A", "2N2907", "PNP", "small signal", "TO-18"],
    },
    "BC147B": {
        "name": "BC147B",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "Vceo": "45V", "Ic_max": "100mA",
                  "Pt_max": "300mW", "hFE": "220-460", "package": "TO-18"},
        "desc": ("NPN small-signal transistor, TO-18. B-suffixet anger hög förstärkning "
                 "(hFE 220–460). Vceo 45 V, 100 mA. "
                 "Används i lågbrusförstärkare, drivsteg och switchande kretsar."),
        "tags": ["BC147B", "BC147", "NPN", "small signal", "TO-18", "high gain"],
    },
    "BC141-10": {
        "name": "BC141-10",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "Vceo": "60V", "Ic_max": "1A",
                  "Pt_max": "8W", "hFE_min": 10, "package": "TO-39"},
        "desc": ("NPN medeleffekt transistor, TO-39. Suffixet -10 anger "
                 "lägre förstärkningsklass (hFE min 10). Vceo 60 V, 1 A, 8 W. "
                 "Används i drivsteg och analoga effektkretsar."),
        "tags": ["BC141-10", "BC141", "NPN", "TO-39"],
    },
    "2N4899": {
        "name": "2N4899",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "PNP", "material": "Si", "package": "TO-3"},
        "desc": ("PNP kisel-effekttransistor. TO-3. "
                 "Detaljerade specs ej verifierade – kontrollera databladet vid användning."),
        "tags": ["2N4899", "PNP", "TO-3"],
    },
    "2N3741": {
        "name": "2N3741",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "Vceo": "40V", "Ic_max": "10A",
                  "Pt_max": "87W", "package": "TO-3"},
        "desc": ("NPN kisel-effekttransistor. TO-3, 40 V, 10 A. "
                 "Lägre spänning men hög ström, lämpad för "
                 "motorstyrning och linjära effektreglatorer."),
        "tags": ["2N3741", "NPN", "power transistor", "TO-3"],
    },
    "2N3772": {
        "name": "2N3772",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "NPN", "material": "Si", "Vceo": "40V", "Ic_max": "20A",
                  "Pt_max": "150W", "package": "TO-3"},
        "desc": ("NPN kisel-effekttransistor. TO-3, 40 V, 20 A, 150 W. "
                 "Hög strömkapacitet med låg Vceo. "
                 "Komplement: 2N3740 (PNP). Används i effektsteg med låga spänningar."),
        "tags": ["2N3772", "NPN", "power transistor", "TO-3"],
    },
    "2N5631": {
        "name": "2N5631",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "package": "TO-3"},
        "desc": ("NPN kisel-effekttransistor. TO-3. "
                 "Detaljerade specs ej verifierade – kontrollera databladet vid användning."),
        "tags": ["2N5631", "NPN", "TO-3"],
    },
    "RCA40409": {
        "name": "RCA 40409",
        "cat": 1,
        "manufacturer": "RCA",
        "specs": {"type": "NPN", "material": "Si", "package": "TO-66"},
        "desc": ("NPN kisel-transistor från RCAs 40xxx-serie. TO-66 metallkapsel. "
                 "RCA:s 40xxx-transistorer var vanliga i konsumentelektronik under "
                 "1970–80-talen. Specs bör verifieras mot RCA-databladet."),
        "tags": ["RCA40409", "40409", "RCA", "NPN", "TO-66"],
    },
    "MC1455G": {
        "name": "MC1455G",
        "cat": 6,   # Timer och oscillator
        "manufacturer": "Motorola",
        "specs": {"technology": "bipolar", "package": "DIP-8", "Vcc": "5-15V",
                  "pins": 8, "channels": 1},
        "desc": ("555-kompatibel timer (Motorola MC1455, DIP-8). "
                 "Funktionellt identisk med NE555/LM555. "
                 "Mono- och astabilt läge. Placerad i L05 – tillhör egentligen IC-kategorin."),
        "tags": ["MC1455G", "MC1455", "555", "timer", "Motorola", "555 compatible"],
    },
    "2N3054": {
        "name": "2N3054",
        "cat": 1,
        "manufacturer": "ON Semiconductor",
        "specs": {"type": "NPN", "material": "Si", "Vceo": "60V", "Ic_max": "4A",
                  "Pt_max": "40W", "hFE": "20-100", "package": "TO-66"},
        "desc": ("NPN kisel-effekttransistor. TO-66 metallkapsel, 60 V, 4 A. "
                 "Klassisk komponent från 1960-talet. Används i linjära "
                 "effektsteg och drivkretsar för medelstora laster."),
        "tags": ["2N3054", "NPN", "power transistor", "TO-66"],
    },
    "2N4911": {
        "name": "2N4911",
        "cat": 1,
        "manufacturer": None,
        "specs": {"type": "NPN", "material": "Si", "package": "TO-3"},
        "desc": ("NPN kisel-transistor. TO-3. "
                 "Detaljerade specs ej verifierade – kontrollera databladet vid användning."),
        "tags": ["2N4911", "NPN", "TO-3"],
    },
}

LAYOUT = [
    (1001, "Okänd_F1001"),
    (1002, "AD131"),
    (1003, "MJ2955"),
    (1004, "BDX92"),
    (1005, "2N4912"),
    (1006, "2N3767"),
    (1007, "ASZ16"),
    (1008, "MJ4030"),
    (1009, "2N4347"),
    (1010, "MJ15004"),
    (1011, "MJ15003"),
    (1012, "2N5886"),
    (1013, "MJ3001"),
    (1014, "2N3631"),
    (1015, "2N3773"),
    (1016, "BDX67C"),
    (1017, "TIP33"),
    (1018, "TIP35C"),
    (1019, "TIP140"),
    (1020, "TIP36C"),
    (1021, "2N1596"),
    (1022, "2N2907A"),
    (1023, "BC147B"),
    (1024, "BC141-10"),
    (1025, "2N4899"),
    (1026, "2N3741"),
    (1027, "2N3772"),
    (1028, "2N5631"),
    (1029, "RCA40409"),
    (1030, "MC1455G"),
    (1031, "2N3054"),
    (1032, "2N4911"),
]

DRAWER_LABEL = "L05"


def main():
    print("=== KOMPIS L05 (F1001-F1032) Seeding Script ===\n")

    categories = api_get("/api/categories")
    if not categories:
        print("FEL: Kan inte hämta kategorier.", file=sys.stderr)
        import sys; sys.exit(1)

    drawers = api_get("/api/drawers")
    drawer = next((d for d in drawers if d["label"] == DRAWER_LABEL), None)
    if not drawer:
        print(f"FEL: Hittade inte {DRAWER_LABEL}!", file=sys.stderr)
        import sys; sys.exit(1)
    drawer_id = drawer["id"]
    print(f"Låda {DRAWER_LABEL} id={drawer_id}")

    drawer_detail = api_get(f"/api/drawers/{drawer_id}")
    existing = {c["label"]: c["id"] for c in (drawer_detail or {}).get("compartments", [])}

    print("\nSkapar fack F1001-F1032...")
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

        specs = {k: v for k, v in (comp.get("specs") or {}).items()}
        result, status = api_post("/api/components", {
            "name": target_name,
            "description": comp["desc"],
            "category_id": comp["cat"],
            "manufacturer": comp.get("manufacturer"),
            "part_number": None,
            "tags": comp.get("tags") or None,
            "specs": specs or None,
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
    print(f"\nKLART! {len(created)} komponenter i {len(compartment_ids)} fack i {DRAWER_LABEL}.")
    print("\nOBS:")
    print("  F1001 – Okänd komponent, identifiera och uppdatera manuellt.")
    print("  F1021 – 2N1596 är en SCR (tyristor), inte bipolär transistor.")
    print("  F1030 – MC1455G är en 555-timer (Motorola), kategoriserad som Timer.")


if __name__ == "__main__":
    main()
