# tests/test_client.py

import pytest
import requests
from unittest.mock import patch, Mock

from incentive import IncentiveClient
from incentive.exceptions import (
    InvalidPayloadError,
    InvalidTokenError,
    InvalidResponseError,
    IncentiveEngineError,
)


def test_init_without_api_key_raises_invalid_token_error():
    with pytest.raises(InvalidTokenError):
        IncentiveClient(api_key="")


@patch("incentive.client.requests.post")
def test_reward_success(mock_post):
    # Mock a successful HTTP response with JSON
    mock_resp = Mock(status_code=200)
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"status": "ok"}
    mock_post.return_value = mock_resp

    client = IncentiveClient(api_key="test-key")
    response = client.reward(event="test_event", user_id="user123", amount=1.0)

    assert response == {"status": "ok"}
    assert mock_post.called
    called_url = mock_post.call_args[0][0]
    assert called_url.endswith("/reward")


@patch("incentive.client.requests.post", side_effect=requests.RequestException("network fail"))
def test_network_error_raises_incentive_engine_error(mock_post):
    client = IncentiveClient(api_key="test-key")
    with pytest.raises(IncentiveEngineError):
        client.reward(event="test_event", user_id="user123", amount=1.0)


@patch("incentive.client.requests.post")
def test_unauthorized_raises_invalid_token_error(mock_post):
    mock_resp = Mock(status_code=401, text="Unauthorized")
    mock_post.return_value = mock_resp

    client = IncentiveClient(api_key="test-key")
    with pytest.raises(InvalidTokenError):
        client.reward(event="test_event", user_id="user123", amount=1.0)


@patch("incentive.client.requests.post")
def test_http_error_raises_invalid_response_error(mock_post):
    mock_resp = Mock(status_code=500, text="Server error")
    mock_resp.raise_for_status.side_effect = requests.HTTPError(response=mock_resp)
    mock_post.return_value = mock_resp

    client = IncentiveClient(api_key="test-key")
    with pytest.raises(InvalidResponseError):
        client.reward(event="test_event", user_id="user123", amount=1.0)


@patch("incentive.client.requests.post")
def test_invalid_json_raises_invalid_response_error(mock_post):
    mock_resp = Mock(status_code=200)
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.side_effect = ValueError("Invalid JSON")
    mock_post.return_value = mock_resp

    client = IncentiveClient(api_key="test-key")
    with pytest.raises(InvalidResponseError):
        client.reward(event="test_event", user_id="user123", amount=1.0)


def test_invalid_payload_raises_invalid_payload_error():
    client = IncentiveClient(api_key="test-key")
    with pytest.raises(InvalidPayloadError):
        client.reward(event="", user_id="user123", amount=1.0)
    with pytest.raises(InvalidPayloadError):
        client.reward(event="test_event", user_id="", amount=1.0)
    with pytest.raises(InvalidPayloadError):
        client.reward(event="test_event", user_id="user123", amount=0)
