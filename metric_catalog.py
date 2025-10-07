
# app/metric_catalog.py
CATALOG = {
    "index_price": {
        "title": "Index Price",
        "family": "indices",
        "path": "/prices/index",
        "unit": "USD",
        "params": {"asset": ["BTC","ETH"], "interval": ["1h","1d"], "max_points": "int"},
        "examples": [
            {"endpoint": "/metric", "params": {"metric":"index_price","asset":"BTC","interval":"1h","max_points": 600}},
            {"endpoint": "/metric", "params": {"metric":"index_price","asset":"ETH","interval":"1d","max_points": 700}}
        ],
        "aliases": ["price","spot","index"]
    },
    "dvol": {
        "title": "Deribit Volatility Index (DVOL)",
        "family": "volatility",
        "path": "/vol/dvol",
        "unit": "%",
        "params": {"asset": ["BTC","ETH"], "interval": ["1d"], "max_points": "int"},
        "examples": [
            {"endpoint": "/metric", "params": {"metric":"dvol","asset":"BTC","interval":"1d","max_points": 600}}
        ],
        "aliases": ["vol index","volatility index","dvol"]
    },
    "funding_rate": {
        "title": "Perpetual Funding Rate",
        "family": "futures",
        "path": "/futures/funding",
        "unit": "%/8h",
        "params": {"asset": ["BTC","ETH"], "max_points": "int"},
        "examples": [
            {"endpoint": "/metric", "params": {"metric":"funding_rate","asset":"BTC","max_points": 500}}
        ],
        "aliases": ["funding","funding rate","perp funding"]
    },
    "hv_30d": {
        "title": "30-Day Realized Volatility",
        "family": "volatility",
        "path": "/vol/hv",
        "unit": "%",
        "params": {"asset": ["BTC","ETH"], "window": [30]},
        "examples": [
            {"endpoint": "/metric", "params": {"metric":"hv_30d","asset":"BTC"}}
        ],
        "aliases": ["realized vol","historical vol","hv"]
    },
    "iv_surface": {
        "title": "Options IV Surface (sampled)",
        "family": "options",
        "path": "/options/iv_surface",
        "unit": "%",
        "params": {"asset": ["BTC","ETH"]},
        "examples": [
            {"endpoint": "/options/iv_surface", "params": {"asset":"BTC"}}
        ],
        "aliases": ["surface","iv surface","vol surface"]
    },
    "term_structure": {
        "title": "Options Term Structure (avg IV by expiry)",
        "family": "options",
        "path": "/options/term_structure",
        "unit": "%",
        "params": {"asset": ["BTC","ETH"]},
        "examples": [
            {"endpoint": "/options/term_structure", "params": {"asset":"BTC"}}
        ],
        "aliases": ["term structure","iv term","smile across expiries"]
    }
}
