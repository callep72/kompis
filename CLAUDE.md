# KOMPIS – KOMPonent Inventarie System

## Projektöversikt

KOMPIS är ett sökbart register för elektronikkomponenter byggt med FastAPI och PostgreSQL.
Det ska köras på en Ubuntu 24.04 VM med Docker Compose och exponeras via HAProxy på kompis.duplo.cc.

## Teknikstack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic
- **Databas**: PostgreSQL 16 + pgvector extension
- **Containerisering**: Docker Compose
- **Sökning**: PostgreSQL fulltextsökning med svenska språkstödet (tsvector/tsquery)

## Arkitektur

```
kompis.duplo.cc
    ├── /          → Webb-GUI (Fas 3)
    ├── /api/      → FastAPI
    ├── /api/docs  → Swagger UI (automatisk)
    └── /mcp/      → MCP-server (Fas 3)
```

## Projektstruktur

```
kompis/
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 001_initial_schema.py
└── app/
    ├── main.py
    ├── database.py
    ├── config.py
    ├── models/
    │   ├── __init__.py
    │   └── models.py
    ├── schemas/
    │   ├── __init__.py
    │   └── schemas.py
    ├── routers/
    │   ├── __init__.py
    │   ├── components.py
    │   ├── locations.py
    │   ├── stock.py
    │   └── categories.py
    └── services/
        ├── __init__.py
        ├── component_service.py
        ├── location_service.py
        ├── stock_service.py
        └── category_service.py
```

## Datamodell

### Hierarki
```
Låda (Drawer) L01-L30+
    └── Fack (Compartment) F0001+ (globalt löpnummer)
            └── Komponent (Component)
                    └── Lager (Stock)
```

### Tabeller

**drawers**
- id: SERIAL PRIMARY KEY
- label: VARCHAR(10) UNIQUE NOT NULL  -- "L01", "L02" etc
- description: TEXT

**compartments**
- id: SERIAL PRIMARY KEY
- drawer_id: FK → drawers
- label: VARCHAR(10) UNIQUE NOT NULL  -- "F0001", "F0002" etc (globalt löpnummer)
- active: BOOLEAN DEFAULT true        -- soft delete, aldrig radera fysiskt
- description: TEXT
- UNIQUE(drawer_id, label)

**categories**
- id: SERIAL PRIMARY KEY
- parent_id: FK → categories (self-referencing träd)
- name: VARCHAR(100) NOT NULL
- slug: VARCHAR(100) UNIQUE NOT NULL  -- "transistors/npn"

**components**
- id: SERIAL PRIMARY KEY
- name: VARCHAR(200) NOT NULL
- description: TEXT
- category_id: FK → categories
- manufacturer: VARCHAR(100)
- part_number: VARCHAR(100)           -- tillverkarens artikelnummer
- tags: TEXT[]                        -- PostgreSQL array
- specs: JSONB                        -- {"resistance": "10k", "tolerance": "1%", "package": "0805"}
- active: BOOLEAN DEFAULT true        -- soft delete
- search_vector: TSVECTOR             -- automatiskt uppdaterat via trigger
- created_at: TIMESTAMPTZ DEFAULT now()
- updated_at: TIMESTAMPTZ DEFAULT now()

**stock**
- id: SERIAL PRIMARY KEY
- component_id: FK → components
- compartment_id: FK → compartments
- quantity: INTEGER DEFAULT 0
- minimum_qty: INTEGER DEFAULT 0      -- varning vid underskridande
- unit: VARCHAR(20) DEFAULT 'st'
- notes: TEXT
- UNIQUE(component_id, compartment_id)

**files**
- id: SERIAL PRIMARY KEY
- component_id: FK → components
- file_type: VARCHAR(20)              -- 'datasheet', 'image', 'schematic' (öppen lista)
- source: VARCHAR(20) DEFAULT 'upload' -- 'upload' eller 'ai_generated'
- filename: VARCHAR(255) NOT NULL
- filepath: TEXT NOT NULL             -- relativ sökväg, t.ex. "components/0001/datasheet.pdf"
- mime_type: VARCHAR(100)
- is_primary: BOOLEAN DEFAULT false   -- primär bild för komponenten
- created_at: TIMESTAMPTZ DEFAULT now()

