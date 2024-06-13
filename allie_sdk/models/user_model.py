"""Alation REST API User Data Models."""

from dataclasses import dataclass, field
from datetime import datetime

from ..core.data_structures import BaseClass, BaseParams


@dataclass
class User(BaseClass):
    display_name: str = field(default=None)
    email: str = field(default=None)
    id: int = field(default=None)
    profile_id: int = field(default=None)
    url: str = field(default=None)
    last_login: datetime = field(default=None)
    ts_created: datetime = field(default=None)
    first_name: str = field(default=None)
    last_name: str = field(default=None)
    role: str = field(default=None)
    title: str = field(default=None)
    username: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.last_login, str):
            self.last_login = self.convert_timestamp(self.last_login)
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)


@dataclass
class UserParams(BaseParams):
    id: set = field(default_factory=set)
    profile_id: set = field(default_factory=set)
    display_name: set = field(default_factory=set)
    display_name__contains: set = field(default_factory=set)
    display_name__icontains: set = field(default_factory=set)
    email: set = field(default_factory=set)
    email__contains: set = field(default_factory=set)
    email__icontains: set = field(default_factory=set)
