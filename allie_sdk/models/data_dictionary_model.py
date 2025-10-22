"""Alation REST API Data Dictionary Data Models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO, IOBase
from pathlib import Path
from typing import BinaryIO, Iterable

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass


DEFAULT_UPLOAD_FILENAME = "data_dictionary.csv"


@dataclass(kw_only=True)
class DataDictionaryAsyncTaskLink(BaseClass):
    """Represents a hyperlink associated with an asynchronous task."""

    rel: str = field(default=None)
    href: str = field(default=None)

"""
The Policy endpoint uses quite a similar structure, just that instead
of ts_created ts_started is used. This is the main reason why we didn't generalise
this one here.
"""
@dataclass(kw_only=True)
class DataDictionaryAsyncTask(BaseClass):
    """Represents an asynchronous task registered by Alation."""

    id: str = field(default=None)
    type: str = field(default=None)
    state: str = field(default=None)
    ts_created: datetime = field(default=None)
    links: list[DataDictionaryAsyncTaskLink] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)

        if self.links:
            self.links = [
                DataDictionaryAsyncTaskLink.from_api_response(link)
                if isinstance(link, dict)
                else link
                for link in self.links
            ]

@dataclass(kw_only=True)
class DataDictionaryAsyncTaskDetails(BaseClass):
    """Container model for asynchronous task details."""

    task: DataDictionaryAsyncTask = field(default=None)

    def __post_init__(self):
        if isinstance(self.task, dict):
            self.task = DataDictionaryAsyncTask.from_api_response(self.task)


@dataclass(kw_only=True)
class DataDictionaryTaskProgress(BaseClass):
    """Represents the progress metadata of a data dictionary upload task."""

    total_batches: int = field(default=None)
    batches_completed: int = field(default=None)


@dataclass(kw_only=True)
class DataDictionaryTaskRecords(BaseClass):
    """Represents record counts in a data dictionary upload task."""

    total: int = field(default=None)
    succeeded: int = field(default=None)
    failed: int = field(default=None)


@dataclass(kw_only=True)
class DataDictionaryTaskResult(BaseClass):
    """Represents the result metadata of a data dictionary upload task."""

    records: DataDictionaryTaskRecords = field(default=None)

    def __post_init__(self):
        if isinstance(self.records, dict):
            self.records = DataDictionaryTaskRecords.from_api_response(self.records)


@dataclass(kw_only=True)
class DataDictionaryResource(BaseClass):
    """Represents the catalog resource affected by a data dictionary task."""

    id: str = field(default=None)
    oid: int | str = field(default=None)
    otype: str = field(default=None)
    user_id: int = field(default=None)


@dataclass(kw_only=True)
class DataDictionaryTaskDetails(BaseClass):
    """Detailed response describing a data dictionary upload task."""

    id: str = field(default=None)
    type: str = field(default=None)
    state: str = field(default=None)
    status: str = field(default=None)
    progress: DataDictionaryTaskProgress = field(default=None)
    result: DataDictionaryTaskResult = field(default=None)
    ts_created: datetime = field(default=None)
    ts_updated: datetime = field(default=None)
    ts_completed: datetime = field(default=None)
    dd_resource: DataDictionaryResource = field(default=None)
    report_download_link: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.progress, dict):
            self.progress = DataDictionaryTaskProgress.from_api_response(self.progress)

        if isinstance(self.result, dict):
            self.result = DataDictionaryTaskResult.from_api_response(self.result)

        if isinstance(self.dd_resource, dict):
            self.dd_resource = DataDictionaryResource.from_api_response(self.dd_resource)

        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)

        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)

        if isinstance(self.ts_completed, str):
            self.ts_completed = self.convert_timestamp(self.ts_completed)


@dataclass(kw_only=True)
class DataDictionaryTaskErrorRangeEndpoint(BaseClass):
    """Represents the start or end location of a failing data dictionary record."""

    index: int = field(default=None)
    key: str = field(default=None)


@dataclass(kw_only=True)
class DataDictionaryTaskErrorRange(BaseClass):
    """Represents the range of records affected by a particular error."""

    start: DataDictionaryTaskErrorRangeEndpoint = field(default=None)
    end: DataDictionaryTaskErrorRangeEndpoint = field(default=None)
    start_inclusive: bool = field(default=None)
    end_inclusive: bool = field(default=None)

    def __post_init__(self):
        if isinstance(self.start, dict):
            self.start = DataDictionaryTaskErrorRangeEndpoint.from_api_response(self.start)

        if isinstance(self.end, dict):
            self.end = DataDictionaryTaskErrorRangeEndpoint.from_api_response(self.end)


@dataclass(kw_only=True)
class DataDictionaryTaskErrorDetailItems(BaseClass):
    """Represents the failing items included in a task error."""

    range: DataDictionaryTaskErrorRange = field(default=None)
    total: int = field(default=None)

    def __post_init__(self):
        if isinstance(self.range, dict):
            self.range = DataDictionaryTaskErrorRange.from_api_response(self.range)


@dataclass(kw_only=True)
class DataDictionaryTaskErrorDetails(BaseClass):
    """Represents additional details for a data dictionary task error."""

    items: DataDictionaryTaskErrorDetailItems = field(default=None)
    error: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.items, dict):
            self.items = DataDictionaryTaskErrorDetailItems.from_api_response(self.items)


@dataclass(kw_only=True)
class DataDictionaryTaskError(BaseClass):
    """Represents a single error reported for a data dictionary task."""

    timestamp: datetime = field(default=None)
    name: str = field(default=None)
    fatal: bool = field(default=None)
    error_message: str = field(default=None)
    original_error_message: str = field(default=None)
    details: DataDictionaryTaskErrorDetails = field(default=None)
    category: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = self.convert_timestamp(self.timestamp)

        if isinstance(self.details, dict):
            self.details = DataDictionaryTaskErrorDetails.from_api_response(self.details)


@dataclass
class DataDictionaryItem:
    """Represents the payload for uploading a data dictionary file."""

    overwrite_values: bool
    file: str | Path | bytes | BinaryIO
    allow_reset: bool = field(default=None)
    file_name: str = field(default=None)
    content_type: str = field(default="text/csv")

    def __post_init__(self):
        if not isinstance(self.overwrite_values, bool):
            raise InvalidPostBody("'overwrite_values' must be a boolean value.")

        if self.allow_reset is not None and not isinstance(self.allow_reset, bool):
            raise InvalidPostBody("'allow_reset' must be a boolean value when provided.")

        if isinstance(self.file_name, str) and not self.file_name.strip():
            raise InvalidPostBody("'file_name' cannot be an empty string.")

        if self.content_type and not isinstance(self.content_type, str):
            raise InvalidPostBody("'content_type' must be a string value when provided.")

    def _normalize_file_name(self, candidate: str | None) -> str:
        if candidate and candidate.strip():
            return candidate
        return DEFAULT_UPLOAD_FILENAME

    def _prepare_file(self) -> tuple[str, BinaryIO, bool]:
        """Prepare the file tuple for a multipart request."""

        file_obj: BinaryIO | None = None
        close_after_use = False
        file_name = self._normalize_file_name(self.file_name)

        if isinstance(self.file, (str, Path)):
            path = Path(self.file)
            if not path.exists():
                raise InvalidPostBody(
                    f"The file '{path}' does not exist. Provide a valid data dictionary file."
                )
            file_obj = path.open("rb")
            close_after_use = True
            file_name = self._normalize_file_name(self.file_name or path.name)
        elif isinstance(self.file, bytes):
            file_obj = BytesIO(self.file)
            close_after_use = True
        elif isinstance(self.file, IOBase) or hasattr(self.file, "read"):
            file_obj = self.file  # type: ignore[assignment]
            derived_name = getattr(self.file, "name", None)
            if derived_name:
                file_name = self._normalize_file_name(self.file_name or derived_name)
        else:
            raise InvalidPostBody(
                "'file' must be a path, bytes, or a file-like object providing a 'read' method."
            )

        if not file_name:
            file_name = DEFAULT_UPLOAD_FILENAME

        # Ensure BytesIO objects use a sensible name for downstream logging/debugging
        if isinstance(file_obj, BytesIO) and not getattr(file_obj, "name", None):
            file_obj.name = file_name

        return file_name, file_obj, close_after_use  # type: ignore[return-value]

    def generate_multipart_payload(
        self,
    ) -> tuple[dict[str, str], dict[str, tuple[str, BinaryIO, str]], Iterable[IOBase]]:
        """Generate the multipart payload for the upload request."""

        file_name, file_obj, close_after_use = self._prepare_file()

        data = {"overwrite_values": str(self.overwrite_values).lower()}

        if self.allow_reset is not None:
            data["allow_reset"] = str(self.allow_reset).lower()

        content_type = self.content_type or "application/octet-stream"
        files = {"file": (file_name, file_obj, content_type)}

        closeables: list[IOBase] = []
        if close_after_use and isinstance(file_obj, IOBase):
            closeables.append(file_obj)

        return data, files, closeables
