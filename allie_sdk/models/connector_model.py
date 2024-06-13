"""Alation REST API Connector Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass

@dataclass
class Connector(BaseClass):
    id: int = field(default=None)
    name: str = field(default=None)
    uses_agent: bool = field(default=None)
    connector_version: str = field(default=None)
    connector_category: str = field(default=None)
