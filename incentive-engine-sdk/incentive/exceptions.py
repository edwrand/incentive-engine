# incentive/exceptions.py

class IncentiveEngineError(Exception):
    """Base exception for all Incentive Engine SDK errors."""
    pass

class InvalidPayloadError(IncentiveEngineError):
    """Raised when the provided payload (event, user_id, amount) is invalid."""
    pass

class InvalidTokenError(IncentiveEngineError):
    """Raised when the API key/token is missing or invalid."""
    pass

class InvalidResponseError(IncentiveEngineError):
    """Raised when the server response is unexpected or malformed."""
    pass
