import os
from datetime import date 
from dotenv import load_dotenv

load_dotenv()

# Database details
DATABASE_NAME: str = "Proj1"
COLLECTION_NAME: str = "Proj1-Data"

# Mongo credentials (from environment variables)
MONGO_USERNAME: str | None = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD: str | None = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER: str | None = os.getenv("MONGO_CLUSTER")

# MongoDB connection URL
MONGODB_URL_KEY: str = (
    f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/"
)