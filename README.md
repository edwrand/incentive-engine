# Incentive Engine

[![PyPI version](https://img.shields.io/pypi/v/incentive-engine-sdk)](https://pypi.org/project/incentive-engine-sdk/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/yourname/incentive-engine/ci.yml?branch=main&label=build%20&logo=github)](https://github.com/yourname/incentive-engine/actions)
[![Codecov](https://img.shields.io/codecov/c/github/yourname/incentive-engine)](https://codecov.io/gh/yourname/incentive-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**A complete solution for issuing, tracking, and disbursing USDC rewards.**

Incentive Engine provides a streamlined way to integrate blockchain based financial rewards into your application with minimal complexity. Whether you're building a Web3 application, a loyalty program, or implementing user incentives, our system handles the entire lifecycle of USDC payments.

## 💡 Key Features

- **One line Reward Issuance** - Integrate rewards with a single function call
- **Isolated Developer Subwallets** - Maintain separate balances for different use cases
- **Automatic Event Logging** - Track all transactions with detailed metadata
- **Enterprise ready USDC Integration** - Connect directly with Circle or Fireblocks
- **Flexible Deployment** - Self host or use our SaaS offering
- **Comprehensive Monitoring** - Built in metrics and health endpoints

## 🏗️ Architecture

Incentive Engine consists of two primary components:

- **Client SDK** (`incentive-engine-sdk/`) – A zero configuration Python library that enables your application to trigger on-chain payouts with minimal code.
- **API Service** (`incentive-engine-api/`) – A robust FastAPI backend that manages wallets, events, balances, and USDC transfers.

## 🚦 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (for production) or SQLite (for local development)
- Optional: Circle or Fireblocks credentials for live USDC transfers
- Docker & Docker Compose (recommended for local setup)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourname/incentive-engine.git
cd incentive-engine
```

2. **Install the SDK**

```bash
cd incentive-engine-sdk
pip install -e .  # Install in development mode
# OR
pip install incentive-engine-sdk  # From PyPI
```

3. **Set up the API Service**

```bash
cd ../incentive-engine-api
pip install -e .
```

### Configuration

Create your environment configuration by copying the example file:

```bash
cp .env.example .env
```

Important configuration values:

| Variable | Description | Default |
|----------|-------------|---------|
| `INCENTIVE_API_KEY` | Master key for API authentication | *Required* |
| `DATABASE_URL` | Connection string for your database | *Required* |
| `CIRCLE_API_KEY` | Circle API credentials | Optional |
| `CIRCLE_WALLET_ID` | Circle wallet identifier | Optional |
| `API_HOST` | Host to bind the API server | `0.0.0.0` |
| `API_PORT` | Port for the API server | `8000` |

## 📘 Usage Examples

### SDK Quickstart

```python
from incentive import IncentiveClient

# Initialize the client
client = IncentiveClient(
    api_key="YOUR_API_KEY",
    host="https://api.yourdomain.com"  # or "http://localhost:8000"
)

# Issue a reward
response = client.reward(
    event="user_signed_up",
    user_id="user_123",
    amount=5.00,
    metadata={"plan": "premium", "source": "referral"}
)

print(f"Reward ID: {response['reward_id']}")
print(f"Updated Balance: ${response['balance']}")
print(f"Status: {response['status']}")
```

### API Service Quickstart

Start the FastAPI service:

```bash
uvicorn api.main:app --reload --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000}
```

## 🔌 API Endpoints

All API requests (except account provisioning) require the header:
```
X-API-KEY: <your-api-key>
```

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reward` | POST | Issue a new reward to a user |
| `/accounts` | POST | Create a new developer sub-wallet |
| `/accounts/{account_id}/deposit_address` | GET | Get your USDC deposit address |
| `/accounts/{account_id}/balance` | GET | Check current wallet balance |
| `/accounts/{account_id}/withdraw` | POST | Transfer USDC to an external address |

### Example: Issue a Reward

```bash
curl -X POST "https://api.yourdomain.com/reward" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "content_created",
    "user_id": "user_abc123",
    "amount": 10.5,
    "metadata": {
      "content_type": "article",
      "quality_score": 9.2
    }
  }'
```

Response:

```json
{
  "reward_id": 123,
  "balance": 10.5,
  "status": "pending"
}
```

For full API documentation, visit the OpenAPI schema at `http://<host>:<port>/docs`.

## 🗂️ Project Structure

```
incentive-engine/
├── incentive-engine-sdk/           # Client SDK
│   ├── incentive/                  # Core implementation
│   ├── examples/                   # Usage examples
│   ├── tests/                      # Unit tests
│   └── pyproject.toml              # Package definition
│
└── incentive-engine-api/           # API Service
    ├── api/
    │   ├── main.py                 # Application entry point
    │   ├── config.py               # Configuration management
    │   ├── db/                     # Database models & migrations
    │   ├── models/                 # Pydantic schemas
    │   ├── routes/                 # API endpoints
    │   ├── services/               # Business logic
    │   └── utils/                  # Helper functions
    ├── tests/                      # Service tests
    ├── Dockerfile                  # Container definition
    └── pyproject.toml              # Package definition
```

## 🧪 Testing

Run the test suite for each component:

```bash
# SDK Tests
cd incentive-engine-sdk
pip install -e .[dev]
pytest

# API Tests
cd ../incentive-engine-api
pip install -e .[dev]
pytest
```

## 💻 Development

We welcome contributions! To get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -e .[dev]`)
4. Make your changes
5. Run tests (`pytest`)
6. Submit a Pull Request

Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [SDK Documentation](incentive-engine-sdk/README.md)
- [API Documentation](incentive-engine-api/README.md)
- [Example Projects](examples/)
- [Issue Tracker](https://github.com/yourname/incentive-engine/issues)

---
