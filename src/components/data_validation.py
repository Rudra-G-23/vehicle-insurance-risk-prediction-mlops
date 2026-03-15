import os
import sys
import json

import pandas as pd
from pandas import DataFrame

from src.exception import MyException
from src.logger import logger
from src.entity import DataValidationArtifact
from src.entity import DataValidationConfig, DataIngestionConfig
import src.constants.constants as constants

class DataValidation:
    
    def __init__(
        self,
        ):
        pass