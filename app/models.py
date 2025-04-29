from decimal import Decimal
from pydantic import BaseModel

# Decimal was used here instead of float, because of rounding errors that occur with float in python
class ConversionResponse(BaseModel):
    source_currency: str
    final_currency: str
    amount: Decimal
    converted_amount: Decimal
    exchange_rate: Decimal