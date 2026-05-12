import asyncio
import logging
import json
from typing import Any, Dict, List
from sqlalchemy import create_engine, Column, Integer, String, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StagingData(Base):
    __tablename__ = 'staging_data'
    id = Column(Integer, primary_key=True)
    data = Column(JSONB)

async def extract_data(source: str) -> List[Dict[str, Any]]:
    logger.info(f"Starting extraction from {source}")
    # Simulate data extraction
    await asyncio.sleep(1)
    return [{"field1": "value1", "field2": "value2"}]

async def ingest_data(source: str) -> None:
    try:
        data = await extract_data(source)
        logger.info(f"Data extracted from {source}: {data}")
        await clean_and_normalize(data)
    except Exception as e:
        logger.error(f"Error during ingestion from {source}: {e}")

async def clean_and_normalize(List[Dict[str, Any]]) -> None:
    cleaned_data = []
    for record in data:
        cleaned_record = {k: v if v is not None else "default_value" for k, v in record.items()}
        cleaned_data.append(cleaned_record)
    await load_to_staging(cleaned_data)

async def load_to_staging(List[Dict[str, Any]]) -> None:
    session = Session()
    try:
        for record in data:
            staging_record = StagingData(data=json.dumps(record))
            session.add(staging_record)
        session.commit()
        logger.info("Data loaded to staging successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Error loading data to staging: {e}")
    finally:
        session.close()

async def main(sources: List[str]) -> None:
    tasks = [ingest_data(source) for source in sources]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    sources = ["source1", "source2", "source3"]
    asyncio.run(main(sources))