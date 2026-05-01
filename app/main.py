from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import components, locations, stock, categories, web

app = FastAPI(
    title="KOMPIS API",
    description="KOMPonent Inventarie System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(components.router)
app.include_router(locations.router)
app.include_router(stock.router)
app.include_router(categories.router)
app.include_router(web.router)


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}
