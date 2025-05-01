# incentive-engine-api/api/models/account.py

from pydantic import BaseModel, Field
from typing import Optional


class AccountCreateResponse(BaseModel):
    """
    Response schema for POST /accounts.
    """
    account_id: int = Field(..., description="Internal ID of the developer account")
    wallet_id: str = Field(..., description="Custody provider sub-wallet identifier")
    deposit_address: str = Field(
        ..., description="USDC address where the developer should top up funds"
    )


class DepositAddressResponse(BaseModel):
    """
    Response schema for GET /accounts/{account_id}/deposit_address.
    """
    deposit_address: str = Field(
        ..., description="USDC address where the developer should send funds"
    )


class BalanceResponse(BaseModel):
    """
    Response schema for GET /accounts/{account_id}/balance.
    """
    balance: float = Field(..., description="Current USDC balance in the developer's wallet")


class WithdrawRequest(BaseModel):
    """
    Request schema for POST /accounts/{account_id}/withdraw.
    """
    user_address: str = Field(..., description="On-chain address (EOA) to send USDC to")
    amount: float = Field(..., gt=0, description="Amount of USDC to withdraw (must be positive)")


class WithdrawResponse(BaseModel):
    """
    Response schema for POST /accounts/{account_id}/withdraw.
    """
    tx_hash: str = Field(..., description="Transaction hash of the USDC transfer")
    status: str = Field(..., description="Resulting status (e.g., 'submitted')")
