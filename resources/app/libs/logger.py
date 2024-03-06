from __future__ import annotations

import logging
from enum import Enum


class LogLevel(int, Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class CustomFormatter(logging.Formatter):
    # grey = "\x1b[38;2;190;190;190m" # ? RGB not supported by Grafana
    # green = "\x1b[38;2;55;220;37m" # ? RGB not supported by Grafana
    # bold_green = "\x1b[38;2;55;220;37;1m" # ? RGB not supported by Grafana
    green = "\x1b[32m"
    bold_green = "\x1b[32;1m"
    # yellow = "\x1b[38;2;240;255;0m" # ? RGB not supported by Grafana
    # bold_yellow = "\x1b[38;2;240;255;0;1m" # ? RGB not supported by Grafana
    yellow = "\x1b[33m"
    bold_yellow = "\x1b[33;1m"
    # red = "\x1b[38;2;255;0;0m" # ? RGB not supported by Grafana
    # bold_red = "\x1b[38;2;255;0;0;1m" # ? RGB not supported by Grafana
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    bg_red = "\x1b[41m"
    reset = "\x1b[0m"
    format = "%(asctime)s - [%(levelname)s] [%(threadName)s] %(name)s::%(funcName)s %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: reset + format + reset,
        logging.INFO: bold_green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: bold_red + format + reset,
        logging.CRITICAL: bg_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt=Logger._datefmt)
        return formatter.format(record)


class Logger:
    """Logger instance generator

    Attributes:
        __loggers (dict): List of loggers
        _default_name (str): Default logger name
        _default_level (int): Default logger level
        _datefmt (str): Default date format

    Methods:
        get_logger: Get a logger instance or create it if it doesn't exist
    """

    # ? List of loggers
    __loggers = {}

    # ? Class parameters
    _default_name = "CILogger"
    _default_level = LogLevel.DEBUG.value
    _datefmt = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def get_logger(
        cls,
        name: str | None = None,
        level: int | None = None,
    ) -> logging.Logger:
        """Get a logger instance or create it if it doesn't exist

        Parameters:
            name (str): Logger name
            level (int): Logger level

        Returns:
            Logger: Logger instance
        """
        # ? Set default values
        if name is None:
            name = cls._default_name
        if level is None:
            level = cls._default_level

        # ? Check if logger already exists
        if name in cls.__loggers:
            return cls.__loggers[name]

        # ? Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # ? Create handler
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(CustomFormatter())

        # ? Add handler to logger
        logger.addHandler(handler)

        # ? Add logger to list
        cls.__loggers[name] = logger
        logger.propagate = False

        return logger


# ------------------------------------------------------------------ #
# The following classes are used by uvicorn to filter logs
# ------------------------------------------------------------------ #


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().find("/healthcheck") == -1

