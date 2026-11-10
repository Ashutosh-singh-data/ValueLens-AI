import os
from Valuelens_AI.constants import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    history_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, HISTORY_FILE_NAME)
    future_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, FUTURE_FILE_NAME)
    cutoff_date: str = CUTOFF_DATE
    prediction_window_months: int = PREDICTION_WINDOW_MONTHS
    collection_name: str = DATA_INGESTION_COLLECTION_NAME