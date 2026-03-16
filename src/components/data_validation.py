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

            # Load schema
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            
            logger.info(f"Schema Loaded: {self._schema_config}")

        except Exception as e:
            raise MyException(e) from e

    # Read Data
    @staticmethod
    def read_data(file_path: str) -> DataFrame:
        try:
            logger.info(f"Reading data from {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e) from e

    
    # Validate Column Names
    def validate_columns(self, df: DataFrame) -> bool:
        try:

            expected_columns = list(self._schema_config["columns"].keys())
            dataset_columns = list(df.columns)

            logger.info(f"Expected columns: {expected_columns}")
            logger.info(f"Dataset columns: {dataset_columns}")

            missing_columns = list(set(expected_columns) - set(dataset_columns))
            extra_columns = list(set(dataset_columns) - set(expected_columns))

            if missing_columns:
                logger.error(f"Missing Columns: {missing_columns}")

            if extra_columns:
                logger.warning(f"Unexpected Columns: {extra_columns}")

            if missing_columns:
                return False

            return True

        except Exception as e:
            raise MyException(e) from e

    
    # Validate Numerical + Categorical Columns
    def validate_feature_groups(self, df: DataFrame) -> bool:

        try:

            df_columns = df.columns

            missing_numerical_columns = []
            missing_categorical_columns = []

            # Check numerical
            for col in self._schema_config["numerical_columns"]:
                if col not in df_columns:
                    missing_numerical_columns.append(col)

            # Check categorical
            for col in self._schema_config["categorical_columns"]:
                if col not in df_columns:
                    missing_categorical_columns.append(col)

            if len(missing_numerical_columns) > 0:
                logger.error(f"Missing Numerical Columns: {missing_numerical_columns}")

            if len(missing_categorical_columns) > 0:
                logger.error(f"Missing Categorical Columns: {missing_categorical_columns}")

            if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0:
                return False

            return True

        except Exception as e:
            raise MyException(e) from e

    
    # Main Validation Pipeline
    def initiate_data_validation(self) -> DataValidationArtifact:

        try:

            logger.info("Starting Data Validation")

            validation_error_msg = ""

            train_df = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            
            # Train Column Validation            
            status = self.validate_columns(train_df)

            if not status:
                validation_error_msg += "Train dataset missing required columns.\n"
            else:
                logger.info("Train dataset columns validated")

            
            # Test Column Validation            
            status = self.validate_columns(test_df)

            if not status:
                validation_error_msg += "Test dataset missing required columns.\n"
            else:
                logger.info("Test dataset columns validated")

            
            # Train Feature Validation            
            status = self.validate_feature_groups(train_df)

            if not status:
                validation_error_msg += "Train dataset feature group mismatch.\n"
            else:
                logger.info("Train dataset feature groups validated")

            
            # Test Feature Validation            
            status = self.validate_feature_groups(test_df)

            if not status:
                validation_error_msg += "Test dataset feature group mismatch.\n"
            else:
                logger.info("Test dataset feature groups validated")

            
            # Final Validation Status            
            validation_status = validation_error_msg == ""

            logger.info(f"Validation Status: {validation_status}")

            
            # Create Validation Artifact            
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg.strip(),
                validation_report_file_path=self.data_validation_config.data_validation_report_file_path
            )

            
            # Save Validation Report            
            report_path = self.data_validation_config.data_validation_report_file_path

            os.makedirs(os.path.dirname(report_path), exist_ok=True)

            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_msg.strip()
            }

            with open(report_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)

            logger.info(f"Validation report saved at {report_path}")

            return data_validation_artifact

        except Exception as e:
            raise MyException(e) from e