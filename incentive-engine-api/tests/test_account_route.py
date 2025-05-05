# incentive-engine-api/tests/test_account_route.py

import pytest
from fastapi.testclient import TestClient

import api.config
from api.main import app

# Set a known master key for tests
api.config.API_KEY = "masterkey"

client = TestClient(app)

@pytest.fixture(autouse=True)
def stub_account_service(monkeypatch):
    """
    Stub out account_service functions so tests don’t hit a real database
    or custody provider.
    """
    class FakeDev:
        id = 1
        api_key = "newkey"
        wallet_id = "wallet123"
        deposit_address = "0xDEADBEEF"

    async def fake_create_account(session):
        return FakeDev()

    async def fake_get_deposit_address(session, account_id):
        if account_id != 1:
            raise Exception("Not found")
        return "0xDEADBEEF"

    async def fake_get_balance(session, account_id):
        if account_id != 1:
            raise Exception("Not found")
        return 123.45

    async def fake_withdraw(session, account_id, user_address, amount):
        if account_id != 1 or amount > 123.45:
            raise Exception("Bad request")
        return "0xTRANSACTIONHASH"

    monkeypatch.setattr(
        "api.services.account_service.create_account",
        fake_create_account,
    )
    monkeypatch.setattr(
        "api.services.account_service.get_deposit_address",
        fake_get_deposit_address,
    )
    monkeypatch.setattr(
        "api.services.account_service.get_balance",
        fake_get_balance,
    )
    monkeypatch.setattr(
        "api.services.account_service.withdraw",
        fake_withdraw,
    )
    yield

def test_create_account_unauthorized():
    """POST /accounts without master key returns 401."""
    response = client.post("/accounts/")
    assert response.status_code == 401

def test_create_account_success():
    """POST /accounts with master key returns new account info."""
    response = client.post(
        "/accounts/",
        headers={"X-API-KEY": api.config.API_KEY},
    )
    assert response.status_code == 201
    assert response.json() == {
        "account_id": 1,
        "wallet_id": "wallet123",
        "deposit_address": "0xDEADBEEF"
    }

def test_get_deposit_address_success():
    """GET /accounts/1/deposit_address returns address."""
    response = client.get("/accounts/1/deposit_address")
    assert response.status_code == 200
    assert response.json() == {"deposit_address": "0xDEADBEEF"}

def test_get_deposit_address_not_found():
    """GET /accounts/2/deposit_address returns 404."""
    response = client.get("/accounts/2/deposit_address")
    assert response.status_code == 404

def test_get_balance_success():
    """GET /accounts/1/balance returns balance."""
    response = client.get("/accounts/1/balance")
    assert response.status_code == 200
    assert response.json() == {"balance": 123.45}

def test_withdraw_success():
    """POST /accounts/1/withdraw with valid amount returns tx hash."""
    payload = {"user_address": "0xUSER", "amount": 100}
    response = client.post("/accounts/1/withdraw", json=payload)
    assert response.status_code == 200
    assert response.json() == {"tx_hash": "0xTRANSACTIONHASH", "status": "submitted"}

def test_withdraw_insufficient_funds():
    """POST /accounts/1/withdraw with too large amount returns 400."""
    payload = {"user_address": "0xUSER", "amount": 200}
    response = client.post("/accounts/1/withdraw", json=payload)
    assert response.status_code == 400
