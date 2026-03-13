""" 
MongoDB Connection Module

This module provides a reuseable MongoDB client for the application.
It ensures that only one MongoDB connection is created and add reused
across the entire application.

Dependencies:
    - pymongo: MongoDB Driver for the python
    - certifi: Provides CA bundle for secure TLS connection
"""

import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logger
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Path to certificate authority file
# Used for secure TLS connection with he MongoDB Atlas
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for managing the MongoDB connection.
    
    This class ensures that only one MongoDB client instance is created
    and reused across the application to avoid multiple connections.
    
    Attributes
    ----------
    client : pymongo.MongoClient
        Shared MongoDB client instance.
    
    database: pymongo.database.Database
        MongoDB database instance used by the application.
    """
    
    # Shared MongoDB client (class level variable)
    client = None
    
    def __init__(self, database_name:str = DATABASE_NAME) -> None:
        """
        Initialize MongoDB connection.
        
        If a MongoDB connection does not already exist, this method
        creates a new connection and verifies it.

        Args:
            database_name (str): Name fo the MongoDB database to connect to.

        Raises:
            MyException: If any error occurs while establishing the connection.
        """
        
        try:
            
            # Create MongoDB connection only once
            if MongoDBClient.client is None:
                
                logger.info("connection to MongoDB ...")
                
                # Initialize MongoDB client
                MongoDBClient.client = pymongo.MongoClient(
                    MONGODB_URL_KEY,
                    tlsCAFile=ca, # secure TLS certificate
                    serverSelectionTimeoutMS=5000 # timeout if server not reachable
                )

                # Force connection to verify MongoDB server availability
                MongoDBClient.client.server_info()
                
                logger.info("MongoDB connection established.")
            
            # Assign the shared client to instance
            self.client = MongoDBClient.client
            
            # Access the specified database
            self.database = self.client[database_name]
        
        except Exception as e:
            # Wrap original exception inside custom exception
            raise MyException(e, sys)