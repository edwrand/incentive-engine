# 🚀 Incentive Engine SDK

[![PyPI version](https://img.shields.io/pypi/v/incentive-engine-sdk)](https://pypi.org/project/incentive-engine-sdk/)
[![Python Versions](https://img.shields.io/pypi/pyversions/incentive-engine-sdk)](https://pypi.org/project/incentive-engine-sdk/)
[![Downloads](https://img.shields.io/pypi/dm/incentive-engine-sdk)](https://pypi.org/project/incentive-engine-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Reward users with programmable USDC incentives in just three lines of code.**

## 🔍 Overview

The Incentive Engine SDK enables developers to automatically reward user actions—such as signups, content creation, referrals, or feedback—with USDC payments, without having to build complex payout infrastructure. Our lightweight client handles all the complexity of blockchain transactions while providing a simple, intuitive interface.

```python
from incentive import IncentiveClient

client = IncentiveClient(api_key="YOUR_API_KEY")
client.reward(event="user_signed_up", user_id="abc123", amount=5)
```

## ✨ Key Features

- **Simple Integration** - Reward users with just a few lines of code
- **Flexible Event Tracking** - Define custom events for any user action
- **Detailed Metadata** - Attach contextual information to each reward
- **Type Safety** - Full type hinting and validation for Python 3.8+
- **Comprehensive Error Handling** - Clear error messages and recovery paths
- **Minimal Dependencies** - Lightweight footprint with few requirements

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install incentive-engine-sdk
```

### From Source

```bash
git clone https://github.com/yourname/incentive-engine.git
cd incentive-engine/incentive-engine-sdk
pip install -e .
```

## ⚙️ Configuration

Create an environment file or set environment variables directly:

```bash
cp .env.example .env
# Edit .env to set your INCENTIVE_API_KEY
```

You can also pass configuration directly to the client:

```python
client = IncentiveClient(
    api_key="YOUR_API_KEY",
    host="https://api.custom-domain.com",  # Optional
    timeout=30  # Optional (seconds)
)
```

## 🚀 Quick Start

### Basic Usage

```python
from incentive import IncentiveClient

# Initialize the client
client = IncentiveClient(api_key="YOUR_API_KEY")

# Reward a user for an action
response = client.reward(
    event="user_signed_up",
    user_id="user_abc123",
    amount=5.00,
    metadata={"campaign": "spring_promotion", "source": "referral"}
)

print(f"Reward ID: {response['reward_id']}")
print(f"Current Balance: ${response['balance']}")
print(f"Status: {response['status']}")
```

### Handling Success and Errors

```python
from incentive import IncentiveClient, IncentiveError, InsufficientFundsError

client = IncentiveClient(api_key="YOUR_API_KEY")

try:
    response = client.reward(
        event="premium_content_accessed",
        user_id="user_xyz789",
        amount=2.50
    )
    print(f"Reward successful! ID: {response['reward_id']}")
    
except InsufficientFundsError:
    print("Your account needs more funds. Please deposit USDC.")
    
except IncentiveError as e:
    print(f"An error occurred: {e}")
```

## 📚 API Reference

### IncentiveClient

```python
class IncentiveClient:
    def __init__(
        self, 
        api_key: str, 
        host: Optional[str] = None,
        timeout: Optional[int] = 10
    ):
        """
        Initialize the Incentive Engine client.
        
        Args:
            api_key: Your API key from the Incentive Engine dashboard
            host: Optional custom API host (defaults to production API)
            timeout: Optional request timeout in seconds
        """
        ...
    
    def reward(
        self,
        event: str,
        user_id: str,
        amount: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Issue a reward to a user.
        
        Args:
            event: The type of event that triggered this reward
            user_id: Unique identifier for the rewarded user
            amount: Reward amount in USDC
            metadata: Optional additional context about the reward
            
        Returns:
            Dict containing reward_id, balance, and status
            
        Raises:
            IncentiveError: Base exception for all SDK errors
            AuthenticationError: Invalid API key
            InsufficientFundsError: Not enough USDC in your account
            RateLimitError: Too many requests in a short period
            APIError: Error response from the Incentive API
        """
        ...
```

## 🔧 Advanced Usage

### Custom Event Types

Define event types that match your product's user journey:

```python
# Onboarding events
client.reward(event="account_created", user_id="user1", amount=1.00)
client.reward(event="profile_completed", user_id="user1", amount=2.00)
client.reward(event="first_purchase", user_id="user1", amount=5.00)

# Content creation events
client.reward(event="article_published", user_id="user2", amount=3.00)
client.reward(event="video_uploaded", user_id="user2", amount=10.00)

# Community engagement
client.reward(event="question_answered", user_id="user3", amount=0.50)
client.reward(event="referred_new_user", user_id="user3", amount=20.00)
```

### Rich Metadata

Provide additional context with each reward:

```python
client.reward(
    event="content_created",
    user_id="creator_42",
    amount=15.00,
    metadata={
        "content_type": "article",
        "content_id": "article_789",
        "word_count": 1250,
        "quality_score": 0.92,
        "categories": ["blockchain", "defi", "tutorial"],
        "promotion_eligible": True
    }
)
```

## 📂 Project Structure

```
incentive-engine-sdk/
├── incentive/                # Core SDK implementation
│   ├── __init__.py           # Package exports
│   ├── client.py             # IncentiveClient implementation
│   ├── config.py             # Configuration management
│   ├── exceptions.py         # Custom error classes
│   └── utils.py              # Helper functions and validation
├── examples/                 # Usage examples
│   ├── basic_usage.py        # Simple reward example
│   ├── error_handling.py     # Comprehensive error handling
│   └── advanced_usage.py     # Complex integrations
├── tests/                    # Test suite
│   ├── conftest.py           # Test fixtures
│   ├── test_client.py        # Client tests
│   └── test_utils.py         # Utility function tests
├── .env.example              # Environment variable template
├── pyproject.toml            # Package metadata
├── setup.cfg                 # Development tool configuration
└── README.md                 # This file
```

## 🗺️ Roadmap

Features planned for upcoming releases:

| Feature | Description | Target Version |
|---------|-------------|---------------|
| `reward_once()` | Prevent duplicate rewards for the same event/user | v1.1.0 |
| Wallet Connection | Direct integration with user crypto wallets | v1.2.0 |
| Async Support | Native async/await using httpx | v1.3.0 |
| CLI Tool | Command-line interface for rewards | v2.0.0 |
| Batch Operations | Process multiple rewards in one request | v2.0.0 |
| Webhooks | Event notifications for reward status changes | v2.1.0 |

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=incentive
```

## 👥 Contributing

We welcome contributions to the Incentive Engine SDK!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -e .[dev]`)
4. Make your changes
5. Run tests (`pytest`)
6. Submit a Pull Request

Please see our [Contributing Guidelines](../CONTRIBUTING.md) for more details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [API Documentation](https://docs.incentive-engine.com)
- [Example Projects](https://github.com/yourname/incentive-engine-examples)
- [Community Forum](https://community.incentive-engine.com)

---