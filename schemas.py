
def ok(data): 
    return {"ok": True, "data": data}
def clamp(series: list[dict], max_points: int):
    if len(series) <= max_points: 
        return series
    step = max(1, len(series) // max_points)
    return series[::step]
