# incentive-engine-api/api/utils/auth.py

from fastapi import Header, HTTPException, status
from api.config import API_KEY

async def api_key_auth(x_api_key: str = Header(..., alias="X-API-KEY")) -> str:
    """
    FastAPI dependency to enforce X-API-KEY header matches the master key.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: invalid API key"
        )
    return x_api_key
