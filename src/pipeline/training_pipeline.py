import sys

from src.exception import MyException
from src.logger import logger

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation

from src.entity.config_entity import (DataIngestionConfig,
                                      DataValidationConfig)

from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataValidationArtifact)

class TrainingPipeline:
    
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        
        try:
            logger.info("Entered the start_data_ingestion method of TrainPipeline class")
            logger.info("Getting the Data from MongoDB")
            
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            logger.info("Got the train_set and test_set from MongoDB")
            logger.info("Exited the start_data_ingestion method of TrainPipeline class")
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e) from e

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logger.info("[Training Pipeline] Enter the start_data_validation method of TrainingPipeline class")
        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            
            data_validation_artifact = data_validation.initiate_data_validation()
            
            logger.info("Performed the data validation operation")
            logger.info("Exited the start_data_validation method of TrainingPipeline class")
            
            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e) from e

    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            
        except Exception as e:
            raise MyException(e) from e