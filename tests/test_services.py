import pytest
from app.services import fetch_prices, get_conversion_rate
from app.prices import set_prices, get_prices

def test_fetch_prices():
    fetch_prices()
    prices = get_prices("USD")
    assert prices is not None
    assert "BTC" in prices
    assert "ETH" in prices
    assert "EUR" in prices


def test_get_conversion_rate_usd_to_btc():
    set_prices("USD", {
        "BTC": "0.000015",
        "ETH": "0.00025",
        "EUR": "0.89"
    })
    rate = get_conversion_rate("USD", "BTC")
    assert round(float(rate), 8) == 0.000015

def test_get_conversion_rate_btc_to_usd():
    rate = get_conversion_rate("BTC", "USD")
    assert round(float(rate), 2) == 66666.67

def test_get_conversion_rate_btc_to_eth():
    rate = get_conversion_rate("BTC", "ETH")
    assert round(float(rate), 2) == 16.67


