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
            formatters={
                'standard': {'format': '%(asctime)s[%(name)s][%(levelname)s] %(message)s'},
                'console': {'format': '%(message)s'},
                'json': {'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                         'format': '%(asctime)s %(name)s %(levelname)s %(message)s'}
            },
            handlers={
                'file': {'class': 'logging.FileHandler',
                         'formatter': 'standard',
                         'level': logging.DEBUG,
                         'filename': f'logs/allie-sdk-{datetime.date.today()}.log'},
                'console': {'class': 'logging.StreamHandler',
                            'formatter': 'console',
                            'level': logging.INFO,
                            'stream': 'ext://sys.stdout'},
                'api_json': {'class': 'logging.FileHandler',
                             'formatter': 'json',
                             'level': logging.DEBUG,
                             'filename': f'logs/alation-rest-{datetime.date.today()}.json'}
            },
            root={'handlers': ['file', 'console'],
                  'level': logging.NOTSET},
            loggers={
                'api_json': {'handlers': ['api_json'],
                             'level': logging.DEBUG,
                             'qualname': 'alation_rest'}
            }
        )

        return logging_config
