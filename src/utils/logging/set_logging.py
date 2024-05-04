import sys

from loguru import logger


def set_logger(level: str = "INFO", serialize: bool = False):
    """
    Set logger for the module
    :param level: logger level (default INFO)
    :param serialize: serialize logs to json (default True)
    :return: Logger instance
    """
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "serialize": serialize,
                "level": level,
            }
        ]
    )

    return logger
