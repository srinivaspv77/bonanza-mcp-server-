
# app/routes_catalog.py
from fastapi import APIRouter, Query, HTTPException
from .schemas import ok
from .metric_catalog import CATALOG
from datetime import datetime, timezone

router = APIRouter(prefix="/catalog", tags=["catalog"])

@router.get("/metrics")
async def list_metrics(limit: int = 100, offset: int = 0):
    keys = list(CATALOG.keys())
    slice_ = keys[offset: offset+limit]
    return ok({
        "current_utc_time": datetime.now(timezone.utc).isoformat(),
        "total_metrics": len(keys),
        "returned_metrics": len(slice_),
        "remaining_metrics": max(0, len(keys) - (offset+len(slice_))),
        "pagination": {
            "limit": limit, "offset": offset,
            "requested_offset": offset,
            "has_more": (offset+len(slice_) < len(keys)),
            "next_offset": (offset+len(slice_)) if (offset+len(slice_) < len(keys)) else None
        },
        "metrics": [f"/catalog/metric/{k}" for k in slice_]
    })

@router.get("/metric/{key}")
async def get_metric_metadata(key: str):
    if key not in CATALOG:
        raise HTTPException(404, "Unknown metric")
    m = CATALOG[key]
    return ok({
        "current_utc_time": datetime.now(timezone.utc).isoformat(),
        "metric": {
            "path": m["path"],
            "family": m["family"],
            "title": m["title"],
            "unit": m["unit"]
        },
        "parameters": m["params"],
        "examples": m["examples"],
        "usage_notes": [
            "All timestamps are Unix ms UTC.",
            "Use max_points to keep payloads small.",
            "Intervals: 1d for long ranges; 1h for short windows."
        ],
        "aliases": m.get("aliases", [])
    })

@router.get("/search")
async def search(q: str = Query(..., min_length=2)):
    ql = q.lower()
    hits = []
    for k, m in CATALOG.items():
        hay = " ".join([k, m["title"], m["family"], " ".join(m.get("aliases", []))]).lower()
        if ql in hay:
            hits.append({"key": k, "title": m["title"], "path": m["path"], "unit": m["unit"]})
    return ok({"query": q, "hits": hits})
