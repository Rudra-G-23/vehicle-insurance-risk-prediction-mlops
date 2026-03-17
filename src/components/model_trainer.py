import os
import sys
import numpy as np
from typing import Tuple

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.exception import MyException
from src.logger import logger

from src.utils.main_utils import load_numpy_array_data, load_object, save_object
from src.entity.config_entity import ModelTrainerConfig

from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from src.entity.estimator import MyModel

class ModelTrainer:
    
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig
        ):
        """
        Args:
            data_transformation_artifact (DataTransformationArtifact): Output reference of data transformation artifact stage
            model_trainer_config (ModelTrainerConfig): Configuration for model training
        """
        
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        
    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        """ 
        Method name  : get_model_object_and_report
        Description  : This function trains a RandomForestClassifier with specified parameters.
        
        Output       : Returns metric artifact object and trained model object
        On Failure   : Write an exception log and then raise an exception
        """
        
        try:
            
            logger.info("Training RadomForestClassifier with specified parameters")
            
            # splitting the train & test data into features and target variables
            X_train, y_train = train[:, :-1], train[:, -1]
            X_test, y_test = test[:, :-1], test[:, -1]
            logger.info("Train-test split done.")
                        
            # Parameters
            model = RandomForestClassifier(
                n_estimators= self.model_trainer_config._n_estimators,
                min_samples_split= self.model_trainer_config._min_samples_split,
                min_samples_leaf= self.model_trainer_config._min_samples_leaf,
                max_depth= self.model_trainer_config._max_depth,
                criterion= self.model_trainer_config._criterion,
                random_state= self.model_trainer_config._radom_state
            )

            # Fit model
            logger.info("Model training going on ...")
            model.fit(X_train, y_train)
            logger.info("Model Training completed.")
            
            # Prediction
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall =  recall_score(y_test, y_pred)
            
            # Creating metric artifact
            metric_artifact = ClassificationMetricArtifact(
                f1_score=f1,
                precision_score=precision,
                recall_score= recall
            )
            
            return model, metric_artifact
        
        except Exception as e:
            raise MyException(e) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """ 
        Method Name  : initiate_model_trainer
        Desc         : This function initiates the model training steps
        
        Output       : Returns model trainer artifact
        On Failure   : Write an exception log and then raise an exception
        """
        
        try:
             
            logger.info("Starting initiate model trainer")
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            logger.info("Train-Test data loaded inside model for training")
            
            train_model, metric_artifact = self.get_model_object_and_report(
                train= train_arr, test= test_arr
            )
            logger.info("Model object & artifact loaded.")
            
            preprocessing_obj = load_object(
                self.data_transformation_artifact.transformed_object_file_path
            )
            logger.info("Preprocessing object loaded.")

            # Check it model accuracy meet the expected threshold
            threshold = accuracy_score(train_arr[:, -1], train_model.predict(train_arr[:, :-1]))
            if threshold < self.model_trainer_config.expected_accuracy:
                logger.info("No model found with score above the base score.")
                raise Exception("No model found with score above the base score.")
            
            logger.info("Saving new model as performance is better then previous one.")
            my_model = MyModel(preprocessing_obj, train_model)
            save_object(self.model_trainer_config.model_config_file_path, my_model)
            logger.info("Save final model object that includes both preprocessing and the trained model.")
            
            model_trainer_artifact =  ModelTrainerArtifact(
                trained_model_file_path= self.model_trainer_config.trained_model_file_path,
                metric_artifact= metric_artifact
            )
            logger.info(f"Model trainer artifact {model_trainer_artifact}")
            
            return model_trainer_artifact
            
        except Exception as e:
            raise MyException(e) from e