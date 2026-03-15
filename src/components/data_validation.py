import os
import sys
import json

import pandas as pd
from pandas import DataFrame

from src.exception import MyException
from src.logger import logger
from src.entity import DataValidationArtifact
from src.entity import DataValidationConfig, DataIngestionConfig
from src.constants.constants import SCHEMA_FILE_PATH
from src.utils.main_utils import read_yaml_file

class DataValidation:
    
    def __init__(
        self,
        data_ingestion_artifact: DataValidationArtifact,
        data_validation_config: DataValidationConfig
        ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e) from e
        
    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            status = len(df.columns) == len(self._schema_config["columns"])
            logger.info(f"Is required columns present: [{status}]")
            
            return status
        
        except Exception as e:
            raise MyException(e) from e