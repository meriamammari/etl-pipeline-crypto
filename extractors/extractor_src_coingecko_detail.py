import httpx
import asyncio
import logging
from typing import List, Dict, Any
from httpx import HTTPStatusError

class AuthenticationError(Exception):
    pass

class SrcCoingeckoDetailExtractor:
    BASE_URL = "https://api.coingecko.com/api/v3/coins/{coin_id}"
    
    def __init__(self, coin_ids: List[str]):
        self.coin_ids = coin_ids
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def fetch_coin_data(self, client: httpx.AsyncClient, coin_id: str) -> Dict[str, Any]:
        url = self.BASE_URL.format(coin_id=coin_id)
        for attempt in range(3):
            try:
                self.logger.info(f"Fetching data for coin_id: {coin_id}")
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except HTTPStatusError as e:
                if e.response.status_code == 429:
                    self.logger.warning("Rate limit exceeded, waiting for 60 seconds before retrying...")
                    await asyncio.sleep(60)
                elif e.response.status_code in {401, 403}:
                    raise AuthenticationError("Authentication failed, check your credentials.")
                else:
                    self.logger.error(f"HTTP error occurred: {e}")
                    break
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                break
        return {}

    async def extract(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_coin_data(client, coin_id) for coin_id in self.coin_ids]
            results = await asyncio.gather(*tasks)
        return [result for result in results if result]