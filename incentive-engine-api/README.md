# 🔌 Incentive Engine API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A robust FastAPI service that powers the Incentive Engine ecosystem, managing developer wallets, recording reward events, tracking balances, and executing USDC payouts. Available as both a self-hosted solution or a fully-managed SaaS offering.

## ✨ Features

- **Developer Sub-Wallets**: Isolated balances for different use cases or teams
- **Reward Event Tracking**: Complete history of all reward activities
- **Automated USDC Transfers**: Seamless integration with crypto payment rails
- **Real-time Balance Updates**: Instant visibility into wallet funds
- **Comprehensive API**: Simple endpoints for all common operations
- **Enterprise-Ready**: Built for scale with monitoring and observability

## 🛠️ Requirements

- **Python 3.8+**
- **Database**:
  - PostgreSQL (recommended for production)
  - SQLite (supported for local development)
- **Optional Integrations**:
  - Circle API credentials (for USDC transfers)
  - Fireblocks credentials (alternative custody provider)

## 🚀 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourname/incentive-engine.git
cd incentive-engine/incentive-engine-api
```

2. **Install the package**:

```bash
pip install -e .
```

3. **Configure environment variables**:

```bash
cp .env.example .env
# Edit .env to configure your environment
```

## ⚙️ Configuration

Set the following environment variables in your `.env` file:

| Variable | Description | Required | Default |
|----------|-------------|:--------:|:-------:|
| `INCENTIVE_API_KEY` | Master API key for authentication | ✅ | - |
| `DATABASE_URL` | Database connection string | ✅ | - |
| `CIRCLE_API_KEY` | Circle API credentials | - | - |
| `CIRCLE_WALLET_ID` | Circle wallet identifier | - | - |
| `API_HOST` | Host to bind the API server | - | `0.0.0.0` |
| `API_PORT` | Port for the API server | - | `8000` |

## 🚦 Running the Service

### Local Development

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The service will automatically create database tables on first startup.

### Docker Deployment

```bash
docker build -t incentive-engine-api .
docker run -p 8000:8000 --env-file .env incentive-engine-api
```

## 📡 API Endpoints

All endpoints require authentication via the `X-API-KEY` header.

### Core Endpoints

#### Issue a Reward

```
POST /reward
```

Issue a new reward to a user and track the event.

**Request Body**:
```json
{
  "event": "content_created",
  "user_id": "user_abc123",
  "amount": 10.5,
  "metadata": {
    "content_type": "article",
    "quality_score": 9.2
  }
}
```

**Response** (200 OK):
```json
{
  "reward_id": 123,
  "balance": 10.5,
  "status": "pending"
}
```

#### Create Developer Account

```
POST /accounts
```

Provision a new developer sub-wallet for isolated tracking.

**Response** (201 Created):
```json
{
  "account_id": 1,
  "wallet_id": "subwallet_abc",
  "deposit_address": "0x123..."
}
```

#### Get Deposit Address

```
GET /accounts/{account_id}/deposit_address
```

Retrieve the USDC address to fund your sub-wallet.

**Response** (200 OK):
```json
{
  "deposit_address": "0x123..."
}
```

#### Check Balance

```
GET /accounts/{account_id}/balance
```

View the current balance of your sub-wallet.

**Response** (200 OK):
```json
{
  "balance": 42.0
}
```

#### Withdraw Funds

```
POST /accounts/{account_id}/withdraw
```

Transfer USDC from your sub-wallet to an end-user address.

**Request Body**:
```json
{
  "user_address": "0xabc...",
  "amount": 5.0
}
```

**Response** (202 Accepted):
```json
{
  "tx_hash": "0xdeadbeef...",
  "status": "submitted"
}
```

### Additional Endpoints

For a complete list of endpoints and interactive documentation, visit the Swagger UI at `/docs` when the service is running.

## 📂 Project Structure

```
incentive-engine-api/
├── api/
│   ├── main.py              # Application entry point 
│   ├── config.py            # Configuration management
│   ├── db/                  # Database models & migrations
│   │   ├── models.py        # SQLAlchemy models
│   │   └── migrations/      # Alembic migrations
│   ├── models/              # Pydantic schemas
│   │   ├── rewards.py       # Reward schemas
│   │   └── accounts.py      # Account schemas
│   ├── routes/              # API endpoints
│   │   ├── rewards.py       # Reward routes
│   │   └── accounts.py      # Account routes
│   ├── services/            # Business logic
│   │   ├── reward.py        # Reward processing
│   │   ├── accounts.py      # Account management
│   │   └── payment.py       # Payment providers
│   └── utils/               # Helper functions
│       ├── auth.py          # Authentication
│       └── logging.py       # Logging utilities
├── tests/                   # Test suite
│   ├── conftest.py          # Test fixtures
│   ├── test_rewards.py      # Reward tests
│   └── test_accounts.py     # Account tests
├── .env.example             # Example environment variables
├── Dockerfile               # Container definition
├── docker-compose.yml       # Local deployment setup
├── pyproject.toml           # Package definition
└── README.md                # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=api
```

## 🔍 Monitoring & Observability

The API includes several built-in monitoring endpoints:

- `/health` - Service health check
- `/metrics` - Prometheus metrics endpoint
- `/docs` - Interactive API documentation

## 🔒 Security

The API uses several security mechanisms:

- API key authentication for all endpoints
- Rate limiting to prevent abuse
- Input validation with Pydantic
- SQL injection protection via ORM

## 👥 Contributing

We welcome contributions to the Incentive Engine API!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -e .[dev]`)
4. Make your changes
5. Run tests (`pytest`)
6. Submit a Pull Request

Please follow our code style guidelines and include tests for new features.

## 📜 License

Released under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🔗 Related Projects

- [Incentive Engine SDK](../incentive-engine-sdk) - Client library for integrating with this API
- [Incentive Engine Demo](../examples/demo-app) - Example application using the full stack

---