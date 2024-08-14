"""Alation REST API Trust Check Flag Data Models."""

import logging
from dataclasses import dataclass, field
from datetime import datetime

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams
from .user_model import User

LOGGER = logging.getLogger('allie_sdk_logger')


@dataclass
class TrustCheckFlagSubject(BaseClass):
    id: int = field(default=None)
    otype: str = field(default=None)
    url: str = field(default=None)


@dataclass
class TrustCheckFlag(BaseClass):
    id: int = field(default=None)
    flag_type: str = field(default=None)
    flag_reason: str = field(default=None)
    ts_created: datetime = field(default=None)
    ts_updated: datetime = field(default=None)
    subject: TrustCheckFlagSubject = field(default=None)
    user: User = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)
        if isinstance(self.subject, dict):
            self.subject = TrustCheckFlagSubject.from_api_response(self.subject)
        if isinstance(self.user, dict):
            self.user = User.from_api_response(self.user)

    def generate_api_put_body(self) -> dict:
        if self.flag_type.upper() in ['WARNING', 'DEPRECATION']:
            return {'flag_reason': self.flag_reason}
        else:
            raise InvalidPostBody(
                f"The Trust Check can not be updated when the flag reason is '{self.flag_reason}'")


@dataclass
class TrustCheckFlagItem:
    flag_type: str = field(default=None)
    flag_reason: str = field(default=None)
    subject: TrustCheckFlagSubject = field(default_factory=TrustCheckFlagSubject)

    def generate_api_post_payload(self) -> dict:
        payload = {}
        if self.flag_type.upper() not in ['DEPRECATION', 'ENDORSEMENT', 'WARNING']:
            raise InvalidPostBody(
                f"The value '{self.flag_type}' is not a supported 'flag_type' value.\n"
                f"Please update the value to: 'DEPRECATION', 'ENDORSEMENT', 'WARNING'")
        payload['flag_type'] = self.flag_type.upper()

        if self.flag_type == 'ENDORSEMENT' and self.flag_reason:
            LOGGER.warning(
                f"The flag type of 'ENDORSEMENT' does not support setting a flag_reason."
                f"The flag_reason value will not be included in the REST API POST Call.")

        if self.flag_type in ['DEPRECATION', 'WARNING']:
            payload['flag_reason'] = self.flag_reason

        for item in [self.subject.otype, self.subject.id]:
            if item is None:
                raise InvalidPostBody(
                    "'subject.otype', and 'subject.id' are required fields for the API POST Call")
        payload["subject"] = {"id": self.subject.id, "otype": self.subject.otype.lower()}

        return payload


@dataclass
class TrustCheckFlagParams(BaseParams):
    oid: set = field(default_factory=set)
    otype: set = field(default_factory=set)
