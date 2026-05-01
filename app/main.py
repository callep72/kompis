from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.routers import components, locations, stock, categories, files, web

MAX_UPLOAD_BYTES = 50 * 1024 * 1024


class FileSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            cl = request.headers.get("content-length")
            if cl and int(cl) > MAX_UPLOAD_BYTES:
                return Response("Filen är större än 50 MB", status_code=413)
        return await call_next(request)


app = FastAPI(
    title="KOMPIS API",
    description="KOMPonent Inventarie System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(FileSizeLimitMiddleware)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/files", StaticFiles(directory=settings.file_storage_path), name="files")

app.include_router(components.router)
app.include_router(locations.router)
app.include_router(stock.router)
app.include_router(categories.router)
app.include_router(files.router)
app.include_router(web.router)


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}
