"""Alation REST API Otype Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass

@dataclass
class Otype(BaseClass):
    name: str = field(default=None)
