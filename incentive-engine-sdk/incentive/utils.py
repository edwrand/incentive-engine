# utils.py

def validate_event_payload(event: str, user_id: str, amount: float) -> None:
    if not event or not isinstance(event, str):
        raise ValueError("Invalid event name. Must be a non-empty string.")

    if not user_id or not isinstance(user_id, str):
        raise ValueError("Invalid user_id. Must be a non-empty string.")

    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number.")
