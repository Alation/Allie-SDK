"""Standardize Logging across the Library."""
import datetime
import logging
import os
import time

log_level_name = os.getenv("ALATION_SDK_LOG_LEVEL", "INFO")
try:
    log_level = getattr(logging, log_level_name.upper())
    if not isinstance(log_level, int):
        log_level = logging.INFO
except AttributeError:
    log_level = logging.INFO


def clean_old_logs(days: int = 7) -> None:
    """Remove log files older than the specified number of days."""
    for log_file in os.listdir("logs"):
        log = os.path.join("./logs", log_file)
        if os.stat(log).st_mtime < time.time() - days * 86400:
            if os.path.isfile(log):
                os.remove(log)


def ensure_log_directory() -> bool:
    """Return True if the log directory was created or already exists."""
    try:
        os.makedirs("logs", exist_ok=True)
        return os.path.exists("logs")
    except:
        return False

core_handlers = {
    "file_for_allie": {
        "class": "logging.FileHandler",
        "formatter": "standard",
        "level": log_level,
        "filename": f"logs/allie-sdk-{datetime.date.today()}.log",
    },
    "console_for_allie": {
        "class": "logging.StreamHandler",
        "formatter": "console",
        "level": log_level,
        "stream": "ext://sys.stdout",
    },
    "api_json": {
        "class": "logging.FileHandler",
        "formatter": "json",
        "level": log_level,
        "filename": f"logs/alation-rest-{datetime.date.today()}.json",
    },
}

class LoggingConfigs(object):
    """
    Python Logging Configuration Dictionary.

    Reads ALATION_SDK_LOG_HANDLERS env variable for the list of logger handlers.

    If unset or empty, the default handler console_for_allie is added.

    If file handlers are listed, the logs directory is created.

    The possible logger handlers are:
        - console_for_allie
        - file_for_allie
        - api_json
    """

    @staticmethod
    def handlers_from_env() -> list[str]:
        """Return a list of logging handlers from the environment variable."""
        handlers = os.getenv("ALATION_SDK_LOG_HANDLERS") or "console_for_allie"
        return handlers.strip().split(",")

    @staticmethod
    def logging_configs() -> dict:
        """Return the Python Logging Configuration Dictionary.

        Returns:
            dict: Python Logging Configurations.

        """
        enabled_handlers = LoggingConfigs.handlers_from_env()
        file_handlers = {"file_for_allie", "api_json"}
        if set(enabled_handlers) & file_handlers:
            log_dir_exists = ensure_log_directory()
            if not log_dir_exists:
                enabled_handlers = list(set(enabled_handlers) - file_handlers)

        handler_configs = {
            k: v for k, v in core_handlers.items() if k in enabled_handlers
        }

        logging_config = dict(
            version=1,
            disable_existing_loggers=False,
            formatters={
                "standard": {
                    "format": "%(asctime)s[%(name)s][%(levelname)s] %(message)s"
                },
                "console": {"format": "%(message)s"},
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                },
            },
            handlers=handler_configs,
            loggers={
                "allie_sdk_logger": {
                    "handlers": enabled_handlers,
                    "level": log_level,
                }
            },
        )

        return logging_config
