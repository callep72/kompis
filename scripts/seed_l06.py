#!/usr/bin/env python3
"""Seed drawer L06 (F0001-F0128) with IC components.

Run on rash:
  python3 scripts/seed_l06.py
Or via Docker:
  docker compose exec app python3 scripts/seed_l06.py
"""
import json
import sys
import urllib.request
import urllib.error

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


# ---------------------------------------------------------------------------
# Component definitions
# cat_hint matches a substring (case-insensitive) in category name
# ---------------------------------------------------------------------------
COMPONENTS = {
    # ---- TTL Logic ----
    "SN74185B": {
        "name": "SN74185B",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "6-bit binary-to-BCD omvandlare. Omvandlar ett 6-bitars binärt tal (0–63) till BCD-format. Kan kaskadkopplas för bredare tal.",
        "tags": ["74185", "SN74185", "binary to BCD"],
    },
    "SN74151N": {
        "name": "SN74151N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "8-till-1 datamultiplexer. Väljer en av 8 ingångssignaler med en 3-bitars adress. Har komplement- och normalutgång.",
        "tags": ["74151", "SN74151", "MUX", "multiplexer"],
    },
    "SN7474": {
        "name": "SN7474",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel D-vippa med preset och clear. Positiv flankstyrning. Standard TTL-vippa för datalagring och sekvenslogik.",
        "tags": ["7474", "dual D flip-flop", "D-vippa"],
    },
    "SN74LS373": {
        "name": "SN74LS373",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-20", "Vcc": "5V", "pins": 20},
        "desc": "Oktalt D-latch med 3-state utgångar. 8 st transparenta latch med gemensam latch-enable och output-enable. Används ofta som adresslatch på databuss.",
        "tags": ["74LS373", "74373", "octal latch", "adresslatch"],
    },
    "SN74LS02": {
        "name": "SN74LS02",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Fyra stycken 2-ingångs NOR-grindar i ett 14-bensigt DIP-kapsel.",
        "tags": ["74LS02", "74002", "NOR gate", "NOR-grind"],
    },
    "SN7417": {
        "name": "SN7417",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Hex buffer/drivare med open-collector-utgångar. Kan driva laster upp till 30V/40mA. Används för nivåanpassning och till reläer, LED-displayer m.m.",
        "tags": ["7417", "hex buffer", "open collector", "OC buffer"],
    },
    "74LS85": {
        "name": "74LS85",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "4-bitars magnitujdkomparator. Jämför två 4-bitars tal (A och B) och ger ut A>B, A=B och A<B. Kan kaskadkopplas till bredare komparatorer.",
        "tags": ["74LS85", "74085", "74LS85PC", "comparator", "magnitude comparator"],
    },
    "74LS240": {
        "name": "74LS240",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-20", "Vcc": "5V", "pins": 20, "output": "3-state"},
        "desc": "Oktal inverterad bussbuffer med 3-state utgångar. Används som linjdrivare och bussbuffer på databussar. Inverterar signalen.",
        "tags": ["74LS240", "74240", "octal buffer", "bus driver", "3-state"],
    },
    "74LS367": {
        "name": "74LS367",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16, "output": "3-state"},
        "desc": "Hex bussbuffer med 3-state utgångar (ej inverterande). 6 buffertar med gemensam output-enable-ingång.",
        "tags": ["74LS367", "hex buffer", "3-state", "bus buffer"],
    },
    "74LS138": {
        "name": "74LS138",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "3-till-8 linjedekoder/demultiplexer. Aktiverar en av 8 aktiv-låg-utgångar baserat på 3-bitars adress. Tre chip-select-ingångar. Mycket vanlig IC för adressdekodning.",
        "tags": ["74LS138", "SN74LS138N", "3-to-8 decoder", "demultiplexer", "address decoder"],
    },
    "DM81LS97N": {
        "name": "DM81LS97N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16, "output": "3-state"},
        "desc": "Hex 3-state bussbuffer (National Semiconductor). Kompabilitet med LS-TTL-bussar. Icke-inverterande buffer med tri-state-styrning.",
        "tags": ["81LS97", "hex buffer", "3-state", "National Semi"],
    },
    "SN74LS374N": {
        "name": "SN74LS374N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-20", "Vcc": "5V", "pins": 20, "output": "3-state"},
        "desc": "Oktal D-vippa med 3-state utgångar. 8 positiv-flankstyrda D-vippor. Liknar 74LS373 men är flankstyrda istället för nivåstyrda.",
        "tags": ["74LS374", "74374", "octal D flip-flop", "3-state"],
    },
    "SN7406": {
        "name": "SN7406",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Hex inverterande buffer/drivare med open-collector-utgångar. Kan hantera upp till 30V/40mA per utgång. Används för nivåkonvertering och drivning av externa laster.",
        "tags": ["7406", "SN7406A", "hex inverter", "open collector", "OC driver"],
    },
    "74LS07": {
        "name": "74LS07",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Hex buffer/drivare med open-collector-utgångar (ej inverterande). Utgångarna tål upp till 30V.",
        "tags": ["74LS07", "7407", "hex buffer", "open collector"],
    },
    "7407": {
        "name": "7407",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Hex buffer/drivare med open-collector-utgångar (ej inverterande). Standard-TTL-variant. Utgångarna tål upp till 30V/40mA.",
        "tags": ["7407", "SN7407", "hex buffer", "open collector"],
    },
    "SN74LS21": {
        "name": "SN74LS21",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel 4-ingångs AND-grind. Två oberoende AND-grindar med 4 ingångar vardera.",
        "tags": ["74LS21", "dual 4-input AND", "AND gate"],
    },
    "SN74LS173": {
        "name": "SN74LS173",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16, "output": "3-state"},
        "desc": "4-bitars D-register med 3-state-utgångar. Fyra D-vippor med gemensam klocka, nollställning och 3-state output-enable.",
        "tags": ["74LS173", "4-bit register", "3-state"],
    },
    "SN7425": {
        "name": "SN7425",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel 4-ingångs NOR-grind med strobe. Varje grind har en aktiv-låg strobe-ingång som kan inaktivera utgången.",
        "tags": ["7425", "dual NOR", "NOR gate", "strobe"],
    },
    "SN7410": {
        "name": "SN7410",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Trippel 3-ingångs NAND-grind. Tre oberoende 3-ingångs NAND-grindar i ett paket.",
        "tags": ["7410", "triple NAND", "NAND gate"],
    },
    "SN74148N": {
        "name": "SN74148N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "8-till-3 prioritetsencoder. Kodar den aktiva ingången med högst prioritet till 3-bitars binär kod. Har enable-ingång och kan kaskadkopplas.",
        "tags": ["74148", "priority encoder", "8-to-3 encoder"],
    },
    "SN74LS266": {
        "name": "SN74LS266",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Fyra XOR-grindar med open-collector-utgångar. Används för paritetsgenerering, addition och jämförelse av bitar.",
        "tags": ["74LS266", "XNOR", "XOR", "open collector"],
    },
    "SN7458N": {
        "name": "SN7458N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel AND-OR-grind. Varje sektion har en 2-ingångs AND-grind vars utgång går till en OR-grind. Kan WIRED-OR kopplas.",
        "tags": ["7458", "AND-OR", "combinational logic"],
    },
    "SN7420N": {
        "name": "SN7420N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel 4-ingångs NAND-grind. Två oberoende 4-ingångs NAND-grindar.",
        "tags": ["7420", "dual NAND", "4-input NAND"],
    },
    "SN74LS37": {
        "name": "SN74LS37",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Fyra 2-ingångs NAND-buffertar med open-collector-utgångar. Ger högre drivförmåga än standard NAND-grindar.",
        "tags": ["74LS37", "NAND buffer", "open collector"],
    },
    "SN74LS12": {
        "name": "SN74LS12",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Trippel 3-ingångs NAND-grind med open-collector-utgångar. Tre oberoende 3-ingångs NAND-grindar.",
        "tags": ["74LS12", "triple NAND", "open collector"],
    },
    "T74LS03B1": {
        "name": "T74LS03B1",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14, "manufacturer": "SGS", "output": "open-collector"},
        "desc": "Fyra 2-ingångs NAND-grindar med open-collector-utgångar (SGS/STMicroelectronics-variant av 74LS03). Funktionellt identisk med SN74LS03N.",
        "tags": ["74LS03", "T74LS03", "NAND open collector", "SGS"],
    },
    "SN74LS01": {
        "name": "SN74LS01",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Fyra 2-ingångs NAND-grindar med open-collector-utgångar. NAND med OC-utgångar för wired-AND-koppling.",
        "tags": ["74LS01", "NAND open collector"],
    },
    "SN74LS74": {
        "name": "SN74LS74",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Dubbel D-vippa med preset och clear. LS-variant av SN7474. Positiv flankstyrning.",
        "tags": ["74LS74", "dual D flip-flop", "D-vippa"],
    },
    "SN74LS153N": {
        "name": "SN74LS153N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "Dubbel 4-till-1 multiplexer. Väljer en av 4 ingångssignaler per sektion med en gemensam 2-bitars adress.",
        "tags": ["74LS153", "dual 4:1 MUX", "multiplexer"],
    },
    "74LS75": {
        "name": "74LS75",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16},
        "desc": "4-bitars bistabilt latch. Fyra transparenta D-latch med inverterade och icke-inverterade utgångar. Lagrar 4 bitar.",
        "tags": ["74LS75", "4-bit latch", "bistable"],
    },
    "74LS377N": {
        "name": "74LS377N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-20", "Vcc": "5V", "pins": 20},
        "desc": "Oktal D-vippa med clock-enable. Lagrar 8 bitar vid positiv flank. Clock-enable-ingång hindrar onödiga latching-operationer.",
        "tags": ["74LS377", "octal D flip-flop", "clock enable"],
    },
    "SN74141": {
        "name": "SN74141",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-16", "Vcc": "5V", "pins": 16, "output": "high-voltage"},
        "desc": "BCD-till-decimal-dekoder/drivare för nixierör. Avkodar 4-bitars BCD-kod (0–9) till en av 10 utgångar. Utgångarna tål upp till 60V för att driva nixierör (glimrör).",
        "tags": ["74141", "Nixie decoder", "BCD decoder", "nixie tube driver"],
    },
    "DM74L17N": {
        "name": "DM74L17N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL L", "package": "DIP-14", "Vcc": "5V", "pins": 14, "output": "open-collector"},
        "desc": "Hex open-collector buffer (National Semiconductor, lågeffekt-TTL). L-serien har lägre strömförbrukning men långsammare än standard TTL.",
        "tags": ["74L17", "DM74L17", "hex buffer", "open collector", "low power TTL"],
    },
    "SN74105N": {
        "name": "SN74105N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL", "package": "DIP-14", "Vcc": "5V", "pins": 14},
        "desc": "Fyra JK master-slave-vippor (äldre TTL-krets). En äldre komponent ur 74-serien; ersatt av modernare vippor.",
        "tags": ["7405", "SN74105", "J-K flip-flop", "obsolete TTL"],
    },

    # ---- CMOS Logic ----
    "CD4539": {
        "name": "CD4539",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "Dubbel 4-ingångs multiplexer. Väljer en av 4 ingångssignaler per sektion med en 2-bitars adress. Liknar CD4052 men med separat enable.",
        "tags": ["4539", "HEF4539", "dual 4:1 MUX", "CMOS MUX"],
    },
    "CD40109": {
        "name": "CD40109",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "Fyra spänningsnivåkonverterare (låg-till-hög). Konverterar signaler från lägre Vcc till en högre Vcc. Används för att koppla samman kretsar med olika matningsspänningar.",
        "tags": ["40109", "level shifter", "level converter", "CMOS"],
    },
    "CD40175": {
        "name": "CD40175",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "Fyra D-vippor. Positiv flankstyrda D-vippor med gemensam klocka och gemensam reset. CMOS-variant av 74175.",
        "tags": ["40175", "CD40175", "quad D flip-flop", "4175"],
    },
    "MC14042": {
        "name": "MC14042",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "MC14000", "package": "DIP-16", "Vcc": "3-18V", "pins": 16, "manufacturer": "Motorola"},
        "desc": "Fyra klockade D-latch (Motorola CMOS). Lagrar 4 bitar vid klock-flanken. Funktionellt lik CD4042.",
        "tags": ["14042", "MC14042", "quad D latch", "Motorola CMOS"],
    },
    "MC14024BCL": {
        "name": "MC14024BCL",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "MC14000", "package": "DIP-14", "Vcc": "3-18V", "pins": 14, "manufacturer": "Motorola"},
        "desc": "7-stegs binär rippelräknare (Motorola CMOS). Identisk funktion som CD4024. Delar klocksignal med 2, 4, 8 … 128.",
        "tags": ["14024", "MC14024", "7-stage counter", "ripple counter", "Motorola"],
    },
    "MC14040BCP": {
        "name": "MC14040BCP",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "MC14000", "package": "DIP-16", "Vcc": "3-18V", "pins": 16, "manufacturer": "Motorola"},
        "desc": "12-stegs binär rippelräknare (Motorola CMOS). Identisk funktion som CD4040. Ger ut 12 Q-utgångar (Q1–Q12).",
        "tags": ["14040", "MC14040", "12-stage counter", "Motorola CMOS"],
    },
    "CD4024": {
        "name": "CD4024",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "7-stegs binär rippelräknare. Räknar nedåt och ger utgångar Q1–Q7 som delar klocksignalen med 2, 4, 8, 16, 32, 64 och 128.",
        "tags": ["4024", "CD4024", "7-stage counter", "frequency divider"],
    },
    "CD4025": {
        "name": "CD4025",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Trippel 3-ingångs NOR-grind. Tre oberoende NOR-grindar med 3 ingångar vardera.",
        "tags": ["4025", "triple NOR", "NOR gate"],
    },
    "CD4067BE": {
        "name": "CD4067",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-24", "Vcc": "3-18V", "pins": 24},
        "desc": "16-kanalig analog multiplexer/demultiplexer. Väljer en av 16 analogkanaler med en 4-bitars adress. Kan hantera signaler i hela matningsspänningsintervallet.",
        "tags": ["4067", "CD4067", "CD4067BE", "16-channel MUX", "analog switch"],
    },
    "CD4514BCN": {
        "name": "CD4514BCN",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-24", "Vcc": "3-18V", "pins": 24},
        "desc": "4-till-16 linjedekoder med latch. Aktiverar en av 16 utgångar (aktiv hög) baserat på 4-bitars adress. Har inbyggt adresslatch.",
        "tags": ["4514", "CD4514", "4-to-16 decoder", "1-of-16"],
    },
    "CD40106BE": {
        "name": "CD40106BE",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Hex Schmitt-trigger-inverter. 6 inverterare med Schmitt-trigger-ingångar för bra brusimmunitet. Används för signalformning och oscillatorer.",
        "tags": ["40106", "CD40106", "hex Schmitt", "Schmitt trigger", "inverter"],
    },
    "HEF4514BP": {
        "name": "HEF4514BP",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "HEF4000", "package": "DIP-24", "Vcc": "3-15V", "pins": 24, "manufacturer": "Philips"},
        "desc": "4-till-16 linjedekoder med latch (Philips HEF-serie). Funktionellt identisk med CD4514. Aktiv-hög-utgångar.",
        "tags": ["HEF4514", "4514", "4-to-16 decoder", "Philips CMOS"],
    },
    "MM74C906N": {
        "name": "MM74C906N",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "package": "DIP-14", "Vcc": "3-15V", "pins": 14, "output": "open-drain", "manufacturer": "National Semiconductor"},
        "desc": "Hex open-drain buffer (National Semiconductor CMOS). Kan koppla CMOS-signaler till högre spänningsnivåer via pull-up-motstånd.",
        "tags": ["74C906", "MM74C906", "hex buffer", "open drain", "CMOS"],
    },
    "DM4512BE": {
        "name": "DM4512BE",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "package": "DIP-16", "Vcc": "3-15V", "pins": 16, "manufacturer": "National Semiconductor"},
        "desc": "8-kanalig analog switch/multiplexer (National Semiconductor). Väljer en av 8 analogingångar med 3-bitars adress. Funktionellt lik CD4051.",
        "tags": ["4512", "DM4512", "analog multiplexer", "CMOS switch"],
    },
    "CD4072": {
        "name": "CD4072",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Dubbel 4-ingångs OR-grind. Två oberoende OR-grindar med 4 ingångar vardera.",
        "tags": ["4072", "CD4072", "dual OR", "4-input OR"],
    },
    "CD4069": {
        "name": "CD4069",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Hex inverter. Sex oberoende CMOS-inverterare. Standardkomponent för logikkomplementering.",
        "tags": ["4069", "CD4069", "hex inverter", "NOT gate"],
    },
    "CD4013": {
        "name": "CD4013",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Dubbel D-vippa. Positiv flankstyrda D-vippor med set och reset. Kan konfigureras för T-vippa eller delning med 2.",
        "tags": ["4013", "CD4013", "dual D flip-flop", "D-vippa"],
    },
    "CD4001": {
        "name": "CD4001",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Fyra 2-ingångs NOR-grindar. Grundläggande CMOS-NOR-grind; kan användas som inverterare (båda ingångarna kopplade).",
        "tags": ["4001", "CD4001", "quad NOR", "NOR gate"],
    },
    "CD4093": {
        "name": "CD4093",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Fyra 2-ingångs NAND-grindar med Schmitt-trigger-ingångar. Kombinerar NAND och Schmitt-trigger för bra brusimmunitet. Vanlig för oscillatorer.",
        "tags": ["4093", "CD4093", "NAND Schmitt", "Schmitt trigger"],
    },
    "CD4015": {
        "name": "CD4015",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "Dubbelt 4-stegs serieingångs/parallellutgångs skiftregister. Var sektions 4-bitars skiftregister kan kopplas i serie för längre skift.",
        "tags": ["4015", "CD4015", "shift register", "SIPO"],
    },
    "CD4012": {
        "name": "CD4012",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Dubbel 4-ingångs NAND-grind. Två oberoende 4-ingångs NAND-grindar.",
        "tags": ["4012", "CD4012", "dual 4-input NAND"],
    },
    "CD4050BE": {
        "name": "CD4050BE",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "Hex icke-inverterande buffer. Kan drivas med 5V ingång och 15V VDD för nivåkonvertering uppåt. Utgångsspänningen följer VDD.",
        "tags": ["4050", "CD4050", "hex buffer", "level shifter", "non-inverting"],
    },
    "CD4040BE": {
        "name": "CD4040BE",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "12-stegs binär rippelräknare. Ger 12 utgångar Q1–Q12 som delar klocksignalen. Ofta använd som frekvensdelarkrets.",
        "tags": ["4040", "CD4040", "12-stage counter", "ripple counter"],
    },
    "CD4099": {
        "name": "CD4099",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "8-bitars adresserbart latch. Låter dig skriva till en vald bit (Q0–Q7) via 3-bitars adress utan att påverka övriga bitar.",
        "tags": ["4099", "CD4099", "addressable latch", "8-bit latch"],
    },
    "CD4020": {
        "name": "CD4020",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "14-stegs binär rippelräknare. Ger utgångar Q1, Q4–Q14 (inte Q2 och Q3 externt). Används för frekvensdelning i längre kedjor.",
        "tags": ["4020", "CD4020", "14-stage counter", "ripple counter"],
    },
    "CD4023": {
        "name": "CD4023",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-14", "Vcc": "3-18V", "pins": 14},
        "desc": "Trippel 3-ingångs NAND-grind. Tre oberoende NAND-grindar med 3 ingångar vardera.",
        "tags": ["4023", "CD4023", "triple NAND", "3-input NAND"],
    },
    "CD4516": {
        "name": "CD4516",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS", "series": "4000B", "package": "DIP-16", "Vcc": "3-18V", "pins": 16},
        "desc": "Förinställbar binär upp/ned-räknare. 4-bitars räknare med upp/ned-styrning, parallell load och ripple carry. Kan kaskadkopplas.",
        "tags": ["4516", "CD4516", "up/down counter", "presettable counter"],
    },
    "SN74HC245N": {
        "name": "SN74HC245N",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS HC", "package": "DIP-20", "Vcc": "2-6V", "pins": 20, "output": "3-state"},
        "desc": "Oktal busstransceiver med 3-state-utgångar (icke-inverterande). Dir-ingång styr dataflödets riktning. Vanlig för databussanslutningar.",
        "tags": ["74HC245", "74245", "octal transceiver", "bus transceiver", "3-state"],
    },
    "SN74HC595N": {
        "name": "SN74HC595N",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS HC", "package": "DIP-16", "Vcc": "2-6V", "pins": 16},
        "desc": "8-bitars skiftregister med parallellutgångslatch (SIPO). Serial-in, parallel-out med SPI-kompatibelt gränssnitt. Vanlig för att utöka antalet utgångar via SPI.",
        "tags": ["74HC595", "shift register", "SIPO", "SPI", "serial to parallel"],
    },
    "SN74AHCT125": {
        "name": "SN74AHCT125",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS AHCT", "package": "DIP-14", "Vcc": "4.5-5.5V", "pins": 14, "output": "3-state"},
        "desc": "Fyra bussbuffertar med 3-state-utgångar. AHC-T-serien har TTL-kompatibla ingångsnivåer (Vih=2V) men CMOS-utgångar. Var buffert aktiveras separat.",
        "tags": ["74AHCT125", "74125", "quad buffer", "3-state", "AHCT"],
    },
    "74HC21D": {
        "name": "74HC21D",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS HC", "package": "SO-14", "Vcc": "2-6V", "pins": 14},
        "desc": "Dubbel 4-ingångs AND-grind (SMD-kapsel). HC-CMOS. Notera: D-suffixet = SO-14 (SMD-kapsel), ej DIP.",
        "tags": ["74HC21", "dual 4-input AND", "CMOS SMD"],
    },
    "MM74HC241B1": {
        "name": "MM74HC241B1",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS HC", "package": "DIP-20", "Vcc": "2-6V", "pins": 20, "output": "3-state"},
        "desc": "Oktal 3-state buffer/linjedrivare (National Semiconductor). Icke-inverterande med två aktiv-låg enable-ingångar (G1A och G2A styr varsin grupp om 4).",
        "tags": ["74HC241", "MM74HC241", "octal buffer", "3-state", "National Semi"],
    },
    "SN74HC640P": {
        "name": "SN74HC640P",
        "cat_hint": "cmos",
        "specs": {"technology": "CMOS HC", "package": "DIP-20", "Vcc": "2-6V", "pins": 20, "output": "3-state"},
        "desc": "Oktal inverterad busstransceiver med 3-state-utgångar. Inverterar datasignalen. Dir-ingång styr riktning.",
        "tags": ["74HC640", "octal transceiver", "inverting", "3-state"],
    },

    # ---- Op-amp / Comparator ----
    "LM339N": {
        "name": "LM339N",
        "cat_hint": "ompar",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "2-36V single / ±1-18V dual", "pins": 14, "channels": 4, "output": "open-collector"},
        "desc": "Fyrkanalig spänningskomparator. Open-collector-utgångar kan driva direkt till positiv matning (wired-OR). Fungerar med enkel eller dubbel matning.",
        "tags": ["LM339", "quad comparator", "komparator", "open collector"],
    },
    "LM358N": {
        "name": "LM358N",
        "cat_hint": "op-amp",
        "specs": {"technology": "bipolar", "package": "DIP-8", "Vcc": "3-32V single / ±1.5-16V dual", "pins": 8, "channels": 2},
        "desc": "Dubbel operationsförstärkare med intern frekvenssäkring. Kan drivas med enkel matning ner till 3V. Utgången kan swingas nära GND.",
        "tags": ["LM358", "dual op-amp", "operationsförstärkare"],
    },
    "TL071": {
        "name": "TL071",
        "cat_hint": "op-amp",
        "specs": {"technology": "JFET+bipolar", "package": "DIP-8", "Vcc": "±3.5-18V", "pins": 8, "channels": 1},
        "desc": "JFET-ingångs operationsförstärkare (singel). Extremt hög ingångsimpedans, låg ingångspolarisationsström. Används i instrumentering och audiokretsar.",
        "tags": ["TL071", "TL071CP", "JFET op-amp", "operationsförstärkare", "low noise"],
    },
    "LF353": {
        "name": "LF353",
        "cat_hint": "op-amp",
        "specs": {"technology": "JFET+bipolar", "package": "DIP-8", "Vcc": "±5-18V", "pins": 8, "channels": 2},
        "desc": "Dubbel JFET-ingångs operationsförstärkare med intern kompensation. Låg offsetspänning, låg brusström. Pin-kompatibel med LM1458/LM358.",
        "tags": ["LF353", "dual JFET op-amp", "operationsförstärkare"],
    },
    "LM348": {
        "name": "LM348",
        "cat_hint": "op-amp",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "±5-18V", "pins": 14, "channels": 4},
        "desc": "Fyrkanalig operationsförstärkare (internt kompenserad). Varje section är pin-kompatibel med μA741. Används där 4 oberoende op-ampar krävs.",
        "tags": ["LM348", "quad op-amp", "741 compatible", "operationsförstärkare"],
    },
    "UA741": {
        "name": "UA741",
        "cat_hint": "op-amp",
        "specs": {"technology": "bipolar", "package": "DIP-8", "Vcc": "±5-18V", "pins": 8, "channels": 1},
        "desc": "Klassisk enkanalig operationsförstärkare (μA741). Internt kompenserad. Industristandard sedan 1968, bred tillgänglighet. Används i grundläggande förstärkar- och filterkretsar.",
        "tags": ["741", "uA741", "op-amp", "operationsförstärkare", "classic"],
    },
    "LM324": {
        "name": "LM324",
        "cat_hint": "op-amp",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "3-32V single / ±1.5-16V dual", "pins": 14, "channels": 4},
        "desc": "Fyrkanalig operationsförstärkare för enkelmatsning. Utgången kan swingas nära GND. Vanlig och billig; används i signalbehandling, filter och jämförelsekretsar.",
        "tags": ["LM324", "quad op-amp", "single supply", "operationsförstärkare"],
    },
    "CA324E": {
        "name": "CA324E",
        "cat_hint": "op-amp",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "3-32V single", "pins": 14, "channels": 4, "manufacturer": "RCA"},
        "desc": "Fyrkanalig operationsförstärkare (RCA). Funktionellt identisk med LM324. Pin-kompatibel. Kan drivas med enkel matning.",
        "tags": ["CA324", "LM324 compatible", "quad op-amp", "RCA"],
    },
    "LM393": {
        "name": "LM393",
        "cat_hint": "ompar",
        "specs": {"technology": "bipolar", "package": "DIP-8", "Vcc": "2-36V single / ±1-18V dual", "pins": 8, "channels": 2, "output": "open-collector"},
        "desc": "Dubbel spänningskomparator med open-collector-utgångar. Låg offsetspänning. Kan driva TTL/CMOS direkt. Vanlig för nivådetektering.",
        "tags": ["LM393", "dual comparator", "komparator", "open collector"],
    },

    # ---- Microprocessors / Microcontrollers ----
    "Z80A": {
        "name": "Zilog Z80A",
        "cat_hint": "mikroprocessor",
        "specs": {"technology": "NMOS", "package": "DIP-40", "Vcc": "5V", "pins": 40, "word_size": "8-bit", "max_clock": "4MHz", "manufacturer": "Zilog"},
        "desc": "Klassisk 8-bitars mikroprocessor med Z80-arkitektur. 4MHz-variant. Internt register med 208 bitar inkl. IX/IY-indexregister. Kompatibel med 8080-instruktioner. Används i historiska datorer (ZX Spectrum, Amstrad, CP/M etc.).",
        "tags": ["Z80", "Z80A", "Zilog", "8-bit CPU", "mikroprocessor", "CP/M"],
    },
    "TMP8085AP": {
        "name": "TMP8085AP",
        "cat_hint": "mikroprocessor",
        "specs": {"technology": "NMOS", "package": "DIP-40", "Vcc": "5V", "pins": 40, "word_size": "8-bit", "max_clock": "3MHz", "manufacturer": "Toshiba"},
        "desc": "Toshibas version av Intel 8085A. 8-bitars mikroprocessor fullt kompatibel med Intel 8085A. Multiplexad adress/databuss (AD0–AD7). Inbyggd UART och interrupt-kontroller.",
        "tags": ["8085", "TMP8085", "Intel 8085 compatible", "Toshiba", "mikroprocessor"],
    },
    "ATmega328P": {
        "name": "ATmega328P",
        "cat_hint": "mikrokontroller",
        "specs": {"technology": "CMOS", "package": "DIP-28", "Vcc": "1.8-5.5V", "pins": 28, "word_size": "8-bit", "flash": "32KB", "ram": "2KB", "max_clock": "20MHz", "manufacturer": "Atmel/Microchip"},
        "desc": "AVR 8-bitars mikrokontroller. Känd som hjärtat i Arduino Uno/Nano. 32KB flash, 2KB RAM, 1KB EEPROM. 23 GPIO, UART, SPI, I2C, 6st ADC-kanaler.",
        "tags": ["ATmega328", "ATmega328P", "AVR", "Arduino", "mikrokontroller", "Atmel"],
    },
    "Intel8039": {
        "name": "Intel 8039",
        "cat_hint": "mikrokontroller",
        "specs": {"technology": "NMOS", "package": "DIP-40", "Vcc": "5V", "pins": 40, "word_size": "8-bit", "ram": "128B", "manufacturer": "Intel"},
        "desc": "8-bitars enkretsmikrokontroller ur MCS-48-familjen. Kräver extern ROM (till skillnad från 8048 som har intern ROM). 128 byte intern RAM, 27 I/O-portar, en 8-bitars timer.",
        "tags": ["8039", "MCS-48", "Intel 8039", "mikrokontroller"],
    },
    "Intel8155": {
        "name": "Intel 8155",
        "cat_hint": "mikroprocessor",
        "specs": {"technology": "NMOS", "package": "DIP-40", "Vcc": "5V", "pins": 40, "manufacturer": "Intel"},
        "desc": "RAM/I/O/Timer-krets för 8080/8085-system. Innehåller 256 bytes RAM, 22 I/O-portar (3 portar) och en 14-bitars timer. Ansluts direkt till 8085:ans multiplexade buss.",
        "tags": ["8155", "Intel 8155", "RAM IO Timer", "8085 peripheral"],
    },
    "Intel8243": {
        "name": "Intel 8243",
        "cat_hint": "mikroprocessor",
        "specs": {"technology": "NMOS", "package": "DIP-24", "Vcc": "5V", "pins": 24, "manufacturer": "Intel"},
        "desc": "I/O-expanderkrets för MCS-48-familjen (8048/8039). Ger 16 extra I/O-linjer (4 portar × 4 bitar) via 4-bitars expanderbuss.",
        "tags": ["8243", "Intel 8243", "I/O expander", "MCS-48 peripheral"],
    },
    "Intel8216": {
        "name": "Intel 8216",
        "cat_hint": "mikroprocessor",
        "specs": {"technology": "bipolar", "package": "DIP-18", "Vcc": "5V", "pins": 18, "manufacturer": "Intel"},
        "desc": "4-bitars dubbelriktad bussdrivare för 8080-system. Förstärker 8080:ans databuss. Styr riktning via CS och DIEN-signaler.",
        "tags": ["8216", "Intel 8216", "bus driver", "8080 peripheral"],
    },
    "D80C39C": {
        "name": "D80C39C",
        "cat_hint": "mikrokontroller",
        "specs": {"technology": "CMOS", "package": "DIP-40", "Vcc": "5V", "pins": 40, "manufacturer": "NEC", "ram": "128B"},
        "desc": "NECs CMOS-variant av Intel 8039. Funktionellt kompatibel men med lägre strömförbrukning tack vare CMOS-teknik. MCS-48-kompatibel.",
        "tags": ["D80C39", "NEC 8039", "CMOS 8039", "MCS-48", "mikrokontroller"],
    },

    # ---- Memory ----
    "HM6264LP-12": {
        "name": "HM6264LP-12",
        "cat_hint": "minne",
        "specs": {"technology": "CMOS SRAM", "package": "DIP-28", "Vcc": "5V", "pins": 28, "capacity": "8K×8 bit", "access_time": "120ns", "manufacturer": "Hitachi"},
        "desc": "8K×8 statiskt RAM (SRAM). 64Kbit CMOS-SRAM med 120ns åtkomsttid. Batteri-backupkompatibel. Pin-kompatibel med EPROM-26-pin-kapslar med adapter.",
        "tags": ["HM6264", "6264", "SRAM", "8Kx8", "static RAM"],
    },
    "N82S129": {
        "name": "N82S129",
        "cat_hint": "minne",
        "specs": {"technology": "bipolar PROM", "package": "DIP-16", "Vcc": "5V", "pins": 16, "capacity": "256×4 bit", "manufacturer": "Intel"},
        "desc": "256×4-bitars programmerbara ROM (PROM, bipolär). Fältprogrammerbar en gång via fuse-teknik. TTL-kompatibla utgångar. Används för lookup-tabeller och adressdekodning.",
        "tags": ["82S129", "N82S129", "PROM", "256x4", "bipolar PROM"],
    },
    "SN74S387N": {
        "name": "SN74S387N",
        "cat_hint": "minne",
        "specs": {"technology": "Schottky TTL PROM", "package": "DIP-16", "Vcc": "5V", "pins": 16, "capacity": "256×4 bit"},
        "desc": "256×4-bitars Schottky TTL PROM. Fältprogrammerbar en gång. Aktiv-låg utgångar. Snabbare åtkomsttid än bipolär 82S129 tack vare Schottky-dioder.",
        "tags": ["74S387", "SN74S387", "PROM", "256x4", "Schottky"],
    },
    "SN74189AP": {
        "name": "SN74189AP",
        "cat_hint": "minne",
        "specs": {"technology": "TTL SRAM", "package": "DIP-16", "Vcc": "5V", "pins": 16, "capacity": "16×4 bit", "output": "3-state"},
        "desc": "16×4-bitars TTL-RAM med inverterade 3-state-utgångar. 64 bitars statiskt RAM. Fyra adressingångar, aktiv-låg skrivstyrning.",
        "tags": ["74189", "SN74189", "TTL RAM", "16x4 RAM"],
    },
    "TDF6264APG": {
        "name": "TDF6264APG",
        "cat_hint": "minne",
        "specs": {"technology": "CMOS SRAM", "package": "DIP-28", "Vcc": "5V", "pins": 28, "capacity": "8K×8 bit", "manufacturer": "Philips"},
        "desc": "8K×8 statiskt RAM (Philips/Signetics TDF6264). CMOS-SRAM funktionellt identisk med HM6264. TDF = Philips/Signetics-beteckning.",
        "tags": ["TDF6264", "6264", "SRAM", "8Kx8", "Philips SRAM"],
    },

    # ---- Drivers / Interface ----
    "ULN2004A": {
        "name": "ULN2004A",
        "cat_hint": "drivkrets",
        "specs": {"technology": "bipolar Darlington", "package": "DIP-16", "Vcc": "5V logic", "pins": 16, "channels": 7, "output_voltage": "50V max", "output_current": "500mA per channel"},
        "desc": "7-kanalig Darlington-transistormatris för PMOS/CMOS-ingångsnivåer (ingångströskel ~14V). Utgångarna kan driva reläer, solenoidventiler och stegmotorer. Inbyggda flyback-dioder.",
        "tags": ["ULN2004", "Darlington array", "relay driver", "PMOS input"],
    },
    "ULN2803APG": {
        "name": "ULN2803APG",
        "cat_hint": "drivkrets",
        "specs": {"technology": "bipolar Darlington", "package": "DIP-18", "Vcc": "5V logic", "pins": 18, "channels": 8, "output_voltage": "50V max", "output_current": "500mA per channel"},
        "desc": "8-kanalig Darlington-transistormatris för TTL/CMOS-ingångsnivåer (ingångströskel ~2.7V). Driver reläer, stegmotorer, solenoidventiler. Inbyggda flyback-dioder mot gemensam COM-pin.",
        "tags": ["ULN2803", "Darlington array", "relay driver", "stepper motor driver"],
    },
    "ULN2804A": {
        "name": "ULN2804A",
        "cat_hint": "drivkrets",
        "specs": {"technology": "bipolar Darlington", "package": "DIP-18", "Vcc": "5V logic", "pins": 18, "channels": 8, "output_voltage": "50V max", "output_current": "500mA per channel"},
        "desc": "8-kanalig Darlington-transistormatris för CMOS 6-15V-ingångsnivåer (ingångströskel ~8V). Annars lik ULN2803A. Inbyggda flyback-dioder.",
        "tags": ["ULN2804", "Darlington array", "relay driver", "CMOS input"],
    },
    "UDN2981A": {
        "name": "UDN2981A",
        "cat_hint": "drivkrets",
        "specs": {"technology": "bipolar", "package": "DIP-18", "Vcc": "5-50V", "pins": 18, "channels": 8, "output_current": "500mA per channel"},
        "desc": "8-kanalig källstyrningsdrivare (high-side). Till skillnad från ULN2003 är UDN2981A en PNP-baserad source-driver (drar upp mot Vcc). Vanlig för matning av displayer och LED-matriser.",
        "tags": ["UDN2981", "source driver", "high-side driver", "PNP array"],
    },
    "ULN2002A": {
        "name": "ULN2002A",
        "cat_hint": "drivkrets",
        "specs": {"technology": "bipolar Darlington", "package": "DIP-16", "Vcc": "5V logic", "pins": 16, "channels": 7, "output_voltage": "50V max", "output_current": "500mA per channel"},
        "desc": "7-kanalig Darlington-transistormatris för DTL/TTL-ingångsnivåer (ingångströskel ~0.9V). Äldre ingångströskel än ULN2003A. Inbyggda flyback-dioder.",
        "tags": ["ULN2002", "Darlington array", "relay driver", "DTL TTL input"],
    },
    "MCP23017": {
        "name": "MCP23017",
        "cat_hint": "kommunikation",
        "specs": {"technology": "CMOS", "package": "DIP-28", "Vcc": "1.8-5.5V", "pins": 28, "interface": "I2C", "gpio": 16, "manufacturer": "Microchip"},
        "desc": "16-bitars I/O-expanderkrets via I2C. Ger 16 extra GPIO-pinnar via 2-trådigt I2C-gränssnitt. Upp till 8 kretsar på samma buss (128 GPIO). Stöder interrupt-output.",
        "tags": ["MCP23017", "I2C IO expander", "GPIO expander", "I2C"],
    },
    "MAX232": {
        "name": "MAX232",
        "cat_hint": "kommunikation",
        "specs": {"technology": "CMOS", "package": "DIP-16", "Vcc": "5V", "pins": 16, "interface": "RS-232", "channels": 2, "manufacturer": "Maxim"},
        "desc": "RS-232 nivåkonverterare. Konverterar TTL-logik (0/5V) till RS-232-nivåer (±12V) med inbyggda laddningspumpar. Kräver fyra externa 1μF-kondensatorer.",
        "tags": ["MAX232", "RS-232", "UART level converter", "serial interface"],
    },

    # ---- Timer ----
    "NE556": {
        "name": "NE556",
        "cat_hint": "timer",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "5-15V", "pins": 14, "channels": 2},
        "desc": "Dubbel 555-timer i ett paket. Innehåller två oberoende 555-timerkretsar. Monostabilt (one-shot) och astabilt (oscillator) läge.",
        "tags": ["NE556", "556", "dual 555", "timer", "oscillator"],
    },
    "MC14536": {
        "name": "MC14536",
        "cat_hint": "timer",
        "specs": {"technology": "CMOS", "package": "DIP-16", "Vcc": "3-18V", "pins": 16, "manufacturer": "Motorola"},
        "desc": "Programmerbar CMOS-timer med 24 steg. Binär delningskedja ger tidsintervall från mikrosekunder till timmar via extern RC-oscillator. Utbytbart med MC14541.",
        "tags": ["MC14536", "14536", "programmable timer", "CMOS timer", "Motorola"],
    },

    # ---- Analog ----
    "TBA800": {
        "name": "TBA800",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-12", "Vcc": "3-20V", "pins": 12, "power_output": "7W", "manufacturer": "Philips/Siemens"},
        "desc": "Monolitisk ljudeffektförstärkare, 7W vid 20V. Används i radio- och TV-mottagare. Kräver heatsink. Inbyggda skyddsdioder och termisk skydd.",
        "tags": ["TBA800", "audio amplifier", "power amplifier", "Philips", "Siemens"],
    },
    "TDA1905": {
        "name": "TDA1905",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-12", "Vcc": "8-18V", "pins": 12, "power_output": "5W", "manufacturer": "ST/Philips"},
        "desc": "5W monolitisk ljudeffektförstärkare. Kräver ett minimum av externa komponenter. Inbyggd kortslutningsskydd och termisk frånkoppling. Vanlig i radioapparater.",
        "tags": ["TDA1905", "audio amp", "power amplifier", "5W"],
    },
    "LM381N": {
        "name": "LM381N",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "9-40V", "pins": 14, "channels": 2, "noise": "low", "manufacturer": "National Semiconductor"},
        "desc": "Låbrusig dubbel förförstärkarkrets. Används i audioapplikationer, t.ex. PHONO-förförstärkare och mikrofonförstärkare. Internt kompenserad, inga externa kondensatorer behövs.",
        "tags": ["LM381", "preamplifier", "low noise", "audio preamp"],
    },
    "LM389": {
        "name": "LM389",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-14", "Vcc": "5-12V", "pins": 14, "manufacturer": "National Semiconductor"},
        "desc": "Kombinerad lavbrus-preamp och NPN-transistorarray. Innehåller en lågbrusig op-amp och tre separata NPN-transistorer i ett paket. Används i audiokretsar.",
        "tags": ["LM389", "audio amp", "transistor array", "preamp"],
    },
    "CA3089": {
        "name": "CA3089",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-16", "Vcc": "8-18V", "pins": 16, "manufacturer": "Harris/RCA"},
        "desc": "FM IF-system IC. Komplett FM-melllanfrekvensförstärkare med begränsare och FM-detektor i ett paket. Internt AGC och mätutgång. Används i FM-mottagare.",
        "tags": ["CA3089", "FM IF", "FM receiver", "demodulator", "RCA"],
    },
    "MM5452N": {
        "name": "MM5452N",
        "cat_hint": "analog",
        "specs": {"technology": "CMOS", "package": "DIP-40", "Vcc": "5-9V", "pins": 40, "segments": 32, "manufacturer": "National Semiconductor"},
        "desc": "LCD-segmentdrivare. Driver upp till 32 LCD-segement med serial-in gränssnitt. Intern oscillator för LCD-bakspänning (AC-signal). Vanlig i äldre displayapplikationer.",
        "tags": ["MM5452", "LCD driver", "segment driver", "National Semi"],
    },
    "TCA105": {
        "name": "TCA105",
        "cat_hint": "analog",
        "specs": {"technology": "bipolar", "package": "DIP-8", "Vcc": "5-18V", "pins": 8, "manufacturer": "Siemens"},
        "desc": "Tyristort/triac-triggerkrets (Siemens). Genererar synkroniserade triggerpulser för tyristorer och triaceretter med nollspänningsdetektering. Faskontroll av AC-last.",
        "tags": ["TCA105", "thyristor trigger", "triac controller", "phase control", "Siemens"],
    },

    # ---- Unknown / Obscure ----
    "LNDX829A": {
        "name": "LNDX829A",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP"},
        "desc": "Okänd integrerad krets. Beteckning LNDX829A. Tillverkare och funktion har ej kunnat identifieras.",
        "tags": [],
    },
    "93438-DC": {
        "name": "93438-DC",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP"},
        "desc": "Okänd komponent, beteckning 93438-DC. Möjligen äldre industrikomponent. Funktion och tillverkare okänd.",
        "tags": [],
    },
    "9667PC": {
        "name": "9667PC",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP"},
        "desc": "Okänd integrerad krets, beteckning 9667PC. Möjligen ur 9000-serien (militär 74-serien) eller annan äldre serie. Funktion okänd.",
        "tags": [],
    },
    "K155ID1": {
        "name": "K155ID1",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL (sovjet)", "package": "DIP-16", "Vcc": "5V", "pins": 16, "manufacturer": "Sovjet/Ryssland"},
        "desc": "Sovjet-/rysk BCD-till-decimal-dekoder/drivare för nixierör (К155ИД1). Funktionellt ekvivalent med SN74141. Ingår i К155-serien som är den sovjet­iska ekvivalenten till SN74-serien.",
        "tags": ["K155ID1", "К155ИД1", "74141 equivalent", "nixie decoder", "Soviet TTL"],
    },
    "ICM7243BIPLZ": {
        "name": "ICM7243BIPLZ",
        "cat_hint": "analog",
        "specs": {"technology": "CMOS", "package": "DIP-28", "Vcc": "5V", "pins": 28, "manufacturer": "Intersil/Maxim"},
        "desc": "Alfanumerisk LCD-teckendrivare (Intersil ICM7243). Driver 4,5-siffrigt 7-segmentsdisplay. Serial-in-gränssnitt med inbyggd teckendekodning.",
        "tags": ["ICM7243", "LCD driver", "character display", "7-segment driver"],
    },
    "6561APC": {
        "name": "MOS 6561 (VIC)",
        "cat_hint": "övrigt",
        "specs": {"technology": "NMOS", "package": "DIP-40", "Vcc": "5V", "pins": 40, "manufacturer": "MOS Technology"},
        "desc": "Video Interface Chip (VIC), PAL-variant. Används i Commodore VIC-20 (europeisk version). Genererar videosignal, hanterar sprites och färger. Extremt sällsynt.",
        "tags": ["6561", "MOS 6561", "VIC", "VIC-20", "Commodore", "video chip"],
    },
    "LS7210": {
        "name": "LS7210",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP"},
        "desc": "Okänd integrerad krets, beteckning LS7210. Möjligen från US Micro Products eller liknande. Funktion har ej kunnat verifieras.",
        "tags": ["LS7210"],
    },
    "DM81LS97N": {
        "name": "DM81LS97N",
        "cat_hint": "ttl",
        "specs": {"technology": "TTL LS", "package": "DIP-16", "Vcc": "5V", "pins": 16, "output": "3-state", "manufacturer": "National Semiconductor"},
        "desc": "Hex 3-state bussbuffer (National Semiconductor 81LS97). Icke-inverterande med 3-state-utgångar för att dela databuss. Kompatibel med LS-TTL.",
        "tags": ["81LS97", "DM81LS97", "hex buffer", "3-state", "bus driver"],
    },

    # ---- Sockets ----
    "DIP-16-SOCKET": {
        "name": "DIP-16 sockel",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP-16", "pins": 16},
        "desc": "IC-sockel för DIP-16-kapslar. 16-bensig DIP-sockel för enkel utbyte av IC-kretsar.",
        "tags": ["sockel", "socket", "DIP-16", "IC-sockel"],
    },
    "DIP-8-SOCKET": {
        "name": "DIP-8 sockel",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP-8", "pins": 8},
        "desc": "IC-sockel för DIP-8-kapslar. 8-bensig DIP-sockel.",
        "tags": ["sockel", "socket", "DIP-8", "IC-sockel"],
    },
    "DIP-14-SOCKET": {
        "name": "DIP-14 sockel",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP-14", "pins": 14},
        "desc": "IC-sockel för DIP-14-kapslar. 14-bensig DIP-sockel.",
        "tags": ["sockel", "socket", "DIP-14", "IC-sockel"],
    },
    "DIP-18-SOCKET": {
        "name": "DIP-18 sockel",
        "cat_hint": "övrigt",
        "specs": {"package": "DIP-18", "pins": 18},
        "desc": "IC-sockel för DIP-18-kapslar. 18-bensig DIP-sockel.",
        "tags": ["sockel", "socket", "DIP-18", "IC-sockel"],
    },
}

