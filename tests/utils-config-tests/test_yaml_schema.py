from src.utils.main_utils import read_yaml_file
from src.constants.constants import SCHEMA_FILE_PATH
import pprint

schema = read_yaml_file(SCHEMA_FILE_PATH)
pprint.pprint(schema["columns"])