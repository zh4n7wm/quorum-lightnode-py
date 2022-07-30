import logging
import os
import sys
from logging.config import dictConfig

__all__ = ["get_logger"]

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": (
                "[%(asctime)s.%(msecs)03d] %(name)s in %(module)s"
                " at %(lineno)d %(levelname)s: %(message)s"
            ),
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
            "level": os.getenv("LOG_LEVEL", "DEBUG"),
        },
    },
    "loggers": {
        "gunicorn": {
            "handlers": ["console"],
            "level": logging.INFO,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": logging.INFO,
            "propagate": False,
        },
        "socketio": {
            "handlers": ["console"],
            "level": logging.ERROR,
            "propagate": False,
        },
    },
}

# config logger
dictConfig(logger_config)


def get_logger(name=None):
    return logging.getLogger(name)
