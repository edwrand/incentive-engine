# incentive/client.py

import requests
from typing import Optional, Dict, Any

from .config import API_BASE_URL
from .exceptions import (
    InvalidPayloadError,
    InvalidTokenError,
    InvalidResponseError,
    IncentiveEngineError,
)
from .utils import validate_event_payload


class IncentiveClient:
    """
    SDK client for sending reward events to the Incentive Engine API.
    """

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        # Validate API key
        if not api_key or not isinstance(api_key, str):
            raise InvalidTokenError("API key must be a non-empty string.")
        self.api_key = api_key
        # Allow overriding the endpoint (e.g., for testing)
        self.base_url = base_url or API_BASE_URL.rstrip("/")

    def reward(
        self,
        event: str,
        user_id: str,
        amount: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send a reward event to the API.

        :param event: Name of the event (e.g., "user_signed_up").
        :param user_id: Unique identifier for the user.
        :param amount: Positive number of USDC to reward.
        :param metadata: Optional dict of extra data to attach.

        :returns: Parsed JSON response from the API.
        :raises: InvalidPayloadError, InvalidTokenError, InvalidResponseError, IncentiveEngineError
        """
        # Validate inputs
        try:
            validate_event_payload(event, user_id, amount)
        except ValueError as ve:
            raise InvalidPayloadError(str(ve))

        payload = {
            "event": event,
            "user_id": user_id,
            "amount": amount,
            "metadata": metadata or {},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/reward"
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 401:
                raise InvalidTokenError("Unauthorized: check your API key.")
            response.raise_for_status()
        except InvalidTokenError:
            raise
        except requests.HTTPError as he:
            raise InvalidResponseError(f"HTTP error: {he.response.text}") from he
        except requests.RequestException as re:
            raise IncentiveEngineError(f"Network error: {str(re)}") from re

        # Parse response JSON
        try:
            return response.json()
        except ValueError as ve:
            raise InvalidResponseError("Invalid JSON in response.") from ve
