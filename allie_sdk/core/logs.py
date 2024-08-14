"""Standardize Logging across the Library."""

import datetime
import logging


class LoggingConfigs(object):
    """Python Logging Configuration Dictionary."""

    @staticmethod
    def logging_configs() -> dict:
        """Return the Python Logging Configuration Dictionary.

        Returns:
            dict: Python Logging Configurations.

        """
        logging_config = dict(
            version=1,
            disable_existing_loggers=False,
            formatters={
                'standard': {'format': '%(asctime)s[%(name)s][%(levelname)s] %(message)s'},
                'console': {'format': '%(message)s'},
                'json': {'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                         'format': '%(asctime)s %(name)s %(levelname)s %(message)s'}
            },
            handlers={
                'file_for_allie': {'class': 'logging.FileHandler',
                         'formatter': 'standard',
                         'level': logging.DEBUG,
                         'filename': f'logs/allie-sdk-{datetime.date.today()}.log'},
                'console_for_allie': {'class': 'logging.StreamHandler',
                            'formatter': 'console',
                            'level': logging.INFO,
                            'stream': 'ext://sys.stdout'},
                'api_json': {'class': 'logging.FileHandler',
                             'formatter': 'json',
                             'level': logging.DEBUG,
                             'filename': f'logs/alation-rest-{datetime.date.today()}.json'}
            },
            loggers={
                'allie_sdk_logger': {
                    'handlers': ['file_for_allie', 'console_for_allie', 'api_json'],
                    'level': logging.DEBUG
                }
            }
        )

        return logging_config
