# KOMPIS – KOMPonent Inventarie System

Ett sökbart register för elektronikkomponenter med stöd för naturligt språk via AI.

---

## Funktioner

- Hierarkiskt register över lådor och fack
- Sökbar komponentdatabas med tekniska specifikationer
- Datablad och bilder per komponent, inklusive AI-genererade komponentbilder
- Etikettutskrift på Zebra-skrivare med kategorispecifika symboler
- REST API med automatisk OpenAPI-dokumentation
- Naturligt språksök via Claude AI och MCP
- Responsivt webb-GUI tillgängligt för vänner via [kompis.duplo.cc](https://kompis.duplo.cc)

---

## Teknikstack

| Komponent | Teknik |
|-----------|--------|
| Databas | PostgreSQL 16 + pgvector |
| Sökning | Fulltextsökning på svenska via tsvector |
| API | FastAPI med OpenAPI-dokumentation |
| AI-integration | MCP-server (Model Context Protocol) |
| Drift | Docker Compose |
| Proxy | HAProxy + Let's Encrypt |

---

## Arkitektur

```
kompis.duplo.cc
    ├── /          → Webb-GUI
    ├── /api/      → FastAPI
    ├── /api/docs  → Swagger UI
    └── /mcp/      → MCP-server
```

---

## Fasindelning

| Fas | Innehåll | Status |
|-----|----------|--------|
| 1 | Grund, CRUD, sökning, webb-GUI, autentisering | 🚧 Pågår |
| 2 | Filer, datablad, AI-genererade bilder, etiketter | ⏳ Planerad |
| 3 | MCP, naturligt språksök, extern åtkomst för vänner | ⏳ Planerad |
| 4 | BOM-generering, kopplingsscheman, semantisk sökning | ⏳ Planerad |

---

API-dokumentation finns tillgänglig på `http://localhost:8000/api/docs` efter uppstart.

---

## Licens

Privat projekt – alla rättigheter förbehållna.
