import sys
import numpy as np
import pandas as pd
from typing import Optional

from src.logger import logger
from src.exception import MyException
from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME

class Proj1Data:
    
    def __init__(self) -> None:
        try:
            logger.info("Initializing MongoDB client connection ...")
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            logger.info("MongoDB client initialized successfully. ")
        
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(
        self,
        collection_name: str,
        database_name: Optional[str] = None
    ) -> pd.DataFrame:
        
        try:
            logger.info(f"Fetching data from collection: {collection_name}")
            
            if database_name is None:
                df = self.mongo_client.database
            else:
                db = self.mongo_client.client[database_name]
            
            collection = db[collection_name]
            df = pd.DataFrame(list(collection.find()))
            
            logger.info(f"Data fetched successfully. Number of records: {len(df)}")
            
            if "_id" in df.columns:
                df.drop(columns=['_id'], inplace=True)
            
            df.replace({"na": np.nan}, inplace=True)
            
            return df
        
        except Exception as e:
            raise MyException (e, sys)