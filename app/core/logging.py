import logging
import logging.config
import sys
import json
from datetime import datetime

from app.core.config import get_settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logging() -> None:
    settings = get_settings()

    is_production = settings.ENVIRONMENT == "production"

    if is_production:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        level = settings.LOG_LEVEL.upper()

        root = logging.getLogger()
        root.setLevel(level)
        root.handlers = [handler]

    else:
        logging.config.dictConfig({
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": (
                        "[%(asctime)s] "
                        "[%(levelname)s] "
                        "[%(name)s] "
                        "- %(message)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": settings.LOG_LEVEL.upper(),
            },
        })
