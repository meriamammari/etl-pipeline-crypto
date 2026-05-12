import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_sentiment_label():
    test_data = [
        {'change_24h_pct': 6.0, 'expected': 'Strongly Bullish'},
        {'change_24h_pct': 3.0, 'expected': 'Bullish'},
        {'change_24h_pct': 0.0, 'expected': 'Neutral'},
        {'change_24h_pct': -3.0, 'expected': 'Bearish'},
        {'change_24h_pct': -6.0, 'expected': 'Strongly Bearish'},
    ]
    
    for data in test_data:
        result = evaluate_sentiment_label(data['change_24h_pct'])
        assert result == data['expected']

@pytest.mark.asyncio
async def test_market_cap_category():
    test_data = [
        {'market_cap_usd': 15000000000, 'expected': 'Mega Cap'},
        {'market_cap_usd': 5000000000, 'expected': 'Large Cap'},
        {'market_cap_usd': 500000000, 'expected': 'Mid Cap'},
        {'market_cap_usd': 20000000, 'expected': 'Small Cap'},
        {'market_cap_usd': 5000000, 'expected': 'Micro Cap'},
    ]
    
    for data in test_data:
        result = evaluate_market_cap_category(data['market_cap_usd'])
        assert result == data['expected']

@pytest.mark.asyncio
async def test_volatility_flag():
    test_data = [
        {'change_24h_pct': 6.0, 'expected': 'High'},
        {'change_24h_pct': 3.0, 'expected': 'Medium'},
        {'change_24h_pct': 1.0, 'expected': 'Low'},
        {'change_24h_pct': -6.0, 'expected': 'High'},
        {'change_24h_pct': -3.0, 'expected': 'Medium'},
    ]
    
    for data in test_data:
        result = evaluate_volatility_flag(data['change_24h_pct'])
        assert result == data['expected']

@pytest.mark.asyncio
async def test_supply_emission_stage():
    test_data = [
        {'supply_ratio': None, 'expected': 'Uncapped'},
        {'supply_ratio': 0.96, 'expected': 'Near Full'},
        {'supply_ratio': 0.80, 'expected': 'Mature'},
        {'supply_ratio': 0.60, 'expected': 'Mid Emission'},
        {'supply_ratio': 0.40, 'expected': 'Early Stage'},
    ]
    
    for data in test_data:
        result = evaluate_supply_emission_stage(data['supply_ratio'])
        assert result == data['expected']

@pytest.mark.asyncio
async def test_weekly_trend():
    test_data = [
        {'change_24h_abs': 1.0, 'change_7d_pct': 1.0, 'expected': 'Aligned Bullish'},
        {'change_24h_abs': -1.0, 'change_7d_pct': 1.0, 'expected': 'Diverged Bearish'},
        {'change_24h_abs': 1.0, 'change_7d_pct': -1.0, 'expected': 'Diverged Bearish'},
        {'change_24h_abs': 0.0, 'change_7d_pct': 0.0, 'expected': 'Neutral'},
    ]
    
    for data in test_data:
        result = evaluate_weekly_trend(data['change_24h_abs'], data['change_7d_pct'])
        assert result == data['expected']

def evaluate_sentiment_label(change_24h_pct: float) -> str:
    if change_24h_pct >= 5.0:
        return 'Strongly Bullish'
    elif change_24h_pct >= 2.0:
        return 'Bullish'
    elif change_24h_pct >= -2.0:
        return 'Neutral'
    elif change_24h_pct >= -5.0:
        return 'Bearish'
    return 'Strongly Bearish'

def evaluate_market_cap_category(market_cap_usd: float) -> str:
    if market_cap_usd >= 10000000000:
        return 'Mega Cap'
    elif market_cap_usd >= 1000000000:
        return 'Large Cap'
    elif market_cap_usd >= 100000000:
        return 'Mid Cap'
    elif market_cap_usd >= 10000000:
        return 'Small Cap'
    return 'Micro Cap'

def evaluate_volatility_flag(change_24h_pct: float) -> str:
    if abs(change_24h_pct) >= 5.0:
        return 'High'
    elif abs(change_24h_pct) >= 2.0:
        return 'Medium'
    return 'Low'

def evaluate_supply_emission_stage(supply_ratio: float) -> str:
    if supply_ratio is None:
        return 'Uncapped'
    elif supply_ratio >= 0.95:
        return 'Near Full'
    elif supply_ratio >= 0.75:
        return 'Mature'
    elif supply_ratio >= 0.50:
        return 'Mid Emission'
    return 'Early Stage'

def evaluate_weekly_trend(change_24h_abs: float, change_7d_pct: float) -> str:
    if change_24h_abs > 0 and change_7d_pct > 0:
        return 'Aligned Bullish'
    return 'Diverged Bearish'