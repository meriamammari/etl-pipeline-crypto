# POC-CRYPTO-001 ETL Pipeline Documentation

## Architecture Overview
The POC-CRYPTO-001 ETL pipeline is designed to extract cryptocurrency market data from the CoinGecko API and exchange rate data from the Open Exchange Rates API. The pipeline processes this data and loads it into a PostgreSQL database, specifically the `manual.crypto_market_snapshot` table. The architecture consists of the following components:

1. **Data Sources**:
   - **CoinGecko Markets API**: Provides real-time market data for various cryptocurrencies.
   - **Exchange Rates API**: Supplies the latest exchange rates for USD against other currencies.

2. **Data Processing**:
   - The pipeline extracts data from the APIs, applies business rules for categorization, and transforms the data as necessary.

3. **Data Loading**:
   - The processed data is loaded into the target PostgreSQL database using a truncate and insert strategy.

## Setup Instructions
To set up the ETL pipeline, follow these steps:

1. **Install Required Packages**:
   Ensure you have Python 3.7 or higher installed. Then, install the required packages using pip:
   ```
   pip install requests psycopg2-binary python-dotenv
   ```

2. **Environment Configuration**:
   Create a `.env` file in the root directory of the project and add the following environment variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/your_database
   ```

   Replace `username`, `password`, and `your_database` with your PostgreSQL credentials and database name.

## How to Run the Pipeline
To execute the ETL pipeline, run the following command in your terminal:
```
python etl_pipeline.py
```
Ensure that your PostgreSQL database is running and accessible.

## Table Schema Summary
The target table `manual.crypto_market_snapshot` has the following schema:

| Column Name                     | Data Type |
|---------------------------------|-----------|
| coin_id                         | TEXT      |
| symbol                          | TEXT      |
| name                            | TEXT      |
| image_url                       | TEXT      |
| market_cap_rank                 | INTEGER   |
| price_usd                       | NUMERIC   |
| price_eur                       | NUMERIC   |
| price_gbp                       | NUMERIC   |
| price_jpy                       | NUMERIC   |
| price_chf                       | NUMERIC   |
| price_cad                       | NUMERIC   |
| market_cap_usd                  | NUMERIC   |
| fully_diluted_valuation_usd     | NUMERIC   |
| mcap_fdv_ratio                  | NUMERIC   |
| volume_24h_usd                  | NUMERIC   |
| high_24h_usd                    | NUMERIC   |
| low_24h_usd                     | NUMERIC   |
| change_24h_abs                  | NUMERIC   |
| change_24h_pct                  | NUMERIC   |
| change_7d_pct                   | NUMERIC   |
| sentiment_label                 | TEXT      |
| market_cap_category             | TEXT      |

The pipeline applies the following business rules during data processing:
1. **Sentiment Label**: Categorizes sentiment based on the 24-hour price change percentage.
2. **Market Cap Category**: Categorizes market cap based on the market cap in USD.

This documentation provides a comprehensive overview of the POC-CRYPTO-001 ETL pipeline, including its architecture, setup instructions, execution steps, and table schema.