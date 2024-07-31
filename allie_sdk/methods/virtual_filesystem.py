"""Alation REST API Virtual File System Methods."""

import logging
import requests

from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.virtual_filesystem_model import *
from ..core.async_handler import AsyncHandler
from ..models.job_model import *

LOGGER = logging.getLogger()


class AlationVirtualFileSystem(AsyncHandler):
    """Alation REST API Virtual FS."""

    def __init__(self, access_token: str, session: requests.Session,
                 host: str):
        """Creates an instance of the User object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token, session, host)

        self._vfs_endpoint = '/api/v1/bulk_metadata/file_upload/'

    def post_metadata(self, fs_id: int, vfs_objects: list) -> list[JobDetails]:
        """Post (Create/Update/Delete) Alation Virtual Data source objects

        Args:
            fs_id: (int): Virtual Data Source ID for the metadata objects
            vfs_objects: [AlationVirtualFileSystemItem]: A list of Alation virtual file system objects to
                    be added/updated or deleted.

        Returns:
            List of JobDetails: Status report of the executed background jobs.

        """

        # allow a list object for empty payloads
        validate_rest_payload(vfs_objects, (VirtualFileSystemItem, list))
        item: VirtualFileSystemItem
        payload_d = [item.generate_api_post_payload() for item in vfs_objects]
        # add line feeds between json payload dicts for jsonl format
        # add a preceding \n to force an empty payload if vds_objects is empty for delete operations
        payload_jsonl = '\n' + '\n'.join(json.dumps(p) for p in payload_d)

        LOGGER.debug(payload_jsonl)
        async_results = self.async_post(f'{self._vfs_endpoint}{fs_id}/', payload=payload_jsonl)

        if async_results:
            return [JobDetails.from_api_response(item) for item in async_results]

    def post_metadata_jsonl(self, fs_id: int, payload: str) -> list[JobDetails]:
        """Post (Create/Update/Delets) Alation Virtual Data source objects

        Args:
            fs_id: (int): Virtual File System ID for the metadata objects
            payload (str): A list of Alation virtual file system object definitions as a jsonl payload

        Returns:
            List of JobDetails: Status report of the executed background jobs.
        """

        # validate_query_params(query_params, VirtualDataSourceParams)
        # params = query_params.generate_params_dict() if query_params else None
        async_results = self.async_post(f'{self._vfs_endpoint}{fs_id}', data=payload)

        if async_results:
            return [JobDetails.from_api_response(item) for item in async_results]

@property
def vfs_endpoint(self) -> str:
    """Return the Bool Config to use the Alation REST API Virtual Data Source Endpoint.

    Returns:
        bool: Config to use the Alation REST API Virtual DataSource Endpoint.

    """
    return self._vfs_endpoint


@vfs_endpoint.setter
def vfs_endpoint(self, vfs_endpoint_val: str):
    """Return the Bool Config to use the Alation REST API Virtual Data Source Endpoint.

    Returns:
        bool: Config to use the Alation REST API Virtual DataSource Endpoint.

    """
    self._vfs_endpoint = vfs_endpoint_val

