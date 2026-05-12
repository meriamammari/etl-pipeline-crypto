import pytest
import httpx
from unittest.mock import patch
from extractors import CoinGeckoExtractor, ExchangeRatesExtractor

@pytest.mark.asyncio
async def test_coingecko_extractor_happy_path():
    mock_response = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "image": "https://example.com/bitcoin.png",
            "current_price": 50000,
            "market_cap": 900000000000,
            "market_cap_rank": 1,
            "fully_diluted_valuation": 1000000000000,
            "total_volume": 30000000000,
            "high_24h": 51000
        }
    ]
    
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: (200, request, mock_response))) as client:
        extractor = CoinGeckoExtractor(client)
        data = await extractor.extract()
        assert data[0]['coin_id'] == 'bitcoin'
        assert data[0]['symbol'] == 'btc'
        assert data[0]['name'] == 'Bitcoin'
        assert data[0]['image_url'] == 'https://example.com/bitcoin.png'
        assert data[0]['market_cap_rank'] == 1

@pytest.mark.asyncio
async def test_coingecko_extractor_empty_response():
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: (200, request, []))) as client:
        extractor = CoinGeckoExtractor(client)
        data = await extractor.extract()
        assert data == []

@pytest.mark.asyncio
async def test_coingecko_extractor_null_values():
    mock_response = [
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": None,
            "image": None,
            "current_price": 4000,
            "market_cap": 500000000000,
            "market_cap_rank": 2,
            "fully_diluted_valuation": None,
            "total_volume": 20000000000,
            "high_24h": 4100
        }
    ]
    
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: (200, request, mock_response))) as client:
        extractor = CoinGeckoExtractor(client)
        data = await extractor.extract()
        assert data[0]['name'] is None
        assert data[0]['image_url'] is None

@pytest.mark.asyncio
async def test_exchange_rates_extractor_happy_path():
    mock_response = {
        "result": "success",
        "provider": "Open Exchange Rates",
        "documentation": "https://open.er-api.com",
        "terms_of_use": "https://open.er-api.com/terms",
        "time_last_update_unix": 1633072800,
        "time_last_update_utc": "2021-10-01T00:00:00Z",
        "base_code": "USD"
    }
    
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: (200, request, mock_response))) as client:
        extractor = ExchangeRatesExtractor(client)
        data = await extractor.extract()
        assert data['result'] == 'success'
        assert data['base_code'] == 'USD'

@pytest.mark.asyncio
async def test_exchange_rates_extractor_empty_response():
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: (200, request, {}))) as client:
        extractor = ExchangeRatesExtractor(client)
        data = await extractor.extract()
        assert data == {}

@pytest.mark.asyncio
async def test_exchange_rates_extractor_rate_limit():
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: (429, request, {}))) as client:
        extractor = ExchangeRatesExtractor(client)
        with pytest.raises(httpx.HTTPStatusError):
            await extractor.extract()