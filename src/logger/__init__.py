import os
from loguru import logger
from from_root import from_root
from datetime import datetime

# log directory
LOG_DIR = "logs"
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)

# log file name
LOG_FILE = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"
log_file_path = os.path.join(log_dir_path, LOG_FILE)

# remove default logger
logger.remove()

# console logging
logger.add(
    sink=lambda msg: print(msg, end=""),
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
    level="INFO"
)

# file logging with rotation
logger.add(
    log_file_path,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} | {name}:{function}:{line} | {message}",
    level="DEBUG",
    rotation="5 MB",
    retention=3
)