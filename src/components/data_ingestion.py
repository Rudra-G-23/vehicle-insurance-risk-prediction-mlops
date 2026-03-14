import os
import sys

import pandas as pd 
from sklearn.model_selection import train_test_split

from src.logger import logger
from src.exception import MyException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.proj1_data import Proj1Data

class DataIngestion:
    
    def __init__(
        self,
        data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
    ):
        
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e, sys)
    
    def export_data_into_feature_store(self) -> pd.DataFrame:
        
        try:
            logger.info(f"Exporting data from MongoDB")
            data = Proj1Data()
            df = data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            logger.info(f"Shape of df: {df.shape}")
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            df.to_csv(feature_store_file_path, index=False, header=True)
            logger.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
                        
            return df

        except Exception as e:
            raise MyException(e, sys)
        
    def split_data_as_train_test(self, df: pd.DataFrame) -> None:
        
        try:
            logger.info("Performed train test split on dataframe.")
            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logger.info("Exited split_data_as_train_test method od Data_Ingestion class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logger.info("Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )
            logger.info("Exported train and test dataset.")
            
        except Exception as e:
            raise MyException(e, sys)
        
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        
        try:
            df = self.export_data_into_feature_store()
            logger.info("Got the data from MongoDB")
            
            self.split_data_as_train_test(df)
            logger.info("Performed train test split on the dataset.")
            
            data_ingestion_artifact = self.data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.training_file_path,
                test_file_path=self.testing_file_path
            )
            
            
            logger.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise Exception(e, sys)