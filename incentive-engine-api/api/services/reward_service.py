# incentive-engine-api/api/services/reward_service.py

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from api.db.models import DeveloperAccount, Event, Reward, UserBalance
from api.models.reward import RewardResponse


async def process_reward(
    session: AsyncSession,
    api_key: str,
    event_name: str,
    user_id: str,
    amount: float,
    metadata: dict
) -> RewardResponse:
    """
    Record a reward event, update user balance, and return the result.
    Raises HTTPException if the developer API key is invalid.
    """
    # 1. Lookup developer account by API key
    stmt = select(DeveloperAccount).where(DeveloperAccount.api_key == api_key)
    try:
        result = await session.execute(stmt)
        developer = result.scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    # 2. Create and persist Event
    event = Event(
        developer_account_id=developer.id,
        event_name=event_name,
        user_id=user_id,
        metadata=metadata
    )
    session.add(event)
    await session.flush()  # assign event.id

    # 3. Create and persist Reward
    reward = Reward(
        event_id=event.id,
        developer_account_id=developer.id,
        amount=amount
    )
    session.add(reward)

    # 4. Update or create UserBalance
    balance_stmt = select(UserBalance).where(
        UserBalance.developer_account_id == developer.id,
        UserBalance.user_id == user_id
    )
    balance_result = await session.execute(balance_stmt)
    user_balance = balance_result.scalar_one_or_none()

    if user_balance:
        user_balance.balance += amount
    else:
        user_balance = UserBalance(
            developer_account_id=developer.id,
            user_id=user_id,
            balance=amount
        )
        session.add(user_balance)

    # 5. Persist all changes
    await session.commit()

    # 6. Return a structured response
    return RewardResponse(
        reward_id=reward.id,
        balance=user_balance.balance,
        status=reward.status
    )
