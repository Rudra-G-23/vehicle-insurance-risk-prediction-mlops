import os
import sys
import json

import pandas as pd
from pandas import DataFrame

from src.exception import MyException
from src.logger import logger

from src.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from src.entity.config_entity import DataValidationConfig

from src.constants.constants import SCHEMA_FILE_PATH
from src.utils.main_utils import read_yaml_file

class DataValidation:
    
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
        ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e) from e
        
    def validate_number_of_columns(self, df: DataFrame) -> bool:
        try:
            status = len(df.columns) == len(self._schema_config["columns"])
            logger.info(f"Is required columns present: [{status}]")
            
            return status
        
        except Exception as e:
            raise MyException(e) from e

    def is_columns_exist(self, df: DataFrame) -> bool:
        try:
            df_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            
            if len(missing_numerical_columns) > 0:
                logger.info(f"Missing numerical columns: {missing_numerical_columns}")
                
            for column in self._schema_config["categorical_columns"]:
                if column not in df_columns:
                    missing_categorical_columns.append(column)
            
            if len(missing_categorical_columns) > 0:
                logger.info(f"Missing categorical column: {missing_categorical_columns}")
            
            return False if len(missing_categorical_columns) > 0 or len(missing_numerical_columns) > 0 else True
        except Exception as e:
            raise MyException(e) from e
    
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e) from e
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_msg = ""
            logger.info("Starting data Validation")
            
            train_df, test_df = (
                DataValidation.read_data(file_path=self.data_ingestion_artifact.train_file_path),
                DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            )
            
            # Validate no of columns in train df
            status = self.validate_number_of_columns(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training df."
            else:
                logger.info(f"All required columns present in training df.: {status}")

            # Validate no of columns in test df
            status = self.validate_number_of_columns(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in testing df."
            else:
                logger.info(f"All required columns present in testing df.: {status}")
                
            # Validate col data type in train df
            status = self.is_columns_exist(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training df."
            else:
                logger.info(f"All required columns data types are correct in training df.: {status}")
  
              # Validate col data type in test df
            status = self.is_columns_exist(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in testing df."
            else:
                logger.info(f"All required columns data types are correct in testing df.: {status}")
            
            validation_status = len(validation_error_msg) == 0
            
            data_ingestion_artifact = DataValidationArtifact(
                validation_status = validation_status,
                message = validation_error_msg,
                validation_report_file_path= self.data_validation_config.data_validation_report_file_path
            )
            
            # Ensure the directory for validation_report_file_path exists
            report_dir = os.path.dirname(self.data_validation_config.data_validation_report_file_path)  
            os.makedirs(report_dir, exist_ok=True)
            
            # Save validation status and message to  a JSON file
            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_msg.strip()
            }
            
            with open(self.data_validation_config.data_validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)
            
            logger.info("Data validation artifact created and save to JSON file.")
            logger.info(f"Data validation artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e) from e