- Implement assignment using:

  - Language: **Python**
  - Framework: FastAPI


  ## Features:
  - Convert between fiat and crypto currencies
  - This actually should work on any coinbase coins but was only tested for EUR/USD/BTC/ETH
  - Exchange rates are source from the coinbase api
  - We cache prices for 5 minutes
  - Rate limits are per API key:
  - **100 requests/day** on weekdays
  - **200 requests/day** on weekends

  - Logs each request with timestamp, params, and response
  - Includes a full test suite (unit + integration)

To Run APP

Create Virtual Environment
-python3 -m venv venv
-source venv/bin/activate

Install dependencies
-pip install -r requirements.txt

Run the Server with:
uvicorn app.main:app --reload

Use the API KEY HEADER with one of the valid api keys:
test-api-key-1
test-api-key-2
test-api-key-3

API ENDPOINT: GET /convert

PARAMS:
from:string 
to:string
amount:float
x-api-key:string

EXAMPLE:

curl -X GET "http://127.0.0.1:8000/convert?from=USD&to=BTC&amount=1" \
     -H "x-api-key: test-api-key-1"

SAMPLE RESPONSE:
{"source_currency":"USD","final_currency":"BTC","amount":"1","converted_amount":"0.0000105600328628","exchange_rate":"0.0000105600328628"}%   

{
  "source_currency": "USD",
  "final_currency": "BTC",
  "amount": 1.0,
  "converted_amount": 0.0000105,
  "exchange_rate": 0.0000105
}