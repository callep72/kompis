#!/usr/bin/env python3
"""Seed drawer L20 (F0129-F0169) with IC components.

Run on rash:
  python3 scripts/seed_l20.py
Or via Docker:
  docker compose exec app python3 scripts/seed_l20.py
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
        body = e.read()
        print(f"POST {path} → {e.code}: {body[:200]}", file=sys.stderr)
        return None, e.code


COMPONENTS = {

    # ---- TTL LS Logic ----
    "74LS74": {
        "name": "74LS74",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel D-vippa med preset och clear. Positiv flankstyrning. "
                "LS-variant av SN7474; används för datalagring och sekvenslogik.",
        "tags": ["74LS74", "dual D flip-flop", "D-vippa", "TTL LS"],
    },
    "74LS85": {
        "name": "74LS85",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "4-bitars magnitydkomparator. Jämför två 4-bitars tal A och B och ger ut A>B, A=B, A<B. "
                "Kan kaskadkopplas för bredare komparatorer.",
        "tags": ["74LS85", "magnitude comparator", "4-bit comparator"],
    },
    "74107": {
        "name": "74107",
        "cat_hint": "digital",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel JK master-slave-vippa med clear. Negativ flankstyrning på klockan. "
                "Inbyggd aktiv-låg clear. Standard TTL-version.",
        "tags": ["74107", "dual JK flip-flop", "JK-vippa", "TTL"],
    },
    "7417": {
        "name": "7417",
        "cat_hint": "digital",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14,
                  "output": "open-collector", "output_voltage": "30V max"},
        "desc": "Hex buffer/drivare med open-collector-utgångar (ej inverterande). "
                "Utgångarna tål upp till 30 V och 40 mA. Används för nivåanpassning och drivning av reläer, LED-displayer m.m.",
        "tags": ["7417", "SN7417", "hex buffer", "open collector"],
    },
    "74LS368A": {
        "name": "74LS368A",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16,
                  "output": "3-state"},
        "desc": "Hex inverterande bussdrivare med 3-state-utgångar. "
                "Två oberoende enable-grupper (G1 styr 4 buffertar, G2 styr 2). "
                "Används som databuss-buffer med möjlighet att koppla ut (tri-state).",
        "tags": ["74LS368", "74LS368A", "hex inverting buffer", "3-state", "bus driver"],
    },
    "74LS71": {
        "name": "74LS71",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "AND-OR-grind JK master-slave-vippa med preset. "
                "Ingångarna har AND-OR-grind-logik före JK-vippan. "
                "Negativ flankstyrning.",
        "tags": ["74LS71", "AND-OR gated JK", "JK flip-flop", "TTL LS"],
    },
    "74LS161": {
        "name": "74LS161",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "Synkron 4-bitars binärräknare med asynkron clear och parallell load. "
                "Räknar upp vid positiv klockflank. Ripple-carry-utgång för kaskadkoppling. "
                "Skillnad mot 74LS163: clear är asynkron.",
        "tags": ["74LS161", "4-bit counter", "binary counter", "TTL LS"],
    },
    "7497": {
        "name": "7497",
        "cat_hint": "digital",
        "specs": {"technology": "TTL", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "6-bitars binär hastighetsmultiplexer. "
                "Genererar en utgångspulsfrekvens som är en bråkdel (N/64) av ingångsfrekvensen. "
                "Används i digitala frekvenssynteser och tidsbas-kretsar.",
        "tags": ["7497", "SN7497", "rate multiplier", "frequency divider", "TTL"],
    },
    "74LS365": {
        "name": "74LS365",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16,
                  "output": "3-state"},
        "desc": "Hex bussdrivare med 3-state-utgångar (ej inverterande). "
                "6 buffertar med gemensam output-enable. Icke-inverterande variant; "
                "jämför 74LS368 (inverterande).",
        "tags": ["74LS365", "hex buffer", "3-state", "bus driver", "TTL LS"],
    },
    "74LS00": {
        "name": "74LS00",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Fyra 2-ingångs NAND-grindar. Grundläggande LS-TTL-logikgrind. "
                "Standard pinout, pin-kompatibel med 7400, 74HC00 m.fl.",
        "tags": ["74LS00", "7400", "quad NAND", "NAND gate", "TTL LS"],
    },
    "74LS163": {
        "name": "74LS163",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "Synkron 4-bitars binärräknare med synkron clear och parallell load. "
                "Räknar upp vid positiv klockflank. Ripple-carry-utgång. "
                "Skillnad mot 74LS161: clear är synkron (sker vid nästa klockflank).",
        "tags": ["74LS163", "4-bit counter", "binary counter", "synchronous clear", "TTL LS"],
    },
    "74LS374": {
        "name": "74LS374",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-20", "Vcc": "5V", "pins": 20,
                  "output": "3-state"},
        "desc": "Oktal D-vippa med 3-state-utgångar. 8 positiv-flankstyrda D-vippor "
                "med gemensam klocka och output-enable. Liknar 74LS373 men flankstyrda "
                "istället för nivåstyrda (latch).",
        "tags": ["74LS374", "octal D flip-flop", "3-state", "TTL LS"],
    },
    "74LS05": {
        "name": "74LS05",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14,
                  "output": "open-collector"},
        "desc": "Hex inverter med open-collector-utgångar. "
                "Inverterar signalen; OC-utgångar möjliggör wired-AND-koppling "
                "och anslutning till högre spänningsnivåer via pull-up.",
        "tags": ["74LS05", "hex inverter", "open collector", "TTL LS"],
    },
    "74LS10": {
        "name": "74LS10",
        "cat_hint": "digital",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Trippel 3-ingångs NAND-grind (LS-variant). "
                "Tre oberoende NAND-grindar med 3 ingångar vardera. "
                "LS-versionen av SN7410.",
        "tags": ["74LS10", "triple NAND", "3-input NAND", "TTL LS"],
    },
    "7420": {
        "name": "7420",
        "cat_hint": "digital",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel 4-ingångs NAND-grind (standard TTL). "
                "Två oberoende 4-ingångs NAND-grindar.",
        "tags": ["7420", "SN7420", "dual 4-input NAND", "TTL"],
    },

    # ---- TTL övrigt / oklara ----
    "SN49701AN": {
        "name": "SN49701AN",
        "cat_hint": "digital",
        "specs": {"technology": "TTL", "package": "DIP-16", "Vcc": "5V", "pins": 16,
                  "manufacturer": "Texas Instruments"},
        "desc": "Texas Instruments SN49701AN, DIP-16. "
                "Funktion ej verifierad – troligen logik- eller bussdrivare-IC ur TI:s 490x-serie. "
                "Tillverkad i Tyskland (datumkod 439X).",
        "tags": ["SN49701AN", "TI", "Texas Instruments"],
    },
    "DM8602N": {
        "name": "DM8602N",
        "cat_hint": "digital",
        "specs": {"technology": "TTL high-speed", "package": "DIP-16", "Vcc": "5V", "pins": 16,
                  "manufacturer": "SGS"},
        "desc": "SGS (STMicroelectronics) DM8602N, höghastighets-TTL, DIP-16. "
                "Ur National Semiconductor DM8xxx-serien, tillverkad av SGS (datumkod P206, 1996). "
                "Exakt funktion ej verifierad.",
        "tags": ["DM8602N", "DM8602", "SGS", "high-speed TTL"],
    },

    # ---- CMOS ----
    "CD4028": {
        "name": "CD4028",
        "cat_hint": "mux",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16",
                  "Vcc": "3-18V", "pins": 16},
        "desc": "BCD-till-decimal-dekoder (1-av-10). Avkodar 4-bitars BCD-ingång "
                "till en aktiv-hög utgång (0–9). Ingångskoder 10–15 ger alla utgångar låga.",
        "tags": ["4028", "CD4028", "BCD decoder", "1-of-10", "CMOS"],
    },
    "CD4723BCN": {
        "name": "CD4723BCN",
        "cat_hint": "digital",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16",
                  "Vcc": "3-18V", "pins": 16, "manufacturer": "National Semiconductor"},
        "desc": "Dubbelt 4-bitars adresserbart latch (MM4723/CD4723). "
                "Varje sektion har 4 latchade utgångar som adresseras individuellt "
                "via en 2-bitars adress. Kan skriva till en bit utan att påverka övriga. "
                "Funktionellt lik två halverade CD4099.",
        "tags": ["CD4723", "MM4723", "CD4723BCN", "addressable latch", "4-bit latch", "CMOS"],
    },
    "CD4070": {
        "name": "CD4070",
        "cat_hint": "digital",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14",
                  "Vcc": "3-18V", "pins": 14},
        "desc": "Fyra 2-ingångs XOR-grindar (CMOS). "
                "Identisk funktion med CD4030. Används för paritetsgenerering, "
                "jämförelse och enkel addition.",
        "tags": ["4070", "CD4070", "quad XOR", "XOR gate", "CMOS"],
    },
    "CD4030": {
        "name": "CD4030",
        "cat_hint": "digital",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14",
                  "Vcc": "3-18V", "pins": 14},
        "desc": "Fyra 2-ingångs XOR-grindar (CMOS). "
                "Funktionellt identisk med CD4070. Äldre beteckning i 4000-serien.",
        "tags": ["4030", "CD4030", "quad XOR", "XOR gate", "CMOS"],
    },
    "CD4076": {
        "name": "CD4076",
        "cat_hint": "digital",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16",
                  "Vcc": "3-18V", "pins": 16, "output": "3-state"},
        "desc": "Fyra D-vippor med 3-state-utgångar. "
                "Positiv flankstyrning, gemensam klocka och reset. "
                "3-state-utgångarna möjliggör direkt bussanslutning.",
        "tags": ["4076", "CD4076", "quad D register", "3-state", "CMOS"],
    },
    "CD4019": {
        "name": "CD4019",
        "cat_hint": "digital",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16",
                  "Vcc": "3-18V", "pins": 16},
        "desc": "Quad AND-OR-väljare. Fyra sektioner där varje sektion väljer "
                "mellan ingång A eller B via en gemensam select-signal (Ka/Kb). "
                "Kan konfigurera logikfunktioner dynamiskt.",
        "tags": ["4019", "CD4019", "AND-OR select", "quad selector", "CMOS"],
    },
    "CD40105": {
        "name": "CD40105",
        "cat_hint": "digital",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16",
                  "Vcc": "3-15V", "pins": 16},
        "desc": "4-bitars FIFO-register (16 djupt). "
                "First-in first-out-minne med 4-bitars bredd och 16 positioner djup. "
                "Asynkront; separata läs- och skrivklockor. Används för dataköer.",
        "tags": ["40105", "CD40105", "FIFO", "4-bit FIFO", "CMOS"],
    },

    # ---- Minnen ----
    "6264": {
        "name": "6264",
        "cat_hint": "minne",
        "specs": {"technology": "CMOS SRAM", "package": "DIP-28", "Vcc": "5V", "pins": 28,
                  "capacity": "8K×8 bit", "access_time": "100ns"},
        "desc": "8K×8 statiskt RAM (64Kbit CMOS SRAM). "
                "Standard 6264-pinout; kompatibel med HM6264, HM6264LP, CY6264 m.fl. "
                "Batterisäkerhetskopierbar. Vanlig i äldre datorer och inbyggda system.",
        "tags": ["6264", "SRAM", "8Kx8", "static RAM", "64Kbit"],
    },
    "HM6116AP-15": {
        "name": "HM6116AP-15",
        "cat_hint": "minne",
        "specs": {"technology": "CMOS SRAM", "package": "DIP-24", "Vcc": "5V", "pins": 24,
                  "capacity": "2K×8 bit", "access_time": "150ns", "manufacturer": "Hitachi"},
        "desc": "2K×8 statiskt CMOS-RAM (16Kbit), 150 ns åtkomsttid (AP-15-suffixet). "
                "Standard pinout, kompatibel med 6116-familjen. "
                "Lägre strömförbrukning än bipolär SRAM. Hitachi-tillverkat.",
        "tags": ["HM6116", "HM6116AP", "6116", "SRAM", "2Kx8", "Hitachi"],
    },

    # ---- Mikrokontroller-periferi ----
    "D8251AC": {
        "name": "D8251AC",
        "cat_hint": "mikro",
        "specs": {"technology": "NMOS", "package": "DIP-28", "Vcc": "5V", "pins": 28,
                  "manufacturer": "NEC", "interface": "USART"},
        "desc": "Programmerbart kommunikationsgränssnitt USART (NEC D8251AC, kompatibel med Intel 8251A). "
                "Stöder synkron och asynkron seriell kommunikation, full-duplex. "
                "Används i 8080/8085-baserade system för UART-kommunikation.",
        "tags": ["D8251AC", "8251", "8251A", "USART", "serial", "NEC", "Intel 8251"],
    },
    "INS8154": {
        "name": "INS8154",
        "cat_hint": "mikro",
        "specs": {"technology": "NMOS", "package": "DIP-40", "Vcc": "5V", "pins": 40,
                  "manufacturer": "National Semiconductor", "ram": "128 bytes"},
        "desc": "RAM I/O-krets (National Semiconductor INS8154). "
                "Innehåller 128 bytes statiskt RAM och två 8-bitars I/O-portar (Port A och B) "
                "med individuellt konfigurerbar riktning per bit. "
                "Ansluts direkt till 8080/8085-bussen.",
        "tags": ["INS8154", "8154", "RAM IO", "National Semiconductor", "8085 peripheral"],
    },

    # ---- Analog ----
    "LM358": {
        "name": "LM358",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-8", "Vcc": "3-32V single / ±1.5-16V dual",
                  "pins": 8, "channels": 2},
        "desc": "Dubbel operationsförstärkare med intern frekvenssäkring. "
                "Kan drivas med enkel matning ner till 3 V; utgången svänger nära GND. "
                "Vanlig och billig; pin-kompatibel med LM1458.",
        "tags": ["LM358", "dual op-amp", "operationsförstärkare", "single supply"],
    },
    "LM239": {
        "name": "LM239",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-14",
                  "Vcc": "2-36V single / ±1-18V dual", "pins": 14, "channels": 4,
                  "output": "open-collector"},
        "desc": "Fyrkanalig differentiell komparator, industriell temperaturklass (0–70°C). "
                "Funktionellt identisk med LM339 men med bredare specificationstolerans. "
                "Open-collector-utgångar, kan driva TTL/CMOS direkt.",
        "tags": ["LM239", "quad comparator", "komparator", "open collector", "LM339 equivalent"],
    },
    "LM3401N": {
        "name": "LM3401N",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "5-28V", "pins": 14,
                  "manufacturer": "National Semiconductor"},
        "desc": "National Semiconductor LM3401N, DIP-14 (datumkod P913, 1979). "
                "Troligen fyrkanalig komparator eller analog logikkrets; "
                "exakt funktion ej fullt verifierad. "
                "Kontrollera databladet vid användning.",
        "tags": ["LM3401N", "LM3401", "National Semiconductor", "analog"],
    },
    "ADC0804": {
        "name": "ADC0804",
        "cat_hint": "analog",
        "specs": {"technology": "CMOS", "package": "DIP-20", "Vcc": "5V", "pins": 20,
                  "resolution": "8-bit", "channels": 1, "interface": "parallel"},
        "desc": "8-bitars A/D-omvandlare med successiv approximation. "
                "Enkel ingångskanal (differentiell). Parallellt 8-bitars utdatagränssnitt, "
                "kompatibelt med 8080/8085/Z80. Kräver extern RC-oscillator eller klocka.",
        "tags": ["ADC0804", "ADC", "A/D converter", "8-bit ADC", "CMOS"],
    },

    # ---- Display-drivare ----
    "MM74C923N": {
        "name": "MM74C923N",
        "cat_hint": "digital",
        "specs": {"technology": "CMOS", "package": "DIP-20", "Vcc": "2-12V", "pins": 20,
                  "manufacturer": "National Semiconductor"},
        "desc": "20-tangenters tangentbordsencoder (National Semiconductor CMOS). "
                "Känner av vilken av 20 tangenter som trycks ned, "
                "kodar till 5-bitars binärt tal med data-available-signal. "
                "Har intern key-bounce-eliminering.",
        "tags": ["MM74C923", "74C923", "keyboard encoder", "key encoder", "CMOS"],
    },
    "MM5481": {
        "name": "MM5481",
        "cat_hint": "analog",
        "specs": {"technology": "CMOS", "package": "DIP-18", "Vcc": "5-10V", "pins": 18,
                  "outputs": 10, "manufacturer": "National Semiconductor"},
        "desc": "10-kanalig LED-displaydrivare med seriegränssnitt (National Semiconductor). "
                "Tar data seriellt (2-tråd) och driver upp till 10 LED-segment direkt. "
                "Internt latch; utgångarna är sink-drivare.",
        "tags": ["MM5481", "LED driver", "display driver", "serial input", "National Semi"],
    },

    # ---- Signetics P106 ----
    "P106": {
        "name": "P106",
        "cat_hint": "digital",
        "specs": {"technology": "bipolar", "package": "DIP-16", "pins": 16,
                  "manufacturer": "Signetics"},
        "desc": "Signetics P106, DIP-16 (SSS-loggan, datumkod 98540 = 1985 v40). "
                "Exakt funktion ej verifierad. Signetics tillverkade bland annat "
                "logikkretsar, analog-switchar och kommunikations-IC. "
                "Kontrollera databladet vid användning.",
        "tags": ["P106", "Signetics", "SSS"],
    },
}

# ---------------------------------------------------------------------------
# Layout: global fack-nummer → komponentnyckel
# ---------------------------------------------------------------------------
LAYOUT = [
    (129, "74LS74"),
    (130, "D8251AC"),
    (131, "74LS85"),
    (132, "74107"),
    (133, "7417"),
    (134, "6264"),
    (135, "HM6116AP-15"),
    (136, "74LS368A"),
    (137, "74LS71"),
    (138, "74LS161"),
    (139, "7497"),
    (140, "CD40175"),    # redan i databasen
    (141, "LF353"),      # redan i databasen
    (142, "INS8154"),
    (143, "CD4024"),     # redan i databasen
    (144, "LM393"),      # redan i databasen
    (145, "74LS365"),
    (146, "SN49701AN"),
    (147, "CD4015"),     # redan i databasen
    (148, "CD4028"),
    (149, "P106"),
    (150, "CD4723BCN"),
    (151, "74LS00"),
    (152, "CD4070"),
    (153, "CD4030"),
    (154, "74LS163"),
    (155, "CD4076"),
    (156, "74LS374"),
    (157, "CD4019"),
    (158, "MM74C923N"),
    (159, "CD40175"),    # duplikat av F0140
    (160, "DM8602N"),
    (161, "74LS05"),
    (162, "74LS10"),
    (163, "7420"),
    (164, "LM358"),
    (165, "CD40105"),
    (166, "ADC0804"),
    (167, "LM3401N"),
    (168, "LM239"),
    (169, "MM5481"),
]

DRAWER_LABEL = "L20"


def find_category(categories, hint):
    hint_lower = hint.lower()
    for c in categories:
        if hint_lower in c["name"].lower():
            return c["id"]
    for c in categories:
        if hint_lower in c.get("slug", "").lower():
            return c["id"]
    for c in categories:
        if "ic" in c.get("slug", "").lower() and c.get("parent_id") is None:
            return c["id"]
    return None


def main():
    print("=== KOMPIS L20 Seeding Script ===\n")

    print("Hämtar kategorier...")
    categories = api_get("/api/categories")
    if not categories:
        print("FEL: Kan inte hämta kategorier.", file=sys.stderr)
        sys.exit(1)
    for c in categories:
        print(f"  [{c['id']}] {c['name']}")

    print(f"\nSöker efter låda {DRAWER_LABEL}...")
    drawers = api_get("/api/drawers")
    drawer = next((d for d in drawers if d["label"] == DRAWER_LABEL), None)
    if not drawer:
        print(f"FEL: Hittade inte låda {DRAWER_LABEL}!", file=sys.stderr)
        sys.exit(1)
    drawer_id = drawer["id"]
    print(f"  Låda {DRAWER_LABEL} har id={drawer_id}")

    print(f"\nHämtar befintliga fack i {DRAWER_LABEL}...")
    drawer_detail = api_get(f"/api/drawers/{drawer_id}")
    existing_compartments = {}
    if drawer_detail and "compartments" in drawer_detail:
        for comp in drawer_detail["compartments"]:
            existing_compartments[comp["label"]] = comp["id"]
    print(f"  {len(existing_compartments)} befintliga fack")

    print(f"\nSkapar fack F0129–F0169...")
    compartment_ids = {}
    for fack_num, _ in LAYOUT:
        label = f"F{fack_num:04d}"
        if label in existing_compartments:
            compartment_ids[fack_num] = existing_compartments[label]
            continue
        result, status = api_post("/api/compartments", {
            "drawer_id": drawer_id,
            "label": label,
            "description": None,
        })
        if result:
            compartment_ids[fack_num] = result["id"]
            print(f"  Skapade {label} (id={result['id']})")
        else:
            print(f"  FEL: Kunde inte skapa {label} (status={status})", file=sys.stderr)
    print(f"  {len(compartment_ids)} fack redo")

    print(f"\nSkapar komponenter...")
    created_components = {}

    for fack_num, comp_key in LAYOUT:
        if comp_key in created_components:
            continue
        if comp_key not in COMPONENTS:
            print(f"  VARNING: Ingen data för '{comp_key}'", file=sys.stderr)
            continue

        comp_data = COMPONENTS[comp_key]
        target_name = comp_data["name"]

        existing = api_get(f"/api/components?q={urllib.parse.quote(target_name)}&limit=20")
        if existing:
            match = next((c for c in existing if c["name"].lower() == target_name.lower()), None)
            if match:
                created_components[comp_key] = match["id"]
                print(f"  [{match['id']:4d}] {target_name} (finns redan)")
                continue

        cat_id = find_category(categories, comp_data["cat_hint"])
        specs = {k: v for k, v in (comp_data.get("specs") or {}).items() if k != "manufacturer"}

        payload = {
            "name": target_name,
            "description": comp_data.get("desc"),
            "category_id": cat_id,
            "manufacturer": (comp_data.get("specs") or {}).get("manufacturer"),
            "part_number": None,
            "tags": comp_data.get("tags") or None,
            "specs": specs or None,
        }

        result, status = api_post("/api/components", payload)
        if result:
            created_components[comp_key] = result["id"]
            print(f"  [{result['id']:4d}] {target_name} (ny)")
        else:
            print(f"  FEL: Skapade inte '{target_name}' (status={status})", file=sys.stderr)

    print(f"  {len(created_components)} komponenter redo")

    print(f"\nSkapar lagerplatser...")
    stock_count = 0
    for fack_num, comp_key in LAYOUT:
        if comp_key not in created_components:
            continue
        if fack_num not in compartment_ids:
            continue
        result, status = api_post("/api/stock", {
            "component_id": created_components[comp_key],
            "compartment_id": compartment_ids[fack_num],
            "quantity": 1,
            "minimum_qty": 0,
            "unit": "st",
            "notes": None,
        })
        if result:
            stock_count += 1
        elif status == 422:
            pass  # redan registrerat
        else:
            print(f"  FEL: Lager för F{fack_num:04d} (status={status})", file=sys.stderr)

    print(f"  {stock_count} lagerplatser skapade")
    print(f"\nKLART! {len(created_components)} komponenter i {len(compartment_ids)} fack i {DRAWER_LABEL}.")
    print("\nOBS: Tre komponenter har ej verifierad funktion och bör kontrolleras:")
    print("  F0146 – SN49701AN (Texas Instruments, funktion okänd)")
    print("  F0149 – P106 (Signetics, funktion okänd)")
    print("  F0160 – DM8602N (SGS, exakt funktion ej verifierad)")


if __name__ == "__main__":
    main()
