import logging
from typing import List, Dict, Any

class Transformer:
    """Auto-generated transformer — 6 business rules, 0 derived columns."""

    def transform(self, records: List[Dict[str, Any]], rates: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        out = []
        for row in records:
            try:
                row = dict(row)
                if rates:
                    row['_rates'] = rates
                self._apply_derivations(row, rates or {})
                self._apply_business_rules(row)
                row['symbol'] = row['symbol'].upper()
                out.append(row)
            except Exception as e:
                logging.warning(f"Transform error on {row.get('id')}: {e}")
        return out

    def _apply_derivations(self, row: Dict[str, Any], rates: Dict[str, Any]):
        price = row.get('current_price') or row.get('price_usd')
        mc = row.get('market_cap') or row.get('market_cap_usd')
        fdv = row.get('fully_diluted_valuation') or row.get('fully_diluted_valuation_usd')
        vol = row.get('total_volume') or row.get('volume_24h_usd')
        circ = row.get('circulating_supply')
        maxs = row.get('max_supply')
        ath = row.get('ath') or row.get('ath_usd')
        atl = row.get('atl') or row.get('atl_usd')

        def safe_div(a: float, b: float) -> float:
            return round(a / b, 8) if a and b and b != 0 else None

        row['mcap_fdv_ratio'] = safe_div(mc, fdv)
        row['volume_to_mcap_ratio'] = safe_div(vol, mc)
        row['supply_ratio'] = safe_div(circ, maxs)
        row['ath_drawdown_pct'] = round(((price - ath) / ath) * 100, 4) if price and ath else None

    def _apply_business_rules(self, row: Dict[str, Any]):
        row['sentiment_label'] = self._br1_sentiment_label(row)
        row['market_cap_category'] = self._br2_market_cap_category(row)
        row['volatility_flag'] = self._br3_volatility_flag(row)
        row['supply_emission_stage'] = self._br4_supply_emission_stage(row)
        row['weekly_trend'] = self._br5_weekly_trend(row)

    def _br1_sentiment_label(self, row: Dict[str, Any]) -> str:
        change_pct = row.get('change_24h_pct', 0)
        if change_pct >= 5.0:
            return 'Strongly Bullish'
        elif change_pct >= 2.0:
            return 'Bullish'
        elif change_pct >= -2.0:
            return 'Neutral'
        elif change_pct >= -5.0:
            return 'Bearish'
        return 'Strongly Bearish'

    def _br2_market_cap_category(self, row: Dict[str, Any]) -> str:
        market_cap = row.get('market_cap_usd', 0)
        if market_cap >= 10000000000:
            return 'Mega Cap'
        elif market_cap >= 1000000000:
            return 'Large Cap'
        elif market_cap >= 100000000:
            return 'Mid Cap'
        elif market_cap >= 10000000:
            return 'Small Cap'
        return 'Micro Cap'

    def _br3_volatility_flag(self, row: Dict[str, Any]) -> str:
        change_pct = abs(row.get('change_24h_pct', 0))
        if change_pct >= 5.0:
            return 'High'
        elif change_pct >= 2.0:
            return 'Medium'
        return 'Low'

    def _br4_supply_emission_stage(self, row: Dict[str, Any]) -> str:
        supply_ratio = row.get('supply_ratio')
        if supply_ratio is None:
            return 'Uncapped'
        elif supply_ratio >= 0.95:
            return 'Near Full'
        elif supply_ratio >= 0.75:
            return 'Mature'
        elif supply_ratio >= 0.50:
            return 'Mid Emission'
        return 'Early Stage'

    def _br5_weekly_trend(self, row: Dict[str, Any]) -> str:
        change_24h_abs = row.get('change_24h_abs', 0)
        change_7d_pct = row.get('change_7d_pct', 0)
        if change_24h_abs > 0 and change_7d_pct > 0:
            return 'Aligned Bullish'
        return 'Not Aligned'