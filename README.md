# ETL Pipeline README

## Overview
The ETL Pipeline is designed to extract, transform, and load data into the `public.target_data` table. This pipeline is scheduled to run at regular intervals to ensure that the target data is always up-to-date.

## Architecture
The ETL Pipeline consists of three main components:
1. **Extraction**: Data is extracted from various sources (currently none specified).
2. **Transformation**: Data is transformed as per business rules (currently none specified).
3. **Loading**: The transformed data is loaded into the `public.target_data` table.

A high-level architecture diagram can be found in the documentation folder.

## Installation
To install the ETL Pipeline, follow these steps:
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/etl-pipeline.git
   ```
2. Navigate to the project directory:
   ```
   cd etl-pipeline
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
Configuration settings can be found in the `config.yaml` file. Update the following parameters as needed:
- Database connection details
- Logging settings

## Run
To run the ETL Pipeline, execute the following command:
```
python main.py
```
The pipeline is scheduled to run every day at midnight using a cron job:
```
0 0 * * * /usr/bin/python3 /path/to/your/etl-pipeline/main.py
```

## Testing
To run the tests for the ETL Pipeline, use the following command:
```
pytest tests/
```
Ensure that all tests pass before deploying the pipeline to production.

## API Sources
Currently, there are no specified API sources for data extraction. Future implementations may include various APIs as data sources.

## Troubleshooting
If you encounter issues while running the ETL Pipeline, consider the following steps:
1. Check the logs located in the `logs/` directory for any error messages.
2. Ensure that the database connection details in `config.yaml` are correct.
3. Verify that the necessary permissions are granted for the database user.

For further assistance, refer to the user guide or contact the development team.