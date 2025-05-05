# incentive-engine-api/api/models/reward.py

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class RewardRequest(BaseModel):
    """
    Schema for POST /reward requests.
    """
    event: str = Field(..., description="Name of the event triggering the reward")
    user_id: str = Field(..., description="Unique identifier for the end user")
    amount: float = Field(..., gt=0, description="Amount of USDC to reward (must be positive)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional extra data")


class RewardResponse(BaseModel):
    """
    Schema for responses to POST /reward.
    """
    reward_id: int = Field(..., description="Internal ID of the created reward record")
    balance: float = Field(..., description="The user's updated USDC balance")
    status: str = Field(..., description="Current status of the reward (e.g., 'pending')")
