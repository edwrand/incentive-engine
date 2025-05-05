incentive-engine-sdk/README.md

markdown
Copy
Edit
# Incentive Engine SDK

Reward users with programmable USDC incentives in three lines of code.

## Overview

The Incentive Engine SDK lets developers automatically reward user actions—such as signups, referrals, or feedback—in USDC without building payout infrastructure. For example:

```python
from incentive import IncentiveClient

client = IncentiveClient(api_key="your_api_key")
client.reward(event="user_signed_up", user_id="abc123", amount=5)
Installation
bash
Copy
Edit
git clone https://github.com/yourname/incentive-engine.git
cd incentive-engine/incentive-engine-sdk
pip install -e .
Copy and edit the environment template:

bash
Copy
Edit
cp .env.example .env
# set INCENTIVE_API_KEY to your SDK key
Quick Start
python
Copy
Edit
from incentive import IncentiveClient

client = IncentiveClient(api_key="your_api_key")
response = client.reward(
    event="user_signed_up",
    user_id="user_abc",
    amount=5.00,
    metadata={"campaign": "beta-v1"}
)
print(response)
Project Structure
graphql
Copy
Edit
incentive-engine-sdk/
├── incentive/            # Core SDK logic
│   ├── __init__.py
│   ├── client.py         # IncentiveClient implementation
│   ├── config.py         # API base URL configuration
│   ├── exceptions.py     # Custom error classes
│   └── utils.py          # Payload validation and helpers
├── examples/             # Usage examples
│   └── reward_user.py
├── tests/                # Unit tests
│   └── test_client.py
├── .env.example          # Environment variable template
├── .gitignore
├── LICENSE
├── pyproject.toml        # Package metadata
├── setup.cfg             # Linting and formatting settings
└── README.md             # This file
v1.0.0 Features
IncentiveClient(api_key)

reward(event, user_id, amount, metadata={})

Type hints and input validation

Unit tests with pytest

Planned enhancements:

reward_once() to prevent duplicates

Wallet connection and withdrawals

Async support (httpx)

CLI tool (incentive-cli)

Contributing
Fork the repository

Create a branch (feat/your-feature)

Install dev dependencies and run tests:

bash
Copy
Edit
pip install -e .[dev]
pytest
Submit a pull request