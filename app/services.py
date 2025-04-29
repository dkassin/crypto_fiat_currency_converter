import httpx
from decimal import Decimal
from datetime import datetime
from app.prices import set_prices, get_prices
import pdb

## We only need to compare everything to USD and then we can still generate conversions from that
def fetch_prices():
    url = f"https://api.coinbase.com/v2/exchange-rates?currency=USD"

    with httpx.Client() as client:
        response = client.get(url)


    if response.status_code != 200:
        raise Exception(
            f"Received status code {response.status_code}. Double Check client connection."
        )  
    
    json_response = response.json()
    rates = json_response.get("data", {}).get("rates", {})
    if not rates:
        raise Exception("No Price Data was found in response")
    
    ## Should populate the set prices hash
    set_prices("USD", rates)

def refresh_rates_on_start():
    ## This will kickoff on start and fill in our set prices hash
    fetch_prices()

def get_conversion_rate(source_currency: str, final_currency: str):
    source_currency = source_currency.upper()
    final_currency = final_currency.upper()

    prices = get_prices("USD")
    if prices is None:
        raise Exception("Currency rates not available. Please refresh rates.")

    if source_currency == "USD" and final_currency in prices:
        return Decimal(prices[final_currency])
    
    if final_currency == "USD" and source_currency in prices:
        return Decimal("1") / Decimal(prices[source_currency])
    
    if source_currency in prices and final_currency in prices:
        return Decimal(prices[final_currency]) / Decimal(prices[source_currency])
    
    raise Exception(f"Conversion path between {source_currency} and {final_currency} not found.")