import asyncio
import logging
import os
import time
from typing import List, Dict, Any, Optional

class Orchestrator:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def extract(self) -> List[Dict[str, Any]]:
        self.logger.info("Starting extraction phase")
        start_time = time.time()
        try:
            coingecko_markets = await self.fetch_coingecko_markets()
            exchange_rates = await self.fetch_exchange_rates()
            self.logger.info("Extraction completed successfully")
            return coingecko_markets, exchange_rates
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            raise
        finally:
            duration = time.time() - start_time
            self.logger.info(f"Extraction phase duration: {duration:.2f} seconds")

    async def fetch_coingecko_markets(self) -> List[Dict[str, Any]]:
        # Simulated async API call
        return await asyncio.sleep(1, result=[{"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin", "image": "url", "current_price": 50000, "market_cap": 900000000000, "market_cap_rank": 1, "fully_diluted_valuation": 1000000000000, "total_volume": 30000000000, "high_24h": 51000}])

    async def fetch_exchange_rates(self) -> Dict[str, Any]:
        # Simulated async API call
        return await asyncio.sleep(1, result={"result": {"EUR": 0.85, "GBP": 0.75}})

    async def join(self, markets: List[Dict[str, Any]], exchange_rates: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.logger.info("Starting join phase")
        start_time = time.time()
        try:
            enriched_data = self.cross_join(markets, exchange_rates)
            self.logger.info("Join completed successfully")
            return enriched_data
        except Exception as e:
            self.logger.error(f"Join failed: {e}")
            raise
        finally:
            duration = time.time() - start_time
            self.logger.info(f"Join phase duration: {duration:.2f} seconds")

    def cross_join(self, markets: List[Dict[str, Any]], exchange_rates: Dict[str, Any]) -> List[Dict[str, Any]]:
        for market in markets:
            market.update(exchange_rates['result'])
        return markets

    async def transform(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.logger.info("Starting transform phase")
        start_time = time.time()
        try:
            transformed_rows = self.apply_business_rules(rows)
            self.logger.info("Transform completed successfully")
            return transformed_rows
        except Exception as e:
            self.logger.error(f"Transform failed: {e}")
            raise
        finally:
            duration = time.time() - start_time
            self.logger.info(f"Transform phase duration: {duration:.2f} seconds")

    def apply_business_rules(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for row in rows:
            row['sentiment_label'] = self.get_sentiment_label(row['change_24h_pct'])
            row['market_cap_category'] = self.get_market_cap_category(row['market_cap_usd'])
        return rows

    def get_sentiment_label(self, change_24h_pct: float) -> str:
        if change_24h_pct >= 5.0:
            return 'Strongly Bullish'
        elif change_24h_pct >= 2.0:
            return 'Bullish'
        elif change_24h_pct >= -2.0:
            return 'Neutral'
        elif change_24h_pct >= -5.0:
            return 'Bearish'
        return 'Strongly Bearish'

    def get_market_cap_category(self, market_cap_usd: float) -> str:
        if market_cap_usd >= 10000000000:
            return 'Mega Cap'
        elif market_cap_usd >= 1000000000:
            return 'Large Cap'
        elif market_cap_usd >= 100000000:
            return 'Mid Cap'
        elif market_cap_usd >= 10000000:
            return 'Small Cap'
        return 'Micro Cap'

    async def load(self, transformed_rows: List[Dict[str, Any]]) -> None:
        self.logger.info("Starting load phase")
        start_time = time.time()
        try:
            await self.truncate_and_insert(transformed_rows)
            self.logger.info("Load completed successfully")
        except Exception as e:
            self.logger.error(f"Load failed: {e}")
            raise
        finally:
            duration = time.time() - start_time
            self.logger.info(f"Load phase duration: {duration:.2f} seconds")

    async def truncate_and_insert(self, rows: List[Dict[str, Any]]) -> None:
        # Simulated database operation
        await asyncio.sleep(1)

    async def run(self) -> None:
        markets, exchange_rates = await self.extract()
        enriched_data = await self.join(markets, exchange_rates)
        transformed_rows = await self.transform(enriched_data)
        await self.load(transformed_rows)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.run())