import os
from datetime import datetime
from dataclasses import dataclass

import src.constants.constants as constants


# Generate timestamp for each pipeline run
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
@dataclass
class TrainingPipelineConfig:
    """
    Configuration for the overall training pipeline.

    Attributes
    ----------
    pipeline_name : str
        Name of the ML pipeline.

    artifact_dir : str
        Directory where pipeline artifacts will be stored.

    timestamp : str
        Unique timestamp for the current pipeline run.
    """

    pipeline_name: str = constants.PIPELINE_NAME 
    artifact_dir: str = os.path.join(constants.ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP

# Create pipeline config object
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    """
    Configuration for the data ingestion component.

    This class defines paths and parameters used during the
    data ingestion stage of the ML pipeline.
    """

    # Base directory for data ingestion artifacts
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifact_dir,
        constants.DATA_INGESTION_BASE_DIR_NAME
    )

    # Feature store dataset path
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir,
        constants.DATA_INGESTION_FEATURE_STORE_DIR,
        constants.DATA_FILE_NAME
    )

    # Training dataset path
    training_file_path: str = os.path.join(
        data_ingestion_dir,
        constants.DATA_INGESTION_INGESTED_DIR,
        constants.TRAIN_FILE_NAME
    )

    # Testing dataset path
    testing_file_path: str = os.path.join(
        data_ingestion_dir,
        constants.DATA_INGESTION_INGESTED_DIR,
        constants.TEST_FILE_NAME
    )

    # Train-test split ratio
    train_test_split_ratio: float = constants.DATA_INGESTION_TEST_SPLIT_RATIO

    # MongoDB collection name
    collection_name: str = constants.DATA_INGESTION_COLLECTION_NAME

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir,
        constants.DATA_VALIDATION_BASE_DIR_NAME
    )
    data_validation_report_file_path = os.path.join(
        data_validation_dir,
        constants.DATA_VALIDATION_REPORT_FILE_NAME
    )

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir,
        constants.DATA_TRANSFORMATION_BASE_DIR_NAME
    )
    transformed_train_file_path: str = os.path.join(
        data_transformation_dir,
        constants.DATA_TRANSFORMATION_BASE_DIR_NAME,
        constants.TRAIN_FILE_NAME.replace("csv", 'npy')
    )
    transformed_test_file_path: str = os.path.join(
        data_transformation_dir,
        constants.DATA_TRANSFORMATION_BASE_DIR_NAME,
        constants.TEST_FILE_NAME.replace('csv', 'npy')
    )
    transformed_object_file_path: str = os.path.join(
        data_transformation_dir,
        constants.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        constants.PREPROCESSING_OBJECT_FILE_NAME
    )

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifact_dir,
        constants.MODEL_TRAINER_BASE_DIR_NAME
    )
    trained_model_file_path: str = os.path.join(
        model_trainer_dir,
        constants.MODEL_TRAINER_TRAINED_MODEL_DIR,
        constants.MODEL_FILE_NAME
    )
    
    model_config_file_path: str = os.path.join(
        model_trainer_dir,
        constants.MODEL_FILE_NAME
    )
    
    expected_accuracy: float = constants.MODEL_TRAINER_EXPECTED_SCORE
    
    # Model Para
    _n_estimators: int = constants.MODEL_TRAINER_N_ESTIMATORS
    _min_samples_split: int = constants.MODEL_TRAINER_MIN_SAMPLES_SPLIT
    _min_samples_leaf: int = constants.MODEL_TRAINER_MIN_SAMPLES_LEAF
    _max_depth: int = constants.MODEL_TRAINER_MIN_SAMPLES_SPLIT_MAX_DEPTH
    _criterion: str = constants.MODEL_TRAINER_MIN_SAMPLES_SPLIT_CRITERION
    _radom_state: int = constants.MODEL_TRAINER_MIN_SAMPLES_SPLIT_RANDOM_STATE
