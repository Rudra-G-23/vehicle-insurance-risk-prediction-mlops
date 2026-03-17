import sys
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import MyException
from src.logger import logger

class TargetValueMapping:
    def __init__(self):
        self.yest: int = 0
        self.no: int = 1
        
    def _asdict(self):
        return __dict__
    
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(
            zip(mapping_response.values(),mapping_response.keys())
        )

class MyModel:
    
    def __init__(
        self,
        preprocessing_object: Pipeline,
        trained_model_object: object
        ):
        """
        Args:
            preprocessing_object (Pipeline): Input Object of preprocessor
            trained_model_object (object): Input Object of trained model
        """
        
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        
    def predict(self, df: pd.DataFrame) -> DataFrame:
        """ 
        Function accepts preprocessed inputs (with all the custom transformation already applied)
        applies scaling using preprocessing_object, and performs prediction on transformed features.
        """
        
        try:
            
            logger.info("Starting prediction process ..")
            
            # Step 1: Apply scaling transformations using the pre-trained preprocessing object.
            transformed_feature = self.preprocessing_object.transform(df)
            
            # Step 2: Perform Prediction using the trained model
            logger.info("Using the trained model to get prediction")
            predictions = self.trained_model_object.predict(transformed_feature)
            
            return predictions
        
        except Exception as e:
            logger.exception("Error occurred in predict method",)
            raise MyException(e) from e