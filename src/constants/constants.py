import os
from datetime import date 
from dotenv import load_dotenv

load_dotenv()

""" 
MongoDB related constant start with MONGO VAR NAME
"""
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

""" 
Utility Variables 
"""
PIPELINE_NAME: str = "vehicle_insurance_pipeline"
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME: str = "model.pkl"

TARGET_COLUMN: str = "Response"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

DATA_FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


""" 
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_BASE_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_COLLECTION_NAME: str = "Proj1-Data"
DATA_INGESTION_TEST_SPLIT_RATIO: float = 0.25

""" 
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_BASE_DIR_NAME: str ="data_validation"
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yml"

""" 
Data Transformation related constants start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_BASE_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object" 

""" 
Data Trainer related constants start with MODEL_TRAINER VAR NAME
"""
MODEL_TRAINER_BASE_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")

MODEL_TRAINER_N_ESTIMATORS: int = 200
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6
MODEL_TRAINER_MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10
MODEL_TRAINER_MIN_SAMPLES_SPLIT_CRITERION: str = "entropy"
MODEL_TRAINER_MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101