### PostgreSQL-index
- GIN-index på components.search_vector
- GIN-index på components.tags
- GIN-index på components.specs

### Trigger för fulltextsökning
Trigger på components BEFORE INSERT OR UPDATE som uppdaterar search_vector:
- name → vikt A
- part_number → vikt A
- description → vikt B
- manufacturer → vikt C
Använd svenska språkkonfigurationen: to_tsvector('swedish', ...)

## API-endpoints

### Komponenter – /api/components
- GET    /api/components              – lista/sök, query params: q, category_id, in_stock, skip, limit
- GET    /api/components/{id}         – hämta en komponent med stock och files
- POST   /api/components              – skapa
- PUT    /api/components/{id}         – uppdatera
- DELETE /api/components/{id}         – soft delete (sätt active=false)

### Platser – /api/drawers + /api/compartments
- GET    /api/drawers                 – lista alla lådor
- GET    /api/drawers/{id}            – låda med fack
- POST   /api/drawers                 – skapa låda
- GET    /api/compartments/{id}       – fack med innehåll
- POST   /api/compartments            – skapa fack
- PUT    /api/compartments/{id}       – uppdatera fack

### Lager – /api/stock
- GET    /api/stock                   – lista, query param: low_stock (bool)
- POST   /api/stock                   – skapa lagerrad
- PUT    /api/stock/{id}              – uppdatera antal

### Kategorier – /api/categories
- GET    /api/categories              – lista alla
- GET    /api/categories/{id}         – hämta en
- POST   /api/categories              – skapa
- PUT    /api/categories/{id}         – uppdatera

### Hälsokontroll
- GET    /api/health                  – returnerar {"status": "ok"}

## Viktiga designbeslut

- **Soft delete överallt** – inget raderas fysiskt, sätt active=false
- **Fillagring** – filer lagras på disk under /data/files/components/{id}/
  Sökvägen i databasen är relativ, rotsökvägen kommer från config
- **JSONB för specs** – ger flexibilitet utan schemaändringar när nya komponenttyper läggs till
- **Globala facknummer** – F0001 är unikt i hela systemet, inte bara per låda
- **Fulltextsökning på svenska** – tsvector med 'swedish' konfiguration
- **Search vector trigger** – uppdateras automatiskt, aldrig manuellt

## Konfiguration (.env)

```
DB_USER=kompis
DB_PASSWORD=<hemligt>
DATABASE_URL=postgresql://kompis:<hemligt>@db/kompis
FILE_STORAGE_PATH=/data/files
ZEBRA_PRINTER_IP=192.168.1.100
ZEBRA_PRINTER_PORT=9100
```

## Docker Compose

Tre services:
1. **db** – pgvector/pgvector:pg16, data i namngiven volume postgres_data
2. **app** – FastAPI, port 8000, --reload för utveckling, monterar ./data/files och ./app

Healthcheck på db innan app startar.

## Fas-plan

- **Fas 1** (detta): Grund, CRUD, sökning, Docker (PÅGÅR)
- **Fas 2**: Filuppladdning, AI-bildgenerering via OpenAI, Zebra-etiketter med ZPL
- **Fas 3**: MCP-server, naturligt språksök via Claude API, webb-GUI
- **Fas 4**: BOM-generering, semantisk sökning med pgvector

## Instruktioner till Claude Code

1. Skapa hela projektstrukturen enligt ovan i nuvarande katalog
2. Implementera alla filer enligt specifikationen
3. Se till att `docker compose up -d` fungerar
4. Se till att `docker compose exec app alembic upgrade head` skapar alla tabeller korrekt
5. Verifiera att Swagger UI är tillgänglig på http://localhost:8000/api/docs
6. Commit varje logisk del separat med beskrivande commit-meddelanden på engelska
