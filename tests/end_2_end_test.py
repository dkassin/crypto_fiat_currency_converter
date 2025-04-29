import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.prices import set_prices
from app.request_tracker import request_log
from decimal import Decimal
from datetime import datetime, timezone

client = TestClient(app)

VALID_API_KEY = "test-api-key-1"

def test_end_to_end_conversion():
    # Pre-load prices manually
    fake_rates = {
        "BTC": "0.00001", 
        "ETH": "0.0005",   
        "EUR": "0.9",      
    }
    set_prices("USD", fake_rates)

    # Make real API call
    response = client.get(
        "/convert?from=USD&to=BTC&amount=1000",
        headers={"x-api-key": VALID_API_KEY}
    )
    # Validate HTTP response
    assert response.status_code == 200

    # Validate content
    data = response.json()
    assert data["source_currency"] == "USD"
    assert data["final_currency"] == "BTC"
    assert Decimal(data["amount"]) == Decimal("1000")
    assert Decimal(data["exchange_rate"]) == Decimal("0.00001")
    assert Decimal(data["converted_amount"]) == Decimal("0.01")

    # Validate request tracking
    today = datetime.now(timezone.utc).date()
    assert VALID_API_KEY in request_log
    assert today in request_log[VALID_API_KEY]
    assert request_log[VALID_API_KEY][today]["count"] >= 1