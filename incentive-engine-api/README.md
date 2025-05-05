`incentive-engine-api/README.md`**
```markdown
# Incentive Engine API

A FastAPI service that manages per-developer wallets, records reward events, tracks balances, and executes USDC payouts. Can be self-hosted or used as a SaaS endpoint.

## Requirements

- Python 3.8+  
- PostgreSQL (or another supported DB) for production; SQLite is supported for local testing  
- (Optional) Circle or Fireblocks credentials for real-money rails

## Installation

```bash
git clone https://github.com/yourname/incentive-engine.git
cd incentive-engine/incentive-engine-api
pip install -e .
Copy and edit environment variables:

bash
Copy
Edit
cp .env.example .env
# set INCENTIVE_API_KEY, DATABASE_URL, CIRCLE_API_KEY, CIRCLE_WALLET_ID, etc.
Running Locally
bash
Copy
Edit
uvicorn api.main:app --host 0.0.0.0 --port 8000
The database tables will be created automatically on startup.

Configuration
Set the following environment variables (see .env.example):

text
Copy
Edit
INCENTIVE_API_KEY      # Master API key for all endpoints
DATABASE_URL           # e.g. postgresql+asyncpg://user:pass@host/db
CIRCLE_API_KEY         # Custody provider API key (self-hosted or hosted SaaS)
CIRCLE_WALLET_ID       # Custody provider wallet ID
API_HOST               # (Optional) default 0.0.0.0
API_PORT               # (Optional) default 8000
Endpoints
POST /reward
Trigger a reward event for a user.

Request:

json
Copy
Edit
{
  "event": "string",
  "user_id": "string",
  "amount": 10.5,
  "metadata": { "key": "value" }
}
Response:

json
Copy
Edit
{
  "reward_id": 123,
  "balance": 10.5,
  "status": "pending"
}
POST /accounts
Provision a new developer sub-wallet.

Headers: X-API-KEY: <master key>

Response:

json
Copy
Edit
{
  "account_id": 1,
  "wallet_id": "subwallet_abc",
  "deposit_address": "0x123..."
}
GET /accounts/{account_id}/deposit_address
Retrieve the USDC address to fund your sub-wallet.

Response:

json
Copy
Edit
{
  "deposit_address": "0x123..."
}
GET /accounts/{account_id}/balance
Check the current balance of your sub-wallet.

Response:

json
Copy
Edit
{
  "balance": 42.0
}
POST /accounts/{account_id}/withdraw
Send USDC from your sub-wallet to an end-user address.

Request:

json
Copy
Edit
{
  "user_address": "0xabc...",
  "amount": 5.0
}
Response:

json
Copy
Edit
{
  "tx_hash": "0xdeadbeef...",
  "status": "submitted"
}
Project Structure
arduino
Copy
Edit
incentive-engine-api/
├── api/
│   ├── main.py
│   ├── config.py
│   ├── db/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
└── README.md             # This file
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

License
Released under the MIT License. See LICENSE for details.