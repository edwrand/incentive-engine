# examples/reward_user.py

import os
from incentive import IncentiveClient

def main():
    # Load API key from environment variable
    api_key = os.getenv("INCENTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Please set INCENTIVE_API_KEY in your environment")

    # Initialize the client
    client = IncentiveClient(api_key=api_key)

    # Send a reward event
    response = client.reward(
        event="user_signed_up",
        user_id="example_user_123",
        amount=5.00,
        metadata={"campaign": "example_script"}
    )

    # Print the API response
    print("Reward Response:", response)

if __name__ == "__main__":
    main()
