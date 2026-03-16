import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer

from src.logger import logger
from src.exception import MyException

from src.constants.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from src.utils.main_utils import read_yaml_file, save_numpy_array_data, save_object

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact
)

class DataTransformation:
    
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig
        ):
        
        try:
            
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise MyException(e) from e

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e) from e

    def get_data_transformer_object(self) -> Pipeline:
        """ 
        Create and returns a data transformer object for the data,
        including gender mapping, dummy variable creation, column renaming,
        feature scaling, and type adjustments.
        """
        
        logger.info("Enter get_data_transformer_object method of DataTransformation class")
        
        try:
            
            # Initialize transformers
            numeric_transformer = StandardScaler()
            min_max_scaler = MinMaxScaler()
            logger.info("Transformers Initialized: StandardScaler &  MinMaxScaler")
            
            # Load Schema config
            num_features = self._schema_config["num_features"]
            mm_cols = self._schema_config["num_features"]
            logger.info("Columns loaded from schema.")
            
            # Creating preprocessor pipeline
            preprocessor = ColumnTransformer(
                transformers=[
                    ("standard_scaler", numeric_transformer, num_features),
                    ("min_max_scaler", min_max_scaler, mm_cols)
                ],
                remainder="passthrough"
            )
            logger.info("Preprocessor Pipeline created.")
        
            # Wrapping everything in a single pipeline
            final_pipeline = Pipeline(
                steps=[
                    ("Preprocessor", preprocessor)
                ]
            )            
            logger.info("Final Pipeline created.")
            
            logger.info("Exited get_data_transformer_object method of DataTransformation class.")

            return final_pipeline
        
        except Exception as e:
            raise MyException(e) from e
    
    def _map_gender_column(self, df):
        """Map Gender column to 0 for Female and 1 for Male."""
    
        try:
            
            logger.info("Mapping 'Gender' column to binary values.")
            df["Gender"] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
            return df
        
        except Exception as e:
            raise MyException(e) from e

    
    def _create_dummy_columns(self, df):
        """Create dummy variables for categorical features."""
    
        try:
            
            logger.info("Creating dummy variables for categorical features")
            df = pd.get_dummies(df, drop_first=True)
            return df
        
        except Exception as e:
            raise MyException(e) from e

    def _rename_columns(self, df):
        """Rename specific columns and ensure integer types for dummy columns."""
    
        try:
            
            logger.info("Renaming specific columns and casting to int")
            
            df = df.rename(columns={
                "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
                "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
            })
            
            for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
                if col in df.columns:
                    df[col] = df[col].astype('int')
                    
            return df
            
        except Exception as e:
            raise MyException(e) from e

    
    def _drop_id_column(self, df):
        """Drop `_id` column form df."""
    
        try:
            
            logger.info("Dropping 'id' column")
            drop_col = self._schema_config['drop_columns']
            
            if drop_col in df.columns:
                df = df.drop(drop_col, axis=1)
                
            return df
        
        except Exception as e:
            raise MyException(e) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """ 
        Initiate the data transformation component for the pipeline
        """
        
        try:
          
            # Load data
            train_df = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            logger.info("Train Test data loaded")
            
            # Features selection
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            logger.info(f"Input & Target column{TARGET_COLUMN} defined for the both train and test datasets. ")
            
            # Apply Custom transformation w/ sequences
            input_feature_train_df = self._map_gender_column(input_feature_train_df)
            input_feature_train_df = self._drop_id_column(input_feature_train_df)
            input_feature_train_df = self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df = self._rename_columns(input_feature_train_df)
            
            input_feature_test_df = self._map_gender_column(input_feature_test_df)
            input_feature_test_df = self._drop_id_column(input_feature_test_df)
            input_feature_test_df = self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df = self._rename_columns(input_feature_test_df)
            logger.info("Data Transformation applied to train and test datasets.")
            
            # Created pipeline
            logger.info("Starting data transformation.")
            preprocess = self.get_data_transformer_object()
            logger.info("Got the preprocessor object")
            
            # Transformation apply on Test & Train data
            logger.info("Initializing transformation for training-data.")
            input_feature_train_arr = preprocess.fit_transform(input_feature_train_df)
            
            logger.info("Initialized transformation for Testing data")
            input_feature_test_arr = preprocess.transform(input_feature_test_df)
            logger.info("Transformation done end to end for Train and Test data.")
            
            logger.info("Applying SMOTEENN for handling imbalanced dataset.")
            smt = SMOTEENN(sampling_strategy="minority")
            
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )
            
            logger.info("SMOTEENN applied to train-test df.")
            
            # Concatenation of features nad target
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            logger.info("Feature target concatenation done for train-test df.")
            
            # Save 
            save_object(self.data_transformation_config.transformed_object_file_path, preprocess)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            logger.info("Saving transformation object and transformed files.")
            
            logger.info("Excited from initiate_data_transformation method from DataTransformation class.")
            logger.info("Data Transformation completed successfully.")
            
            return DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
            )
        
        except Exception as e:
            raise MyException(e) from e