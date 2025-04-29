from fastapi import APIRouter, HTTPException, Query, Header, Depends
from decimal import Decimal
from app.models import ConversionResponse
from app.services import get_conversion_rate, refresh_rates_on_start
from app.request_tracker import log_request, get_request_count
from datetime import datetime, timezone
import pdb

router = APIRouter()

VALID_API_KEYS = {
    "test-api-key-1": "User One",
    "test-api-key-2": "User Two",
    "test-api-key-3": "User Three",
}

@router.get("/convert", response_model=ConversionResponse)
def convert_currency(
    source_currency: str = Query(..., alias="from"),
    final_currency: str = Query(..., alias="to"),
    amount: Decimal = Query(...),
    user_api_key: str = Header(..., alias="x-api-key"),
):
    # Validate API KEY
    if user_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # Determine date for rate limit
    today = datetime.now(timezone.utc)
    weekday = today.weekday()

    request_count = get_request_count(user_api_key)

    if weekday < 5 and request_count >= 100:
        raise HTTPException(status_code=429, detail="Daily weekday request limit exceeded.")
    if weekday >= 5 and request_count >= 200:
        raise HTTPException(status_code=429, detail="Daily weekend request limit exceeded.")

    # This was added for testing to pass but it jump starts a new prices cache 
    try:
        rate = get_conversion_rate(source_currency, final_currency)
    except Exception:
        try:
            refresh_rates_on_start()
            rate = get_conversion_rate(source_currency, final_currency)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Unable to perform currency conversion after refreshing rates."
            )
    
    converted_amount = amount * rate
    response_body = {
        "source_currency": source_currency.upper(),
        "final_currency": final_currency.upper(),
        "amount": amount,
        "converted_amount": converted_amount,
        "exchange_rate": rate
    }

    log_request(
        api_key = user_api_key,
        params={
            "from": source_currency,
            "to": final_currency,
            "amount": str(amount),
        },
        response_body=response_body
        )
    return response_body