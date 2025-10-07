
from fastapi import APIRouter, Body, HTTPException
from .schemas import ok
from .config import DERIBIT_BASE, HTTP_TIMEOUT, DERIBIT_CLIENT_ID, DERIBIT_CLIENT_SECRET
import httpx, time

router = APIRouter(prefix="/rpc", tags=["rpc"])

_next_id = 1
def _rid():
    global _next_id
    _next_id += 1
    return _next_id

async def _call_jsonrpc(method: str, params: dict | None):
    req = {"jsonrpc":"2.0","id":_rid(),"method":method,"params": params or {}}
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        r = await client.post(f"{DERIBIT_BASE}/api/v2/", json=req)
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            raise HTTPException(status_code=502, detail=data["error"])
        return data.get("result")

@router.post("")
async def rpc_call(payload: dict = Body(...)):
    method = payload.get("method")
    params = payload.get("params", {})
    if not method:
        raise HTTPException(400, "method is required")
    result = await _call_jsonrpc(method, params)
    return ok(result)

# --- private helper with client credentials -----------------------------------
_token_cache = {"access": None, "exp": 0}

async def _ensure_token():
    if not (DERIBIT_CLIENT_ID and DERIBIT_CLIENT_SECRET):
        raise HTTPException(400, "DERIBIT_CLIENT_ID/DERIBIT_CLIENT_SECRET not set")
    now = time.time()
    if _token_cache["access"] and now < _token_cache["exp"] - 60:
        return _token_cache["access"]
    # fetch new token
    params = {
        "grant_type": "client_credentials",
        "client_id": DERIBIT_CLIENT_ID,
        "client_secret": DERIBIT_CLIENT_SECRET
    }
    req = {"jsonrpc":"2.0","id":_rid(),"method":"public/auth","params": params}
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        r = await client.post(f"{DERIBIT_BASE}/api/v2/", json=req)
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            raise HTTPException(status_code=502, detail=data["error"])
        acc = data["result"]["access_token"]
        expires = now + data["result"].get("expires_in", 600)
        _token_cache["access"] = acc
        _token_cache["exp"] = expires
        return acc

@router.post("/private")
async def rpc_private(payload: dict = Body(...)):
    method = payload.get("method")
    params = payload.get("params", {})
    if not method or not method.startswith("private/"):
        raise HTTPException(400, "method must start with 'private/'")
    token = await _ensure_token()
    # Deribit authenticates private methods by Authorization header: Bearer <token>
    req = {"jsonrpc":"2.0","id":_rid(),"method":method,"params": params}
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"Authorization": f"Bearer {token}"}) as client:
        r = await client.post(f"{DERIBIT_BASE}/api/v2/", json=req)
        if r.status_code == 401:
            # refresh and retry once
            token = await _ensure_token()
            client.headers["Authorization"] = f"Bearer {token}"
            r = await client.post(f"{DERIBIT_BASE}/api/v2/", json=req)
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            raise HTTPException(status_code=502, detail=data["error"])
        return ok(data.get("result"))
