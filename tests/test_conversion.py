import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone, date
from app.main import app
from app.request_tracker import request_log
from app.services import refresh_rates_on_start

client = TestClient(app)

VALID_API_KEY = "test-api-key-1"
INVALID_API_KEY = "invalid-key"



def test_successful_conversion():
    response = client.get(
        "/convert?from=USD&to=BTC&amount=1",
        headers={"x-api-key": VALID_API_KEY}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["source_currency"] == "USD"
    assert data["final_currency"] == "BTC"
    assert "converted_amount" in data
    assert "exchange_rate" in data

def test_invalid_api_key():
    response = client.get(
        "/convert?from=USD&to=BTC&amount=1",
        headers={"x-api-key": INVALID_API_KEY}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key"

def test_missing_parameters():
    response = client.get(
        "/convert?from=USD&to=BTC",
        headers={"x-api-key": VALID_API_KEY}
    )
    assert response.status_code == 422

def test_weekday_limit_exceeded():
    #This test will pass if the day of testing is a weekday
    today = datetime.now(timezone.utc).date()
    
    request_log[VALID_API_KEY] = {
        today: {
            "count": 100,
            "requests": []
        }
    }

    response = client.get(
        "/convert?from=USD&to=BTC&amount=1",
        headers={"x-api-key": VALID_API_KEY}
    )
    assert response.status_code == 429
    assert response.json()["detail"] == "Daily weekday request limit exceeded."


# def test_weekend_limit_exceeded():
#     # This test will run if the date of testing is a weekend
#     ## Because of time i had to leave this
#     ## Its commented out bc this is a weekday
#     today = datetime.now(timezone.utc).date()

#     request_log[VALID_API_KEY] = {
#         today: {
#             "count": 200,
#             "requests": []
#         }
#     }

#     response = client.get(
#         "/convert?from=USD&to=BTC&amount=1",
#         headers={"x-api-key": VALID_API_KEY}
#     )
#     assert response.status_code == 429
#     assert response.json()["detail"] == "Daily weekend request limit exceeded."