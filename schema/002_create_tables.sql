CREATE TABLE IF NOT EXISTS etl_pipeline.pipeline_data (
    id SERIAL PRIMARY KEY
);

CREATE INDEX idx_pipeline_data_timestamp ON etl_pipeline.pipeline_data (timestamp);
CREATE INDEX idx_pipeline_data_id ON etl_pipeline.pipeline_data (id);
CREATE INDEX idx_pipeline_data_category ON etl_pipeline.pipeline_data (category);