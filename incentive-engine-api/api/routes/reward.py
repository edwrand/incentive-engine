# incentive-engine-api/api/routes/reward.py

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import API_KEY
from api.db.database import SessionLocal
from api.models.reward import RewardRequest, RewardResponse
from api.services.reward_service import process_reward

router = APIRouter(prefix="/reward", tags=["reward"])


async def get_session() -> AsyncSession:
    """
    Dependency to yield a database session.
    """
    async with SessionLocal() as session:
        yield session


async def api_key_auth(x_api_key: str = Header(...)):
    """
    Validates the X-API-KEY header against the master key.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: invalid API key",
        )


@router.post("/", response_model=RewardResponse)
async def reward_route(
    req: RewardRequest,
    x_api_key: str = Depends(api_key_auth),
    session: AsyncSession = Depends(get_session),
):
    """
    Handle a reward request: validate auth, call service, return result.
    """
    try:
        return await process_reward(
            session=session,
            api_key=x_api_key,
            event_name=req.event,
            user_id=req.user_id,
            amount=req.amount,
            metadata=req.metadata,
        )
    except HTTPException:
        # propagate HTTPExceptions raised in service (e.g. 401)
        raise
    except Exception as e:
        # catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
