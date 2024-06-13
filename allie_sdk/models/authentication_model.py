"""Alation REST API Authentication Data Models."""

from dataclasses import dataclass, field
from datetime import datetime

from ..core.data_structures import BaseClass


@dataclass
class RefreshToken(BaseClass):
    refresh_token: str = field(default=None)
    user_id: int = field(default=None)
    created_at: datetime = field(default=None)
    name: str = field(default=None)
    token_expires_at: datetime = field(default=None)
    token_status: str = field(default=None)
    last_used_at: datetime = field(default=None)

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = self.convert_timestamp(self.created_at)
        if isinstance(self.token_expires_at, str):
            self.token_expires_at = self.convert_timestamp(self.token_expires_at)
        if isinstance(self.last_used_at, str):
            self.last_used_at = self.convert_timestamp(self.last_used_at)


@dataclass
class AccessToken(BaseClass):
    api_access_token: str = field(default=None)
    user_id: int = field(default=None)
    created_at: datetime = field(default=None)
    token_expires_at: datetime = field(default=None)
    token_status: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = self.convert_timestamp(self.created_at)
        if isinstance(self.token_expires_at, str):
            self.token_expires_at = self.convert_timestamp(self.token_expires_at)