# ---------------------------------------------------------------------------
# Layout: fack_number (1–128) → component key (or None to skip)
# Duplicates share the same component key → only one component created,
# but two separate stock entries in different compartments.
# ---------------------------------------------------------------------------
LAYOUT = [
    (1, "LNDX829A"),
    (2, "SN74185B"),
    (3, "CD4539"),
    (4, "CD40109"),
    (5, "TBA800"),
    (6, "SN74151N"),
    (7, "DIP-16-SOCKET"),
    (8, "SN7474"),
    (9, "SN74LS373"),
    (10, "SN74LS02"),
    (11, "DIP-8-SOCKET"),
    (12, "CD4024"),
    (13, "NE556"),
    (14, "SN7417"),
    (15, "MC14042"),
    (16, "CD40175"),
    (17, "HM6264LP-12"),
    (18, "74LS85"),       # same component as F0021
    (19, "ULN2004A"),
    (20, "MC14024BCL"),
    (21, "74LS85"),       # duplicate of F0018
    (22, "74LS240"),
    (23, "Z80A"),
    (24, "74LS367"),
    (25, "MC14040BCP"),
    (26, "LM339N"),
    (27, "CD4025"),
    (28, "93438-DC"),
    (29, "SN74LS153N"),
    (30, "DM81LS97N"),
    (31, "9667PC"),
    (32, "74HC21D"),
    (33, "SN74AHCT125"),
    (34, "SN74HC245N"),
    (35, "MCP23017"),
    (36, "ULN2803APG"),
    (37, "K155ID1"),
    (38, "TDF6264APG"),
    (39, "SN74HC595N"),
    (40, "TMP8085AP"),
    (41, "ATmega328P"),
    (42, "CD4067BE"),     # canonical key: CD4067BE → name CD4067
    (43, "ICM7243BIPLZ"),
    (44, "CD4514BCN"),
    (45, "DIP-14-SOCKET"),
    (46, "74LS138"),      # same component as F0055
    (47, "DIP-18-SOCKET"),
    (48, "6561APC"),
    (49, "CD40106BE"),    # same component as F0057
    (50, "DM74L17N"),
    (51, "MM74HC241B1"),
    (52, "SN74105N"),
    (53, "DM4512BE"),
    (54, "HEF4514BP"),
    (55, "74LS138"),      # duplicate of F0046
    (56, "MM74C906N"),
    (57, "CD40106BE"),    # duplicate of F0049
    (58, "7407"),
    (59, "Intel8155"),
    (60, "LM358N"),
    (61, "SN74LS374N"),
    (62, "CD4024"),       # duplicate of F0012
    (63, "SN7406"),       # SN7406A = same as SN7406
    (64, "74LS07"),
    (65, "TL071"),        # TL071CP = TL071
    (66, "LF353"),
    (67, "SN74LS21"),
    (68, "SN74LS173"),
    (69, "SN74S387N"),
    (70, "SN74189AP"),
    (71, "SN7425"),
    (72, "SN7410"),
    (73, "UDN2981A"),
    (74, "TDA1905"),
    (75, "SN74148N"),
    (76, "SN74LS266"),
    (77, "CD4516"),       # same component as F0097
    (78, "SN7417"),       # duplicate of F0014
    (79, "CD4072"),
    (80, "SN7458N"),
    (81, "SN7420N"),
    (82, "SN74LS37"),
    (83, "SN74LS12"),     # same component as F0086
    (84, "T74LS03B1"),
    (85, "LM348"),
    (86, "SN74LS12"),     # duplicate of F0083
    (87, "SN74LS01"),
    (88, "Intel8039"),
    (89, "SN74LS74"),
    (90, "Intel8243"),
    (91, "MAX232"),
    (92, "SN74HC640P"),
    (93, "CD4013"),
    (94, "CD4069"),
    (95, "ULN2804A"),
    (96, "LM381N"),
    (97, "CD4516"),       # duplicate of F0077
    (98, "Intel8216"),
    (99, "LM389"),
    (100, "LM393"),
    (101, "D80C39C"),
    (102, "CD4001"),
    (103, "MC14536"),
    (104, "LS7210"),
    (105, "LM324"),
    (106, "UA741"),
    (107, "CA3089"),
    (108, "CD4093"),
    (109, "CD4015"),
    (110, "SN74LS373"),   # duplicate of F0009
    (111, "CA324E"),
    (112, "CD4012"),
    (113, "CD4067BE"),    # duplicate of F0042
    (114, "CD4050BE"),
    (115, "74LS377N"),
    (116, "CD4040BE"),
    (117, "CD4099"),
    (118, "CD4020"),
    (119, "ULN2002A"),
    (120, "MM5452N"),
    (121, "TCA105"),
    (122, "CD4023"),
    (123, "N82S129"),
    (124, "TL071"),       # duplicate of F0065
    (125, "SN74141"),
    (126, "SN7406"),      # duplicate of F0063
    (127, "74LS75"),
    (128, "CD40175"),     # 40175 = CD40175, duplicate of F0016
]

