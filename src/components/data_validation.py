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
            
            logger.info("Schema loaded successfully.")
            logger.info(f"Schema Loaded:  {self._schema_config}")

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
            
            missing_columns = list(set(expected_columns) - set(dataset_columns))
            extra_columns = list(set(dataset_columns) - set(expected_columns))

            return {
                "missing_columns": missing_columns,
                "extra_columns": extra_columns
            }

        except Exception as e:
            raise MyException(e) from e

    # Column Order Validation
    def validate_column_order(self, df: DataFrame):
        
        try:
            
            expected_columns = list(self._schema_config["columns"].keys())
            dataset_columns = list(df.columns)
            
            order_match = expected_columns == dataset_columns
            
            return order_match
        
        except Exception as e:
            raise MyException(e) from e
    
    # Validate data types
    def validate_dtypes(self, df: DataFrame):
        
        try:
            
            dtype_mismatch = {}
            
            for col, expected_dtype in self._schema_config["columns"].items():
                if col in df.columns:
                    actual_dtype = str(df[col].dtype)
                    
                    if actual_dtype != expected_dtype:
                        
                        dtype_mismatch[col] = {
                            "expected": expected_dtype,
                            "found": actual_dtype
                        }
                        
            return dtype_mismatch
        
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

            return {
                "missing_numerical_columns": missing_numerical_columns,
                "missing_categorical_columns": missing_categorical_columns
            }

        except Exception as e:
            raise MyException(e) from e

    # Missing Value Validation
    def validate_missing_values(self, df: DataFrame):
        
        try:
            
            missing_threshold = self._schema_config.get("missing_threshold", 0.3)
            missing_report = {}
            
            for col in df.columns:
                missing_pct = df[col].isnull().mean()
                
                if missing_pct > missing_threshold:
                    missing_report[col] = round(missing_pct, 3)
                    
            return missing_report
        
        except Exception as e:
            raise MyException(e) from e
    
    # Data Drift Check
    def detect_data_drift(self, train_df: DataFrame, test_df: DataFrame):
        
        try:
            
            drift_report = {}
            
            numerical_columns = self._schema_config["numerical_columns"]
            
            for col in numerical_columns:
                
                train_mean = train_df[col].mean()
                test_mean = test_df[col].mean()
                
                drift = abs(train_mean - test_mean)
                
                if drift > 0.1:
                    
                    drift_report[col] = {
                        "train_mean": round(train_mean, 3),
                        "test_mean": round(test_mean, 3),
                        "drift": round(drift, 3)
                    }
            return drift_report
            
        except Exception as e:
            raise MyException(e) from e
        
    # Main Validation Pipeline
    def initiate_data_validation(self) -> DataValidationArtifact:

        try:

            logger.info("[Data Validation] Starting Data Validation")
            
            train_df = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            
            # Column Validation
            train_column_report = self.validate_columns(train_df)
            test_column_report = self.validate_columns(test_df)
            
            # Column Order
            train_order_status = self.validate_column_order(train_df)
            test_order_status = self.validate_column_order(test_df)
            
            # Dtype Validation
            train_dtype_report = self.validate_dtypes(train_df)
            test_dtype_report = self.validate_dtypes(test_df)
            
            # Feature Group
            train_feature_report = self.validate_feature_groups(train_df)
            test_feature_report = self.validate_feature_groups(test_df)
            
            # Missing Value
            train_missing_report = self.validate_missing_values(train_df)
            test_missing_report = self.validate_missing_values(test_df)
            
            # Data Drift
            drift_report = self.detect_data_drift(train_df, test_df)
            
            validation_status = True
            
            if (
                train_column_report["missing_columns"]
                or test_column_report["missing_columns"]
                or train_dtype_report
                or test_dtype_report
                or drift_report
            ):
                validation_status = False

            validation_report = {

                "validation_status": validation_status,

                "train_dataset": {

                    "missing_columns": train_column_report["missing_columns"],
                    "extra_columns": train_column_report["extra_columns"],
                    "column_order_correct": train_order_status,
                    "dtype_mismatch": train_dtype_report,
                    "missing_numerical_columns": train_feature_report["missing_numerical_columns"],
                    "missing_categorical_columns": train_feature_report["missing_categorical_columns"],
                    "high_missing_values": train_missing_report
                },

                "test_dataset": {

                    "missing_columns": test_column_report["missing_columns"],
                    "extra_columns": test_column_report["extra_columns"],
                    "column_order_correct": test_order_status,
                    "dtype_mismatch": test_dtype_report,
                    "missing_numerical_columns": test_feature_report["missing_numerical_columns"],
                    "missing_categorical_columns": test_feature_report["missing_categorical_columns"],
                    "high_missing_values": test_missing_report
                },

                "data_drift": drift_report
            }

            report_path = self.data_validation_config.data_validation_report_file_path

            os.makedirs(os.path.dirname(report_path), exist_ok=True)

            with open(report_path, "w") as f:
                json.dump(validation_report, f, indent=4)

            logger.info(f"Validation report saved at {report_path}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message="Validation completed",
                validation_report_file_path=report_path
            )

            return data_validation_artifact

        except Exception as e:
            raise MyException(e, sys)