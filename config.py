
import os

DERIBIT_BASE = os.getenv("DERIBIT_BASE", "https://www.deribit.com")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "20"))
MAX_POINTS = int(os.getenv("MAX_POINTS", "5000"))
API_KEY = os.getenv("API_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
DATABASE_URL = os.getenv("DATABASE_URL")
DERIBIT_CLIENT_ID = os.getenv("DERIBIT_CLIENT_ID")
DERIBIT_CLIENT_SECRET = os.getenv("DERIBIT_CLIENT_SECRET")
