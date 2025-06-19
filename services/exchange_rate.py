from datetime import datetime
from functools import lru_cache
from typing import Dict

import httpx
from fastapi import APIRouter, HTTPException
from cachetools import TTLCache

from core.config import settings
from enums.currency import Currency

router = APIRouter(
    prefix="/exchangerates",
    tags=["Exchange Rates"]
)

API_KEY = settings.API_KEY
api_url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
cache = TTLCache(maxsize=1, ttl=120) #store the conversion rates for 2 minutes

@router.get('/')
async def get_latest_exchange_rate() -> Dict[str, float]:
    if "rates" in cache:
        return cache["rates"]
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch rates")
            data = response.json()
            cache["rates"] = data["conversion_rates"]
            print("calling the api")
            return data["conversion_rates"]
    except httpx.ConnectTimeout:
        raise HTTPException(status_code=504, detail="Exchange rate API timed out")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")

async def old_exchange_rate(curr: Currency, date: datetime) -> float:
    print(curr.title().upper())
    formatted_date = date.strftime("%Y-%m-%d")
    print(formatted_date)
    url = f"https://api.exchangerate.host/convert?access_key=d7c856d3b53a4a1eb455d057ad1a2024&from=USD&to={curr.title().upper()}&amount=1&date={formatted_date}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch exchange rate")

            data = response.json()
            print(data)
            # Ensure result exists
            if "result" not in data or data["result"] is None:
                raise HTTPException(status_code=500, detail="Invalid response from exchange API")

            return data["result"]

    except httpx.ConnectTimeout:
        raise HTTPException(status_code=504, detail="Exchange rate API timed out")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Exchange API error: {str(e)}")
