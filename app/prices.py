from datetime import datetime, timezone
import pdb

prices_dict = {}

def set_prices(base_currency: str, rates: str):
    prices_dict[base_currency] = {
        "rates": rates,
        "timestamp": datetime.now(timezone.utc)
    }


def get_prices(base_currency: str):
    from app.services import fetch_prices
    prices = prices_dict.get(base_currency)
    if not prices:
        raise Exception('Prices Dictionary Did Not Return')

    if (datetime.now(timezone.utc) - prices["timestamp"]).seconds > 300:
        ## This refreshes prices if they are older the 5 minutes
        fetch_prices()
        prices = prices_dict.get(base_currency)
        if not prices:
            raise Exception('Failed to refresh prices')
    
    return prices["rates"]