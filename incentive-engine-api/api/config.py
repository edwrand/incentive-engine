# incentive-engine-api/api/config.py

import os

# API key that clients must include in the X-API-KEY header
API_KEY = os.getenv("INCENTIVE_API_KEY")
if not API_KEY:
    raise RuntimeError("INCENTIVE_API_KEY environment variable is required")

# Database connection URL (supports async drivers, default to local SQLite)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite+aiosqlite:///./dev.db"
)

# Custody provider credentials for USDC sub-wallets (Circle, Fireblocks, etc.)
CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY", "")
CIRCLE_WALLET_ID = os.getenv("CIRCLE_WALLET_ID", "")

# (Optional) Override host/port if you deploy behind a proxy
HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", 8000))
