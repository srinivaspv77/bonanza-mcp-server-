
# Bonanza MCP Server

A production-ready **Deribit Gateway** you can deploy to Render and wire into a **Custom GPT** via Actions (OpenAPI).
Includes optional MCP server (see below) and a cron skeleton for skew ingest.

## Quick start (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export API_KEY=dev-key
uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload
```

Open http://localhost:8082/docs for the auto-generated OpenAPI.

## Deploy to Render

1. Push this folder to a new GitHub repo.
2. In Render: **New +** → **Blueprint** → select your repo (uses `render.yaml`).
3. Set env var **API_KEY** in the web service Settings.
4. Once live, your gateway will be at `https://<your-app>.onrender.com/`.

## Custom GPT Action

In GPT Builder → **Actions → Import from URL** → paste `https://<your-app>.onrender.com/openapi.json`.
Add default header: `X-Api-Key: <your API_KEY>`.

## Key endpoints

- `GET /assets`
- `GET /prices/index?asset=BTC&interval=1h`
- `GET /vol/dvol?asset=BTC`
- `GET /vol/hv?asset=BTC&window=30`
- `GET /futures/funding?asset=BTC`
- `GET /indices/fixing?asset=BTC`
- `GET /system/insurance?asset=BTC`
- `GET /system/proof_of_reserves`
- `GET /options/instruments?asset=BTC`
- `GET /options/chain?asset=BTC`
- `GET /options/iv_surface?asset=BTC`
- `GET /options/term_structure?asset=BTC`
- `GET /options/skew_25d?asset=BTC`
- `GET /metric?metric=index_price&asset=BTC` (generic)

## Notes
- DVOL and 25d skew routes are present; DVOL depends on upstream availability, skew history is a DB-backed add-on.
- Tighten CORS with `ALLOWED_ORIGINS` in prod.
- For heavy metrics, precompute via the cron worker.


---

## Discovery endpoints

- `GET /indices` → list of index-like metrics available via the gateway
- `GET /options/metrics` → discover available options aggregates (surface, term structure, skew stubs)
- `GET /futures/metrics` → discover futures metrics (funding is wired; others are placeholders you can extend)

These exist to let AI clients do **discover → browse → fetch** without hardcoding every metric.
