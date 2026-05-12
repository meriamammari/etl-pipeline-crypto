import httpx
import asyncio
import logging
from typing import List, Dict
from httpx import HTTPStatusError

class AuthenticationError(Exception):
    pass

class SrcCoingeckoMarketsExtractor:
    def __init__(self) -> None:
        self.url = "https://api.coingecko.com/api/v3/coins/markets"
        self.params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "24h,7d"
        }
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self) -> List[Dict]:
        retries = 3
        for attempt in range(retries):
            async with httpx.AsyncClient() as client:
                try:
                    self.logger.info("Sending request to %s with params %s", self.url, self.params)
                    resp = await client.get(self.url, params=self.params, headers={"Accept": "application/json"})
                    resp.raise_for_status()
                    data = resp.json()
                    self.logger.info("Received response with %d records", len(data))
                    return data
                except HTTPStatusError as e:
                    if e.response.status_code in {401, 403}:
                        raise AuthenticationError("Authentication failed") from e
                    elif e.response.status_code == 429:
                        self.logger.warning("Rate limit exceeded, waiting for 60 seconds before retrying...")
                        await asyncio.sleep(60)
                    else:
                        self.logger.error("HTTP error occurred: %s", e)
                        raise
                except Exception as e:
                    self.logger.error("An error occurred: %s", e)
                    if attempt < retries - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise
        return []  # Return an empty list if all attempts fail