import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logger
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()

class MongoDBClient:
    
    client = None
    
    def __init__(self, database_name:str = DATABASE_NAME) -> None:
        try:
            
            if MongoDBClient.client is None:
                
                logger.info("connection to MongoDB ...")
                

                MongoDBClient.client = pymongo.MongoClient(
                    MONGODB_URL_KEY,
                    tlsCAFile=ca,
                    serverSelectionTimeoutMS=5000
                )

                MongoDBClient.client.server_info()
                
                logger.info("MongoDB connection established.")
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
        
        except Exception as e:
            raise MyException(e, sys)