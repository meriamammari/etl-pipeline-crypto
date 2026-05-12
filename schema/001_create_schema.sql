CREATE SCHEMA IF NOT EXISTS manual;

CREATE TABLE IF NOT EXISTS manual.crypto_market_snapshot (
    coin_id                             TEXT PRIMARY KEY NOT NULL,
    symbol                              TEXT NOT NULL,
    name                                TEXT,
    image_url                           TEXT,
    market_cap_rank                     INTEGER,
    price_usd                           NUMERIC,
    price_eur                           NUMERIC,
    price_gbp                           NUMERIC,
    price_jpy                           NUMERIC,
    price_chf                           NUMERIC,
    price_cad                           NUMERIC,
    market_cap_usd                      NUMERIC,
    fully_diluted_valuation_usd         NUMERIC,
    mcap_fdv_ratio                      NUMERIC,
    volume_24h_usd                      NUMERIC,
    high_24h_usd                        NUMERIC,
    low_24h_usd                         NUMERIC,
    change_24h_abs                      NUMERIC,
    change_24h_pct                      NUMERIC,
    change_7d_pct                       NUMERIC,
    mcap_change_24h_abs                 NUMERIC,
    primary_category                     TEXT
);

CREATE TABLE IF NOT EXISTS manual.pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pipeline_runs_status ON manual.pipeline_runs(status);
CREATE INDEX idx_pipeline_runs_start_time ON manual.pipeline_runs(start_time);
CREATE INDEX idx_pipeline_runs_end_time ON manual.pipeline_runs(end_time);