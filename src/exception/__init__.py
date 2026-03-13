import sys
import traceback
from loguru import logger

def get_detailed_error_message(error: Exception) -> str:
    """
    Extract detailed information about an exception.

    Returns:
        Formatted string containing file name, line number, and error message.
    """

    exc_type, exc_value, exc_tb = sys.exc_info()

    if exc_tb is None:
        return f"Error: {str(error)}"

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    message = (
        f"Error occurred in python script [{file_name}] "
        f"at line [{line_number}] "
        f"error message [{str(error)}]"
    )

    return message


class MyException(Exception):
    """
    Custom exception class used across the ML project.
    """

    def __init__(self, error: Exception):
        detailed_message = get_detailed_error_message(error)

        logger.error(traceback.format_exc())

        super().__init__(detailed_message)

        self.error_message = detailed_message

    def __str__(self) -> str:
        return self.error_message