# incentive-engine-api/tests/test_reward_route.py

import pytest
from fastapi.testclient import TestClient

import api.config
from api.main import app

# Configure the master API key for tests
api.config.API_KEY = "testkey"

client = TestClient(app)


def test_reward_unauthorized():
    """Requests without or with wrong API key return 401."""
    response = client.post("/reward/", json={"event": "e", "user_id": "u", "amount": 1})
    assert response.status_code == 422 or response.status_code == 401

    response = client.post(
        "/reward/",
        json={"event": "e", "user_id": "u", "amount": 1},
        headers={"X-API-KEY": "wrongkey"},
    )
    assert response.status_code == 401


@pytest.fixture(autouse=True)
def stub_process_reward(monkeypatch):
    """
    Replace process_reward with a stub that returns a fixed response.
    """
    async def fake_process_reward(session, api_key, event_name, user_id, amount, metadata):
        return {"reward_id": 42, "balance": amount, "status": "pending"}

    monkeypatch.setattr(
        "api.services.reward_service.process_reward",
        fake_process_reward,
    )
    yield


def test_reward_success():
    """Valid requests with correct API key return the stubbed RewardResponse."""
    payload = {"event": "signup", "user_id": "user123", "amount": 2.5}
    response = client.post(
        "/reward/",
        json=payload,
        headers={"X-API-KEY": api.config.API_KEY},
    )
    assert response.status_code == 200
    assert response.json() == {"reward_id": 42, "balance": 2.5, "status": "pending"}
