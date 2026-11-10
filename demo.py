from Valuelens_AI.components.data_ingestion import DataIngestion
from Valuelens_AI.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

training_pipeline_config = TrainingPipelineConfig()
data_ingestion_config = DataIngestionConfig(training_pipeline_config)

artifact = DataIngestion(data_ingestion_config).initiate_data_ingestion()
print(artifact)