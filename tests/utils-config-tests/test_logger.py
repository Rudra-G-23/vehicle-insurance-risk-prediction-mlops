from src.logger import logger

def test_logger_div():
    try:
        x = 1 / 0
    except Exception as e:
        logger.error("Error during training")

if __name__ == "__main__":
    test_logger_div()