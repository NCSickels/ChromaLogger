"""
Custom colored wrapper for the Python Logging library.
"""

import logging
import logging.config
import re

import colorama
from termcolor import colored

colorama.just_fix_windows_console()

# Default theme content
theme_content = {
    "primary": {"color": "white", "highlight": None, "attributes": []},
    "warning": {"color": "light_yellow", "highlight": None, "attributes": []},
    "error": {"color": "red", "highlight": None, "attributes": []},
    "critical": {"color": "red", "highlight": None, "attributes": ["blink"]},
    "cyan": {"color": "cyan", "highlight": None, "attributes": []},
    "magenta": {"color": "magenta", "highlight": None, "attributes": []},
}


def apply_style(text: str, style: dict) -> str:
    """
    Applies the given style to the text with the specified color, highlight, and attributes.
    """
    return colored(
        text,
        color=style["color"],
        on_color=style["highlight"],
        attrs=style["attributes"],
    )


def c(text: str) -> str:
    """
    Applies color styling to the given text based on the default theme.

    Args:
        text (str): The text to be styled.

    Returns:
        str: The styled text.
    """
    result = text

    for key, style in theme_content.items():
        styled_portion = re.findall(f"<{key}>(.*?)</{key}>", text)
        if not styled_portion:
            continue
        for portion in styled_portion:
            result = re.sub(
                f"<{key}>(.*?)</{key}>", apply_style(portion, style), result, 1
            )

    return result


class ColorFormatter(logging.Formatter):
    """
    A custom logging formatter that adds color to log messages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record) -> str:
        format_prop = {
            logging.DEBUG: "primary",
            logging.INFO: "primary",
            logging.WARNING: "warning",
            logging.ERROR: "error",
            logging.CRITICAL: "critical",
        }
        date_text = c("<cyan>%(asctime)s</cyan>")
        message = c(
            f"<{format_prop[record.levelno]}>%(message)s</{format_prop[record.levelno]}>"
        )
        logger_name = c(f"<magenta>{record.name}</magenta>")

        level_prop = format_prop[record.levelno]
        level = c(f"<{level_prop}>{record.levelname}</{level_prop}>")

        log_format = f"{date_text} | [{level}] {logger_name}: {message}"
        formatter = logging.Formatter(log_format, datefmt="[%H:%M:%S]")
        formatted_message = formatter.format(record)

        return formatted_message


class Singleton(type):
    """
    A metaclass that ensures only one instance of a class is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]


class ChromaLogger(metaclass=Singleton):
    """
    The Logger class provides a singleton logger instance for logging messages.

    Usage:
    - Logger.debug("Debug message")
    - Logger.info("Info message")
    - Logger.warning("Warning message")
    - Logger.error("Error message")
    - Logger.critical("Critical message")
    """

    _logger: logging.Logger = None

    def __init__(self):
        super().__init__()
        logging.config.dictConfig(LOGGING_CONFIG)
        ChromaLogger._logger = logging.getLogger()

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Returns the logger instance.
        """
        return cls._logger

    @classmethod
    def setLevel(cls, level: int) -> None:
        """
        Sets the logging level for the logger.

        Args:
            level (int): The logging level to be set.
        """
        cls._logger.setLevel(level)

    @classmethod
    def debug(cls, message: str):  # Severity: 10
        cls._logger.debug(message)

    @classmethod
    def info(cls, message: str):  # Severity: 20
        cls._logger.info(message)

    @classmethod
    def warning(cls, message: str):  # Severity: 30
        cls._logger.warning(message)

    @classmethod
    def error(cls, message: str):  # Severity: 40
        cls._logger.error(message)

    @classmethod
    def critical(cls, message: str):  # Severity: 50
        cls._logger.critical(message)


def get_central_logger():
    return ChromaLogger.get_logger()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "[%H:%M:%S]",
        },
        "colored": {
            "()": "chromalogger.ColorFormatter",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "[%H:%M:%S]",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "colored_console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["colored_console"],
        },
    },
}
