import sys
from loguru import logger


def get_detailed_error_message(error: Exception, error_detail: sys):
    """
    Extract detailed information about an exception.

    Returns:
        Formatted string containing file name, line number, and error message.
    """
    
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in script [{file_name}] "
        f"at line [{line_number}] "
        f"message [{str(error)}]"
    )

    return error_message


class MyException(Exception):
    """
    Custom exception class used across the ML project.
    """
    
    def __init__(self, error: Exception, error_detail=sys):

        message = get_detailed_error_message(error, error_detail)

        logger.error(message)

        super().__init__(message)

        self.error_message = message