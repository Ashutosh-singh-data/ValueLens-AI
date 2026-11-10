import os
from datetime import date

DATABASE_NAME = "Valuelens-AI" #any name

COLLECTION_NAME = "Online-Retail-data" #any name

MONGODB_URL_KEY ="MONGODB_URL"

PIPELINE_NAME: str = "valuelens"
ARTIFACT_DIR: str = "artifact"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

MODEL_FILE_NAME = "model.pkl"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "Online-Retail-data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"

# Data columns
DATE_COLUMN: str = "InvoiceDate"

# Files
FILE_NAME: str = "online_retail_II.csv"
HISTORY_FILE_NAME: str = "history.csv"
FUTURE_FILE_NAME: str = "future.csv"


# Time-based split
CUTOFF_DATE: str = "2011-06-01"
PREDICTION_WINDOW_MONTHS: int = 6