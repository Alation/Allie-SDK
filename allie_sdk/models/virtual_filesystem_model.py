"""Alation REST API Virtual File System Model."""
import dataclasses
import json
from dataclasses import dataclass, field

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams

@dataclass
class VirtualFileSystem(BaseClass):
    pass

@dataclass
class VirtualFileSystemItem(BaseClass):
    path: str = field(default=None)
    name: str = field(default=None)
    is_directory: bool = field(default=None)
    size_in_bytes: int = field(default=None)
    ts_last_modified: str = field(default=None)
    ts_last_accessed: str = field(default=None)
    owner: str = field(default=None)
    group: str = field(default=None)
    permission_bits: int = field(default=None)
    storage_type: int = field(default=None)

    def generate_api_post_payload(self) -> dict:
        if self.path is None:
            raise InvalidPostBody("'path' is required for the POST payload")
        if self.name is None:
            raise InvalidPostBody("'name' is required for the POST payload")
        if self.is_directory is None:
            raise InvalidPostBody("'is_directory' is required for the POST payload")

        return dataclasses.asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})


