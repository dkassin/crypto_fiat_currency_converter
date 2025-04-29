import pytest
from app.prices import set_prices, get_prices

def test_set_and_get_prices():
    fake_rates = {"BTC": "0.000015", "ETH": "0.00025", "EUR": "0.89"}
    set_prices("USD", fake_rates)

    prices = get_prices("USD")
    assert prices is not None
    assert prices["BTC"] == "0.000015"
    assert prices["ETH"] == "0.00025"
    assert prices["EUR"] == "0.89"

