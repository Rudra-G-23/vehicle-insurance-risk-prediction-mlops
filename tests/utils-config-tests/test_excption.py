from src.exception import MyException
from src.logger import logger

def test_exception():

    try:
        a = 10
        b = 0

        result = a / b

    except Exception as e:
        logger.error(e)
        raise MyException(e)


if __name__ == "__main__":
    test_exception()