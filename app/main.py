from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import conversion
from app.services import refresh_rates_on_start

@asynccontextmanager
async def lifespan(app: FastAPI):
    refresh_rates_on_start()
    yield 

app = FastAPI(
    title= "Currency conversion service that includes FIAT and cryptocurrencies",
    description="A service that makes conversions between USD, EUR,BTC, ETH with authentication.",
    lifespan=lifespan
)

app.include_router(conversion.router)

@app.get("/")
async def root():
    return {"message": "Currency Conversion Service is running"}

