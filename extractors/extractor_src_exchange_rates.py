import httpx
import asyncio
import logging
from typing import List, Dict

class AuthenticationError(Exception):
    pass

class SrcExchangeRatesExtractor:
    def __init__(self) -> None:
        self.url = "https://open.er-api.com/v6/latest/USD"
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            for attempt in range(self.max_retries):
                try:
                    self.logger.info("Fetching data from %s (attempt %d)", self.url, attempt + 1)
                    resp = await client.get(
                        self.url,
                        params={},
                        headers={"Accept": "application/json"},
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    return data.get('result', [])
                except httpx.HTTPStatusError as e:
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
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay)
                        self.retry_delay *= 2  # Exponential backoff
                    else:
                        raise
        return []  # Return an empty list if all attempts fail