import os
import sys

import pandas as pd
from pandas import DataFrame

from Valuelens_AI.constants import DATE_COLUMN
from Valuelens_AI.data_access.online_retail_data import valuelensData
from Valuelens_AI.entity.artifact_entity import DataIngestionArtifact
from Valuelens_AI.entity.config_entity import DataIngestionConfig
from Valuelens_AI.exception import valuelensException
from Valuelens_AI.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        :param data_ingestion_config: configuration for the data ingestion stage
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise valuelensException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Reads the full collection from MongoDB, fixes the date column
        and saves it as the feature store file.
        """
        try:
            logging.info("Exporting data from MongoDB")
            data = valuelensData()
            dataframe = data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"Shape of dataframe: {dataframe.shape}")

            # Dates can come back as text, so make sure they are real dates
            dataframe[DATE_COLUMN] = pd.to_datetime(dataframe[DATE_COLUMN])

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            logging.info(f"Saving feature store file: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise valuelensException(e, sys)

    def split_data_by_cutoff(self, dataframe: DataFrame) -> None:
        """
        Splits the data by date, not randomly:
        history = rows before the cutoff
        future  = rows from the cutoff to the end of the prediction window
        """
        logging.info("Entered split_data_by_cutoff method of DataIngestion class")
        try:
            cutoff = pd.Timestamp(self.data_ingestion_config.cutoff_date)
            window_end = cutoff + pd.DateOffset(
                months=self.data_ingestion_config.prediction_window_months
            )

            history = dataframe[dataframe[DATE_COLUMN] < cutoff]
            future = dataframe[
                (dataframe[DATE_COLUMN] >= cutoff) & (dataframe[DATE_COLUMN] < window_end)
            ]

            logging.info(f"Cutoff: {cutoff.date()} | Window end: {window_end.date()}")
            logging.info(f"History rows: {len(history)} | Future rows: {len(future)}")

            if history.empty or future.empty:
                raise Exception("History or future data is empty. Check the cutoff date.")

            os.makedirs(
                os.path.dirname(self.data_ingestion_config.history_file_path), exist_ok=True
            )
            history.to_csv(self.data_ingestion_config.history_file_path, index=False, header=True)
            future.to_csv(self.data_ingestion_config.future_file_path, index=False, header=True)

            logging.info("Exported history and future files")
        except Exception as e:
            raise valuelensException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Runs the full ingestion stage and returns the artifact for the next stage.
        """
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from MongoDB")

            self.split_data_by_cutoff(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                history_file_path=self.data_ingestion_config.history_file_path,
                future_file_path=self.data_ingestion_config.future_file_path,
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            logging.info("Exited initiate_data_ingestion method of DataIngestion class")
            return data_ingestion_artifact
        except Exception as e:
            raise valuelensException(e, sys) from e