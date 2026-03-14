""" 
Data Extraction Module

This module is responsible for fetching data from MongoDB
and converting it into a Pandas DataFrame for further
processing in the ML pipeline.
"""

import sys
import numpy as np
import pandas as pd
from typing import Optional

from src.logger import logger
from src.exception import MyException
from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME

class Proj1Data:
    """ 
    Data access layer for retrieving data from MongoDB.
    
    This class establishes a MongoDB connection using the 
    MongoDBClient class and provides utility methods to 
    export MongoDB collections as Pandas DataFrames.
    """
    
    def __init__(self) -> None:
        """
        Initialize MongoDB client connection.

        Raises:
            MyException: If MongoDB connection initialization fails.
        """
        
        try:
            logger.info("Initializing MongoDB client connection ...")
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            logger.info("MongoDB client initialized successfully. ")
        
        except Exception as e:
            raise MyException(e) from e

    def export_collection_as_dataframe(
        self,
        collection_name: str,
        database_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Export a MongoDB collection to fetch data from.

        Args:
            collection_name (str): Name of the MongoDB collection to fetch data from.
            database_name (Optional[str], optional): Name of the MongoDB database. If not
                provided, the default DATABASE_NAME constant will be used.

        Raises:
            MyException: Custom Exception for handle error.

        Returns:
            pd.DataFrame: Dataframe containing the collection data.
        
        Notes:
            - Removes the MongoDB `_id` column if present.
            - Replaces string value `na` with numpy NaN.
        """
        try:
            # Access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Convert collection data to DataFrame and preprocess
            print("Fetching data from mongoDB")
            df = pd.DataFrame(list(collection.find()))
            
            logger.info(f"Data fetched successfully. Number of records: {len(df)}")
            
           # Delete the `_id` column
            if "_id" in df.columns:
                df.drop(columns=['_id'], inplace=True)
            
            # Fill nan value
            df.replace({"na": np.nan}, inplace=True)
            
            return df
        
        except Exception as e:
            raise MyException(e) from e