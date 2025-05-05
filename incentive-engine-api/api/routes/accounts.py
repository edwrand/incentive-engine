# incentive-engine-api/api/routes/accounts.py

"""
HTTP routes for managing developer accounts and their sub-wallets.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import API_KEY
from api.db.database import SessionLocal
from api.services.account_service import (
    create_account,
    get_deposit_address,
    get_balance,
    withdraw,
)
from api.models.account import (
    AccountCreateResponse,
    DepositAddressResponse,
    BalanceResponse,
    WithdrawRequest,
    WithdrawResponse,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


async def get_session() -> AsyncSession:
    """
    Dependency to yield a database session.
    """
    async with SessionLocal() as session:
        yield session


async def master_auth(x_api_key: str = Header(...)):
    """
    Only the master API key may provision new developer accounts.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: invalid master API key",
        )


@router.post(
    "/",
    response_model=AccountCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(master_auth)],
)
async def create_account_route(session: AsyncSession = Depends(get_session)):
    """
    Provision a new developer account with its own sub-wallet.
    """
    dev = await create_account(session)
    return AccountCreateResponse(
        account_id=dev.id,
        wallet_id=dev.wallet_id,
        deposit_address=dev.deposit_address,
    )


@router.get(
    "/{account_id}/deposit_address",
    response_model=DepositAddressResponse,
)
async def deposit_address_route(
    account_id: int, session: AsyncSession = Depends(get_session)
):
    """
    Return the USDC deposit address for the given developer account.
    """
    address = await get_deposit_address(session, account_id)
    return DepositAddressResponse(deposit_address=address)


@router.get(
    "/{account_id}/balance",
    response_model=BalanceResponse,
)
async def balance_route(
    account_id: int, session: AsyncSession = Depends(get_session)
):
    """
    Return the current USDC balance for the given developer account.
    """
    bal = await get_balance(session, account_id)
    return BalanceResponse(balance=bal)


@router.post(
    "/{account_id}/withdraw",
    response_model=WithdrawResponse,
)
async def withdraw_route(
    account_id: int,
    req: WithdrawRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Debit the developer’s wallet and send USDC to the specified user address.
    """
    tx_hash = await withdraw(session, account_id, req.user_address, req.amount)
    return WithdrawResponse(tx_hash=tx_hash, status="submitted")
