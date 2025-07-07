import logging.config
import os
from pathlib import Path


LOG_DIR = Path(os.getenv("LOG_PATH", "logs")).resolve()
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "daily_file": {
            "formatter": "default",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join("logs", "app.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 14,
            "encoding": "utf-8",
            "utc": False,
            "delay": True,
        },
    },
    "loggers": {
        "custom-logger": {
            "handlers": ["console", "daily_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)
