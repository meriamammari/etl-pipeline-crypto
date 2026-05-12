import pytest
import httpx
from unittest.mock import patch
from your_etl_module import Loader  # Adjust the import based on your actual module structure

@pytest.mark.asyncio
async def test_loader_happy_path():
    async with httpx.AsyncClient() as client:
        with patch('httpx.AsyncClient.get', return_value=httpx.Response(200, json=[
            {
                "id": "bitcoin",
                "symbol": "BTC",
                "name": "Bitcoin",
                "image": "https://example.com/bitcoin.png",
                "current_price": 50000,
                "market_cap": 900000000000,
                "market_cap_rank": 1,
                "fully_diluted_valuation": 1000000000000,
                "total_volume": 30000000000,
                "high_24h": 51000
            }
        ])):
            loader = Loader()
            await loader.load_data()
            # Add assertions to verify data in the database

@pytest.mark.asyncio
async def test_loader_null_values():
    async with httpx.AsyncClient() as client:
        with patch('httpx.AsyncClient.get', return_value=httpx.Response(200, json=[
            {
                "id": "bitcoin",
                "symbol": "BTC",
                "name": None,
                "image": None,
                "current_price": 50000,
                "market_cap": 900000000000,
                "market_cap_rank": 1,
                "fully_diluted_valuation": 1000000000000,
                "total_volume": 30000000000,
                "high_24h": 51000
            }
        ])):
            loader = Loader()
            await loader.load_data()
            # Add assertions to verify handling of null values in the database

@pytest.mark.asyncio
async def test_loader_rate_limit():
    async with httpx.AsyncClient() as client:
        with patch('httpx.AsyncClient.get', side_effect=httpx.HTTPStatusError("Rate limit exceeded", request=httpx.Request('GET', 'https://api.coingecko.com/api/v3/coins/markets'))):
            loader = Loader()
            with pytest.raises(httpx.HTTPStatusError):
                await loader.load_data()

@pytest.mark.asyncio
async def test_loader_empty_response():
    async with httpx.AsyncClient() as client:
        with patch('httpx.AsyncClient.get', return_value=httpx.Response(200, json=[])):
            loader = Loader()
            await loader.load_data()
            # Add assertions to verify that no data is inserted into the database

@pytest.mark.asyncio
async def test_loader_business_rule_sentiment_label():
    async with httpx.AsyncClient() as client:
        with patch('httpx.AsyncClient.get', return_value=httpx.Response(200, json=[
            {
                "id": "bitcoin",
                "symbol": "BTC",
                "name": "Bitcoin",
                "image": "https://example.com/bitcoin.png",
                "current_price": 50000,
                "market_cap": 900000000000,
                "market_cap_rank": 1,
                "fully_diluted_valuation": 1000000000000,
                "total_volume": 30000000000,
                "high_24h": 51000,
                "change_24h_pct": 6.0
            }
        ])):
            loader = Loader()
            await loader.load_data()
            # Add assertions to verify sentiment_label is set to 'Strongly Bullish'

@pytest.mark.asyncio
async def test_loader_business_rule_market_cap_category():
    async with httpx.AsyncClient() as client:
        with patch('httpx.AsyncClient.get', return_value=httpx.Response(200, json=[
            {
                "id": "bitcoin",
                "symbol": "BTC",
                "name": "Bitcoin",
                "image": "https://example.com/bitcoin.png",
                "current_price": 50000,
                "market_cap": 900000000000,
                "market_cap_rank": 1,
                "fully_diluted_valuation": 1000000000000,
                "total_volume": 30000000000,
                "high_24h": 51000
            }
        ])):
            loader = Loader()
            await loader.load_data()
            # Add assertions to verify market_cap_category is set to 'Mega Cap'