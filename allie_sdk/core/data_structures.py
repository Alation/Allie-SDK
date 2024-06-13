"""Core Functions for working with Python Dataclasses"""

import inspect
from dataclasses import dataclass, fields
from datetime import datetime

# Base data class with method that we want to use across all other data classes
@dataclass
class BaseClass:
    # noinspection PyArgumentList
    # This method makes sure that we can deal with API responses
    # that include properties that we are not expecting
    # Normally if response doesn't match the data class definition a 100%
    # this would result in an error.
    # By using method you can handle this exception gracefully. 
    @classmethod
    def from_api_response(cls, body_params: dict):
        return cls(**{
            k: v for k, v in body_params.items()
            if k in inspect.signature(cls).parameters
        })

    @staticmethod
    def convert_timestamp(s_date: str) -> datetime:
        tz_formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f%z']

        for pattern in tz_formats:
            try:
                return datetime.strptime(s_date, pattern)
            except:
                pass


@dataclass
class BaseParams:
    def generate_params_dict(self) -> dict:
        params = {}

        for item in fields(self):
            value = getattr(self, item.name)

            if value:
                params[item.name] = value

        return params
