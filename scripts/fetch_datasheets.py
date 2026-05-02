#!/usr/bin/env python3
"""Download datasheets and upload to KOMPIS for L21 ICs.

Run on rash after seed_l06.py has been executed:
  python3 scripts/fetch_datasheets.py

The script:
1. Downloads each datasheet PDF from a known-good URL
2. Finds the corresponding component in KOMPIS by name
3. Uploads the PDF as a datasheet file
Skips components that already have a datasheet, and silently skips
any URL that fails or returns non-PDF content.
"""
import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_HOST = "localhost"
BASE_PORT = 8000
BASE = f"http://{BASE_HOST}:{BASE_PORT}"

# ---------------------------------------------------------------------------
# Verified working PDF URLs (all return Content-Type: application/pdf)
# Format: (component_search_name, pdf_url, save_filename)
# The search_name is matched against component names in KOMPIS.
# If a component has multiple search names, multiple entries may share a URL.
# ---------------------------------------------------------------------------
DATASHEETS = [
    # --- TTL Logic (Texas Instruments) ---
    ("SN74LS373", "https://www.ti.com/lit/ds/symlink/sn74ls373.pdf", "SN74LS373.pdf"),
    ("SN74LS02",  "https://www.ti.com/lit/ds/symlink/sn74ls02.pdf",  "SN74LS02.pdf"),
    ("SN7474",    "https://www.ti.com/lit/ds/symlink/sn7474.pdf",    "SN7474.pdf"),
    ("SN74LS153N","https://www.ti.com/lit/ds/symlink/sn74ls153.pdf", "SN74LS153.pdf"),
    ("SN74LS374N","https://www.ti.com/lit/ds/symlink/sn74ls374.pdf", "SN74LS374.pdf"),
    ("SN74LS266", "https://www.ti.com/lit/ds/symlink/sn74ls266.pdf", "SN74LS266.pdf"),
    ("SN74LS21",  "https://www.ti.com/lit/ds/symlink/sn74ls21.pdf",  "SN74LS21.pdf"),
    ("SN74LS37",  "https://www.ti.com/lit/ds/symlink/sn74ls37.pdf",  "SN74LS37.pdf"),
    ("SN74LS173", "https://www.ti.com/lit/ds/symlink/sn74ls173a.pdf","SN74LS173.pdf"),
    ("SN74LS74",  "https://www.ti.com/lit/ds/symlink/sn74ls74a.pdf", "SN74LS74.pdf"),
    ("SN74LS01",  "https://www.ti.com/lit/ds/symlink/sn74ls01a.pdf", "SN74LS01.pdf"),
    ("SN74LS21",  "https://www.ti.com/lit/ds/symlink/sn74ls21.pdf",  "SN74LS21.pdf"),
    ("SN74LS240", "https://www.ti.com/lit/ds/symlink/sn74ls240.pdf", "SN74LS240.pdf"),
    ("74LS240",   "https://www.ti.com/lit/ds/symlink/sn74ls240.pdf", "SN74LS240.pdf"),
    ("SN74LS138", "https://www.ti.com/lit/ds/symlink/sn74ls138.pdf", "SN74LS138.pdf"),
    ("74LS138",   "https://www.ti.com/lit/ds/symlink/sn74ls138.pdf", "SN74LS138.pdf"),
    ("74LS07",    "https://www.ti.com/lit/ds/symlink/sn74ls07.pdf",  "SN74LS07.pdf"),
    ("SN7406",    "https://www.ti.com/lit/ds/symlink/sn7406.pdf",    "SN7406.pdf"),
    ("SN7417",    "https://www.ti.com/lit/ds/symlink/sn7417.pdf",    "SN7417.pdf"),
    ("SN7425",    "https://www.ti.com/lit/ds/symlink/sn7425.pdf",    "SN7425.pdf"),
    ("74LS75",    "https://www.ti.com/lit/ds/symlink/sn74ls75.pdf",  "SN74LS75.pdf"),
    ("74LS377N",  "https://www.ti.com/lit/ds/symlink/sn74ls377.pdf", "SN74LS377.pdf"),
    ("74LS367",   "https://www.ti.com/lit/ds/symlink/sn74ls367.pdf", "SN74LS367.pdf"),
    ("74LS85",    "https://www.ti.com/lit/ds/symlink/sn74ls85.pdf",  "SN74LS85.pdf"),
    ("SN74151N",  "https://www.ti.com/lit/ds/symlink/sn74ls151.pdf", "SN74LS151.pdf"),
    ("SN74141",   "https://www.ti.com/lit/ds/symlink/sn74141a.pdf",  "SN74141.pdf"),
    ("SN74148N",  "https://www.ti.com/lit/ds/symlink/sn74148a.pdf",  "SN74148.pdf"),
    ("7407",      "https://www.ti.com/lit/ds/symlink/sn7407.pdf",    "SN7407.pdf"),

    # --- CMOS HC (Texas Instruments) ---
    ("SN74HC245N",  "https://www.ti.com/lit/ds/symlink/sn74hc245.pdf",   "SN74HC245.pdf"),
    ("SN74HC595N",  "https://www.ti.com/lit/ds/symlink/sn74hc595.pdf",   "SN74HC595.pdf"),
    ("SN74AHCT125", "https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf", "SN74AHCT125.pdf"),
    ("SN74HC640P",  "https://www.ti.com/lit/ds/symlink/sn74hc640.pdf",   "SN74HC640.pdf"),
    ("MM74HC241B1", "https://www.ti.com/lit/ds/symlink/sn74hc241.pdf",   "SN74HC241.pdf"),

    # --- CD4000 CMOS (Texas Instruments) ---
    ("CD4001",    "https://www.ti.com/lit/ds/symlink/cd4001b.pdf",   "CD4001B.pdf"),
    ("CD4012",    "https://www.ti.com/lit/ds/symlink/cd4012b.pdf",   "CD4012B.pdf"),
    ("CD4013",    "https://www.ti.com/lit/ds/symlink/cd4013b.pdf",   "CD4013B.pdf"),
    ("CD4015",    "https://www.ti.com/lit/ds/symlink/cd4015b.pdf",   "CD4015B.pdf"),
    ("CD4020",    "https://www.ti.com/lit/ds/symlink/cd4020b.pdf",   "CD4020B.pdf"),
    ("CD4023",    "https://www.ti.com/lit/ds/symlink/cd4023b.pdf",   "CD4023B.pdf"),
    ("CD4024",    "https://www.ti.com/lit/ds/symlink/cd4024b.pdf",   "CD4024B.pdf"),
    ("CD4025",    "https://www.ti.com/lit/ds/symlink/cd4025b.pdf",   "CD4025B.pdf"),
    ("CD4040BE",  "https://www.ti.com/lit/ds/symlink/cd4040b.pdf",   "CD4040B.pdf"),
    ("CD4050BE",  "https://www.ti.com/lit/ds/symlink/cd4050b.pdf",   "CD4050B.pdf"),
    ("CD4067",    "https://www.ti.com/lit/ds/symlink/cd4067b.pdf",   "CD4067B.pdf"),
    ("CD4069",    "https://www.ti.com/lit/ds/symlink/cd4069ub.pdf",  "CD4069UB.pdf"),
    ("CD4072",    "https://www.ti.com/lit/ds/symlink/cd4072b.pdf",   "CD4072B.pdf"),
    ("CD4093",    "https://www.ti.com/lit/ds/symlink/cd4093b.pdf",   "CD4093B.pdf"),
    ("CD4099",    "https://www.ti.com/lit/ds/symlink/cd4099b.pdf",   "CD4099B.pdf"),
    ("CD4516",    "https://www.ti.com/lit/ds/symlink/cd4516b.pdf",   "CD4516B.pdf"),
    ("CD40106BE", "https://www.ti.com/lit/ds/symlink/cd40106b.pdf",  "CD40106B.pdf"),
    ("CD40109",   "https://www.ti.com/lit/ds/symlink/cd40109b.pdf",  "CD40109B.pdf"),
    ("CD40175",   "https://www.ti.com/lit/ds/symlink/cd40175b.pdf",  "CD40175B.pdf"),
    ("CD4514BCN", "https://www.ti.com/lit/ds/symlink/cd4514b.pdf",   "CD4514B.pdf"),

    # --- MC14xxx CMOS (ON Semiconductor) ---
    ("MC14024BCL","https://www.onsemi.com/download/data-sheet/pdf/mc14024b-d.pdf", "MC14024B.pdf"),
    ("MC14040BCP","https://www.onsemi.com/download/data-sheet/pdf/mc14040b-d.pdf", "MC14040B.pdf"),
    ("MC14042",   "https://www.onsemi.com/download/data-sheet/pdf/mc14042b-d.pdf", "MC14042B.pdf"),
    ("MC14536",   "https://www.onsemi.com/download/data-sheet/pdf/mc14536b-d.pdf", "MC14536B.pdf"),

    # --- Op-amps / Comparators (Texas Instruments) ---
    ("LM339N",  "https://www.ti.com/lit/ds/symlink/lm339.pdf",  "LM339.pdf"),
    ("LM358N",  "https://www.ti.com/lit/ds/symlink/lm358.pdf",  "LM358.pdf"),
    ("TL071",   "https://www.ti.com/lit/ds/symlink/tl071.pdf",  "TL071.pdf"),
    ("LF353",   "https://www.ti.com/lit/ds/symlink/lf353.pdf",  "LF353.pdf"),
    ("LM348",   "https://www.ti.com/lit/ds/symlink/lm348.pdf",  "LM348.pdf"),
    ("UA741",   "https://www.ti.com/lit/ds/symlink/ua741.pdf",  "UA741.pdf"),
    ("LM324",   "https://www.ti.com/lit/ds/symlink/lm324.pdf",  "LM324.pdf"),
    ("CA324E",  "https://www.ti.com/lit/ds/symlink/lm324.pdf",  "LM324.pdf"),  # CA324E = LM324 equivalent
    ("LM393",   "https://www.ti.com/lit/ds/symlink/lm393.pdf",  "LM393.pdf"),

    # --- Timers (Texas Instruments) ---
    ("NE556",  "https://www.ti.com/lit/ds/symlink/ne556.pdf", "NE556.pdf"),

    # --- Communication / Interface (Texas Instruments) ---
    ("MAX232",   "https://www.ti.com/lit/ds/symlink/max232.pdf",  "MAX232.pdf"),

    # --- Drivers (Texas Instruments) ---
    ("ULN2004A", "https://www.ti.com/lit/ds/symlink/uln2004a.pdf", "ULN2004A.pdf"),
    ("ULN2002A", "https://www.ti.com/lit/ds/symlink/uln2003a.pdf", "ULN2003A.pdf"),  # same family datasheet

    # --- Microcontrollers (Microchip) ---
    ("ATmega328P", "https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf", "ATmega328P.pdf"),
    ("MCP23017",   "https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP23017-Data-Sheet-DS20001952.pdf", "MCP23017.pdf"),

    # --- Microprocessors (Zilog) ---
    ("Zilog Z80A", "https://www.zilog.com/docs/z80/ps0178.pdf", "Z80A_ProductSpec.pdf"),

    # --- Power / Drivers (ST Microelectronics) ---
    ("ULN2804A", "https://www.st.com/resource/en/datasheet/uln2804a.pdf", "ULN2804A.pdf"),
    ("TDA1905",  "https://www.st.com/resource/en/datasheet/cd00000121.pdf", "TDA1905.pdf"),

    # --- Vintage / Special (MOS Technology archive) ---
    ("MOS 6561 (VIC)", "https://archive.6502.org/datasheets/mos_6560_6561_vic.pdf", "MOS6561_VIC.pdf"),
]

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def api_get(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  GET {path} fel: {e}", file=sys.stderr)
        return None


def download_pdf(url, timeout=30):
    """Download URL, return bytes if it's a PDF, else None."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; KOMPIS-datasheet-fetcher/1.0)",
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ct = r.headers.get("Content-Type", "")
            if "pdf" not in ct.lower():
                return None
            data = r.read()
            if not data.startswith(b"%PDF"):
                return None
            return data
    except Exception:
        return None


def upload_pdf(component_id, pdf_bytes, filename):
    """Upload a PDF datasheet to a component via multipart form POST."""
    boundary = f"--kompis--{os.getpid()}--"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file_type"\r\n\r\n'
        f"datasheet\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode() + pdf_bytes + f"\r\n--{boundary}--\r\n".encode()

    conn = http.client.HTTPConnection(BASE_HOST, BASE_PORT, timeout=30)
    try:
        conn.request(
            "POST",
            f"/components/{component_id}/files",
            body=body,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Content-Length": str(len(body)),
            },
        )
        resp = conn.getresponse()
        return resp.status
    except Exception as e:
        print(f"  Upload fel: {e}", file=sys.stderr)
        return None
    finally:
        conn.close()


def find_component(name):
    """Search KOMPIS for a component by name, return (id, existing_datasheets)."""
    q = urllib.parse.quote(name)
    results = api_get(f"/api/components?q={q}&limit=10")
    if not results:
        return None, 0

    # Exact match first
    name_lower = name.lower()
    for c in results:
        if c["name"].lower() == name_lower:
            sheets = sum(1 for f in c.get("files", []) if f.get("file_type") == "datasheet")
            return c["id"], sheets

    # Substring match
    for c in results:
        if name_lower in c["name"].lower() or c["name"].lower() in name_lower:
            sheets = sum(1 for f in c.get("files", []) if f.get("file_type") == "datasheet")
            return c["id"], sheets

    return None, 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== KOMPIS datasheet fetcher ===\n")

    # Deduplicate: (component_name) → upload at most once per component
    uploaded = set()   # component_ids that already got a datasheet this run
    skipped = 0
    success = 0
    failed_download = []
    not_found = []

    total = len(DATASHEETS)
    for i, (search_name, url, filename) in enumerate(DATASHEETS, 1):
        print(f"[{i:2d}/{total}] {search_name} ... ", end="", flush=True)

        comp_id, existing = find_component(search_name)
        if comp_id is None:
            print("ej hittad i DB")
            not_found.append(search_name)
            continue

        if existing > 0 or comp_id in uploaded:
            print("har redan datablad, hoppar över")
            skipped += 1
            continue

        pdf = download_pdf(url)
        if pdf is None:
            print(f"nedladdning misslyckades ({url[:60]}...)")
            failed_download.append((search_name, url))
            continue

        status = upload_pdf(comp_id, pdf, filename)
        if status in (200, 201):
            print(f"OK ({len(pdf)//1024} KB uppladdad)")
            uploaded.add(comp_id)
            success += 1
        else:
            print(f"upload-fel HTTP {status}")
            failed_download.append((search_name, url))

        time.sleep(0.3)  # polite pause between requests

    print(f"\n=== Sammanfattning ===")
    print(f"  Uppladdade:      {success}")
    print(f"  Redan hade blad: {skipped}")
    print(f"  Ej i DB:         {len(not_found)}")
    print(f"  Misslyckades:    {len(failed_download)}")

    if failed_download:
        print("\nMisslyckade nedladdningar:")
        for name, url in failed_download:
            print(f"  {name}: {url}")

    if not_found:
        print("\nHittades inte i databasen (kör seed_l06.py först?):")
        for name in not_found:
            print(f"  {name}")


if __name__ == "__main__":
    main()
