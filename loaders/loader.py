import os
import psycopg2
import psycopg2.extras
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoMarketSnapshotLoader:
    def __init__(self, rows: List[Dict[str, Any]]):
        self.rows = rows

    def load(self) -> None:
        try:
            conn = psycopg2.connect(
                host=os.environ["DB_HOST"],
                port=os.environ.get("DB_PORT", "5432"),
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
            conn.autocommit = False
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE manual.crypto_market_snapshot")
                psycopg2.extras.execute_batch(
                    cur,
                    """
                    INSERT INTO manual.crypto_market_snapshot (
                        coin_id, symbol, name, image_url, market_cap_rank, 
                        price_usd, price_eur, price_gbp, price_jpy, price_chf, 
                        price_cad, market_cap_usd, fully_diluted_valuation_usd, 
                        mcap_fdv_ratio, volume_24h_usd, high_24h_usd, 
                        low_24h_usd, change_24h_abs, change_24h_pct, 
                        change_7d_pct, mcap_change_24h_abs, primary_category
                    ) VALUES %s
                    """,
                    self.rows,
                    page_size=100,
                )
            conn.commit()
            logger.info(f"Loaded {len(self.rows)} rows into manual.crypto_market_snapshot")
            self.audit_load(len(self.rows))
        except Exception as e:
            logger.error(f"Error loading {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def audit_load(self, rows_loaded: int) -> None:
        try:
            conn = psycopg2.connect(
                host=os.environ["DB_HOST"],
                port=os.environ.get("DB_PORT", "5432"),
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO manual.pipeline_runs (rows_loaded, run_time)
                    VALUES (%s, NOW())
                    """,
                    (rows_loaded,)
                )
            conn.commit()
        except Exception as e:
            logger.error(f"Error writing audit record: {e}")
            conn.rollback()
        finally:
            conn.close()