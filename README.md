# Incentive Engine SDK

**Reward your users with programmable USDC, triggered by any in-app behavior—using just 3 lines of code.**

---

## What is this?

The Incentive Engine SDK lets developers **reward users automatically** when they complete defined events (e.g. signing up, referring someone, completing onboarding). Instead of building a custom payout system or integrating Stripe, PayPal, or crypto wallets, you just:

```python
client.reward(event="user_signed_up", user_id="abc123", amount=5)
```

It’s like Stripe—but for programmable incentives.

---

## Why Use This?

- ✅ 5-minute integration  
- 💸 Micro-payouts using **USDC**
- 🧱 Clean reward ledger (no spreadsheets or hacks)
- 🔐 Secure & verifiable reward logic
- 🌍 Borderless + crypto-native payout rail

---

## ⚙️ Installation

Coming soon to PyPI, for now:

```bash
git clone https://github.com/yourname/incentive-engine-sdk.git
cd incentive-engine-sdk
pip install -e .
```

---

## Quick Start

```python
from incentive import IncentiveClient

client = IncentiveClient(api_key="your-api-key")

client.reward(
    event="user_signed_up",
    user_id="user_abc",
    amount=5.00,
    metadata={"campaign": "beta-v1"}
)
```

✅ Reward will be logged, balance credited, and available for withdrawal.

---

## Project Structure

```
incentive-engine/
├── incentive-engine-sdk/
│   ├── incentive/                  # Core SDK logic
│   │   ├── __init__.py
│   │   ├── client.py               # IncentiveClient
│   │   ├── config.py               # API config / base URL
│   │   ├── exceptions.py           # Custom error classes
│   │   └── utils.py                # Payload validation, helpers
│   │
│   ├── examples/                   # Usage examples
│   │   └── reward_user.py
│   │
│   ├── tests/                      # Unit tests
│   │   └── test_client.py
│   │
│   ├── .env.example                # Example API key config
│   ├── .gitignore
│   ├── LICENSE
│   ├── pyproject.toml              # Package metadata
│   ├── setup.cfg                   # Linting configs
│   └── README.md
│
└── incentive-engine-api/
    ├── api/
    │   ├── __init__.py
    │   ├── main.py                  # FastAPI app entrypoint
    │   ├── config.py                # Env var loading
    │   │
    │   ├── db/
    │   │   ├── database.py          # Async engine & session setup
    │   │   └── models.py            # ORM: DeveloperAccount, Event, Reward, UserBalance
    │   │
    │   ├── models/                  # Pydantic schemas
    │   │   ├── reward.py            # RewardRequest & RewardResponse
    │   │   └── account.py           # AccountCreateResponse, DepositAddressResponse, BalanceResponse, Withdraw schemas
    │   │
    │   ├── routes/                  # HTTP route handlers
    │   │   ├── reward.py            # POST /reward
    │   │   └── accounts.py          # POST /accounts, GET deposit_address, GET balance, POST withdraw
    │   │
    │   ├── services/                # Business logic
    │   │   ├── reward_service.py    # process_reward()
    │   │   └── account_service.py   # create_account(), get_deposit_address(), get_balance(), withdraw()
    │   │
    │   └── utils/                   # Helpers
    │       └── auth.py              # API key validation
    │
    ├── tests/                       # API integration tests
    │   ├── test_reward_route.py
    │   └── test_account_route.py
    │
    ├── .env.example                 # Example environment variables
    ├── .gitignore
    ├── Dockerfile
    ├── pyproject.toml               # API packaging & dependencies
    └── README.md
```

---

## Features (v1.0.0)

- `IncentiveClient(api_key)`
- `reward(event, user_id, amount, metadata={})`
- Full type hints + input validation
- Testable with mocked backend
- Pytest-based test coverage

Planned features:
- `reward_once()` to prevent duplicates
- Wallet connection + withdrawal
- Async support (`httpx`)
- CLI: `incentive-cli trigger event user123 --amount 5`

---

## Contributing

I welcome PRs!

1. Fork this repo
2. Create a new branch (`feature/my-feature`)
3. Run tests with `pytest`
4. Submit a pull request with context

---

## License

MIT — free to use, modify, and distribute with credit.

---

## Support

Open an issue or reach out on [X](https://twitter.com/edwrand)

---

## Example Use Cases

- Reward users $5 for signing up  
- Incentivize feedback submissions  
- Pay contributors automatically for PRs or content  
- Build your own USDC-based referral system in minutes

---

Built by [@edwrand](https://github.com/edwrand)
