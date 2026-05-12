import aiohttp
import asyncio
import logging
from typing import List, Dict, Any

class DataExtractor:
    def __init__(self) -> None:
        self.base_url = "http://example.com/api/data"
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10, connect=30),
            headers={"User-Agent": "ETL-Agent/5.0"},
        )
        self.max_retries = 3
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    async def extract(self) -> List[Dict[str, Any]]:
        results = []
        for attempt in range(self.max_retries):
            try:
                async with self.session.get(self.base_url) as response:
                    if response.status == 429:
                        self.logger.warning("Received HTTP 429, backing off for 60 seconds.")
                        await asyncio.sleep(60)
                        continue
                    response.raise_for_status()
                    data = await response.json()
                    results.extend(data)  # Assuming data is a list of dicts
                    break
            except aiohttp.ClientError as e:
                self.logger.error(f"Client error: {e}, attempt {attempt + 1}")
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}, attempt {attempt + 1}")
                await asyncio.sleep(2 ** attempt)
        return results

    async def close(self) -> None:
        await self.session.close()