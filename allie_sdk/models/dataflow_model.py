"""Alation REST API Dataflow Data Models."""

from dataclasses import dataclass, field
from ..core.data_structures import BaseClass, BaseParams
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody


@dataclass(kw_only=True)
class DataflowBase(BaseClass):
    """Common properties for Dataflow objects."""
    title: str = field(default=None)
    description: str = field(default=None)
    content: str = field(default=None)
    group_name: str = field(default=None)


@dataclass(kw_only=True)
class Dataflow(DataflowBase):
    """Dataflow object definition."""
    external_id: str = field(default=None)
    id: int = field(default=None)

    def generate_api_post_payload(self) -> dict:
        if self.external_id is None:
            raise InvalidPostBody("'external_id' is a required field for Dataflow POST payload body")
        payload = {"external_id": self.external_id}
        if self.title:
            payload["title"] = self.title
        if self.description:
            payload["description"] = self.description
        if self.content:
            payload["content"] = self.content
        if self.group_name:
            payload["group_name"] = self.group_name
        return payload


@dataclass(kw_only=True)
class DataflowPatchItem(DataflowBase):
    """Dataflow object definition for PATCH requests."""
    id: int

    def generate_api_patch_payload(self) -> dict:
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Dataflow PATCH payload body")
        payload = {"id": self.id}
        if self.title:
            payload["title"] = self.title
        if self.description:
            payload["description"] = self.description
        if self.content:
            payload["content"] = self.content
        if self.group_name:
            payload["group_name"] = self.group_name
        return payload


@dataclass(kw_only=True)
class DataflowPathObject(BaseClass):
    """Single object within a Dataflow path segment."""
    otype: str = field(default=None)
    key: str = field(default=None)

    def generate_api_payload(self) -> dict:
        if self.otype is None or self.key is None:
            raise InvalidPostBody("'otype' and 'key' are required fields for Dataflow path object")
        return {"otype": self.otype, "key": self.key}


@dataclass(kw_only=True)
class DataflowPayload(BaseClass):
    """Payload for Dataflow POST requests."""
    dataflow_objects: list[Dataflow] = field(default_factory=list)
    paths: list[list[list[DataflowPathObject]]] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.dataflow_objects, list):
            # init routine to support constructors with passed in object
            self.dataflow_objects = [
                Dataflow.from_api_response(value) if isinstance(value, dict)
                else value if isinstance(value, Dataflow)
                else (_ for _ in ()).throw(TypeError(f"Invalid type: {type(value)}"))
                for value in self.dataflow_objects
            ]

        if isinstance(self.paths, list):
            paths_out = []
            for path in self.paths:
                path_out = []
                if isinstance(path, list):
                    for segment in path:
                        if isinstance(segment, list):
                            segment_out = []
                            for obj in segment:
                                if isinstance(obj, dict):
                                    segment_out.append(DataflowPathObject.from_api_response(obj))
                                else:
                                    segment_out.append(obj)
                            path_out.append(segment_out)
                paths_out.append(path_out)
            self.paths = paths_out

    def generate_api_post_payload(self) -> dict:
        payload: dict = {}
        if self.dataflow_objects:
            validate_rest_payload(self.dataflow_objects, (Dataflow,))
            payload["dataflow_objects"] = [
                item.generate_api_post_payload() for item in self.dataflow_objects
            ]
        if self.paths:
            paths_payload = []
            for path in self.paths:
                path_payload = []
                for segment in path:
                    validate_rest_payload(segment, (DataflowPathObject,))
                    path_payload.append([obj.generate_api_payload() for obj in segment])
                paths_payload.append(path_payload)
            payload["paths"] = paths_payload
        return payload


@dataclass(kw_only=True)
class DataflowParams(BaseParams):
    """Query parameters for Dataflow GET requests."""
    keyField: str = field(default=None)

