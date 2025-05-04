# incentive-engine-api/api/services/account_service.py

import secrets
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func

from api.db.models import DeveloperAccount, UserBalance
from api.config import CIRCLE_API_KEY, CIRCLE_WALLET_ID


async def provision_subwallet() -> (str, str):
    """
    Stubbed “custody provider” call to create a new sub-wallet.
    Returns (wallet_id, deposit_address). Replace with real API integration.
    """
    # TODO: replace with Circle Connect / Fireblocks API calls
    wallet_id = "subwallet_" + secrets.token_urlsafe(8)
    deposit_address = "0x" + secrets.token_hex(20)
    return wallet_id, deposit_address


async def create_account(session: AsyncSession) -> DeveloperAccount:
    """
    Provision a new DeveloperAccount with its own sub-wallet.
    Generates a unique API key, creates a wallet, and persists both.
    """
    new_api_key = secrets.token_urlsafe(32)
    wallet_id, deposit_address = await provision_subwallet()
    dev = DeveloperAccount(api_key=new_api_key, wallet_id=wallet_id)
    session.add(dev)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create developer account"
        )
    # Optionally store deposit_address somewhere or return it via the route
    dev.deposit_address = deposit_address  # attach for route consumption
    return dev


async def get_deposit_address(session: AsyncSession, account_id: int) -> str:
    """
    Return the USDC deposit address for the given DeveloperAccount.
    """
    dev = await session.get(DeveloperAccount, account_id)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    # If deposit_address were stored in the model, return it; otherwise, derive or call provider
    return getattr(dev, "deposit_address", dev.wallet_id)


async def get_balance(session: AsyncSession, account_id: int) -> float:
    """
    Sum all user balances under this developer to return the total funds available.
    """
    stmt = select(func.sum(UserBalance.balance)).where(
        UserBalance.developer_account_id == account_id
    )
    result = await session.execute(stmt)
    total = result.scalar() or 0.0
    return total


async def withdraw(
    session: AsyncSession,
    account_id: int,
    user_address: str,
    amount: float
) -> str:
    """
    Debit the developer’s balance and initiate a USDC transfer to `user_address`.
    Returns the transaction hash. Stubbed for now.
    """
    # Check account exists
    dev = await session.get(DeveloperAccount, account_id)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    # Check sufficient funds
    available = await get_balance(session, account_id)
    if amount > available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    # TODO: call custody provider to move USDC from dev.wallet_id to user_address
    tx_hash = "0x" + secrets.token_hex(32)

    # Deduct from each UserBalance record or create a Withdrawal record if you have one
    # For simplicity, we could track a net balance elsewhere

    return tx_hash
