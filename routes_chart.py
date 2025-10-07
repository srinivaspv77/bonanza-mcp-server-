
# app/routes_chart.py
from fastapi import APIRouter, Body
from .schemas import ok
import base64, io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

router = APIRouter(prefix="/chart", tags=["chart"])

@router.post("")
async def chart_png(payload: dict = Body(...)):
    series = payload.get("series", [])  # [{t, v}]
    title = payload.get("title", "Chart")
    unit = payload.get("unit", "")
    if not series:
        return ok({"png_base64": None})
    xs = [pt["t"]/1000 for pt in series]  # seconds
    ys = [pt["v"] for pt in series]
    fig, ax = plt.subplots()
    ax.plot(xs, ys)
    ax.set_title(title)
    ax.set_ylabel(unit)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return ok({"png_base64": b64})