DRAWER_LABEL = "L21"


def find_category(categories, hint):
    """Find best matching category by hint substring (case-insensitive)."""
    hint_lower = hint.lower()
    # Try exact substring match on name
    for c in categories:
        if hint_lower in c["name"].lower():
            return c["id"]
    # Try slug
    for c in categories:
        if hint_lower in c.get("slug", "").lower():
            return c["id"]
    # Try parent category
    for c in categories:
        if "integrerade" in c["name"].lower() or "ic" in c.get("slug", "").lower():
            return c["id"]
    return None


def main():
    print("=== KOMPIS L06 Seeding Script ===\n")

    # 1. Get categories
    print("Hämtar kategorier...")
    categories = api_get("/api/categories")
    if not categories:
        print("FEL: Kan inte hämta kategorier. Är API:et uppe?", file=sys.stderr)
        sys.exit(1)
    print(f"  Hittade {len(categories)} kategorier:")
    for c in categories:
        print(f"    [{c['id']}] {c['name']} (slug: {c.get('slug', '')})")

    # 2. Find drawer L06
    print(f"\nSöker efter låda {DRAWER_LABEL}...")
    drawers = api_get("/api/drawers")
    drawer = next((d for d in drawers if d["label"] == DRAWER_LABEL), None)
    if not drawer:
        print(f"FEL: Hittade inte låda {DRAWER_LABEL}!", file=sys.stderr)
        sys.exit(1)
    drawer_id = drawer["id"]
    print(f"  Låda {DRAWER_LABEL} har id={drawer_id}")

    # 3. Get existing compartments to avoid duplicates
    print(f"\nHämtar befintliga fack i {DRAWER_LABEL}...")
    drawer_detail = api_get(f"/api/drawers/{drawer_id}")
    existing_compartments = {}
    if drawer_detail and "compartments" in drawer_detail:
        for comp in drawer_detail["compartments"]:
            existing_compartments[comp["label"]] = comp["id"]
    print(f"  {len(existing_compartments)} befintliga fack")

    # 4. Create compartments F0001–F0128
    print(f"\nSkapar fack F0001–F0128...")
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

    # 5. Create unique components (skip duplicates already created)
    print(f"\nSkapar komponenter...")
    created_components = {}  # key → component_id

    for fack_num, comp_key in LAYOUT:
        if comp_key in created_components:
            continue  # already created this component

        if comp_key not in COMPONENTS:
            print(f"  VARNING: Ingen komponentdata för nyckel '{comp_key}'", file=sys.stderr)
            continue

        comp_data = COMPONENTS[comp_key]
        cat_id = find_category(categories, comp_data["cat_hint"])
        specs = {k: v for k, v in (comp_data.get("specs") or {}).items() if k != "manufacturer"}

        payload = {
            "name": comp_data["name"],
            "description": comp_data.get("desc"),
            "category_id": cat_id,
            "manufacturer": comp_data["specs"].get("manufacturer"),
            "part_number": None,
            "tags": comp_data.get("tags") or None,
            "specs": specs or None,
        }

        result, status = api_post("/api/components", payload)
        if result:
            created_components[comp_key] = result["id"]
            print(f"  [{result['id']:4d}] {comp_data['name']}")
        else:
            print(f"  FEL: Skapade inte '{comp_data['name']}' (status={status})", file=sys.stderr)

    print(f"  {len(created_components)} unika komponenter skapade")

    # 6. Create stock entries
    print(f"\nSkapar lagerplatser...")
    stock_count = 0
    for fack_num, comp_key in LAYOUT:
        if comp_key not in created_components:
            continue
        if fack_num not in compartment_ids:
            continue

        comp_id = created_components[comp_key]
        compartment_id = compartment_ids[fack_num]

        result, status = api_post("/api/stock", {
            "component_id": comp_id,
            "compartment_id": compartment_id,
            "quantity": 1,
            "minimum_qty": 0,
            "unit": "st",
            "notes": None,
        })
        if result:
            stock_count += 1
        elif status == 422:
            # Probably already exists (unique constraint), skip silently
            pass
        else:
            fack_label = f"F{fack_num:04d}"
            print(f"  FEL: Kunde inte skapa lager för {fack_label} (status={status})", file=sys.stderr)

    print(f"  {stock_count} lagerplatser skapade")
    print(f"\nKLART! {len(created_components)} komponenter i {len(compartment_ids)} fack i låda {DRAWER_LABEL}.")


if __name__ == "__main__":
    main()
