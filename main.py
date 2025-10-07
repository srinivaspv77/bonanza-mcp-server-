
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bonanza MCP Server - Deribit Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"ok": True}

from app.routes_catalog import router as catalog_router
from app.routes_chart import router as chart_router
app.include_router(catalog_router)
app.include_router(chart_router)
