"""Alation REST API Virtual Data Source Methods."""

import logging
import requests

from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.virtual_datasource_model import *
from ..core.async_handler import AsyncHandler
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationVirtualDataSource(AsyncHandler):
    """Alation REST API Virtual DS."""

    def __init__(self, access_token: str, session: requests.Session,
                 host: str):
        """Creates an instance of the User object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
            use_v2_endpoint (bool): Use the Alation REST API V2 User Endpoint.

        """
        super().__init__(access_token, session, host)

        self._vds_endpoint = '/api/v1/bulk_metadata/extraction/'

    def post_metadata(
            self
            , ds_id: int
            , vds_objects: list
            , query_params: VirtualDataSourceParams = None
    ) -> list[JobDetailsVirtualDatasourcePost]:
        """Post (Create/Update/Delete) Alation Virtual Data source objects

        Args:
            ds_id: (int): Virtual Data Source ID for the metadata objects
            vds_objects (AlationVirtualDataSourceItem): A list of Alation virtual data source objects to
                    be added/updated or deleted.
            query_params: (VirtualDataSourceParams): a VirtualDataSourceParams object
                    query_params.set_title_descs = "true" - use to enable Title and Description updates
                    query_params.remove_not_seen = "false" - set to true to remove the metadata objects that are not
                                                            specified in the list of vds objects (delete)

        Returns:
            List of JobDetailsVirtualDatasourcePost: Status report of the executed background jobs.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, VirtualDataSourceParams)
        params = query_params.generate_params_dict() if query_params else None
        validate_rest_payload(
            vds_objects
            , expected_types = (
                VirtualDataSourceSchema
                , VirtualDataSourceTable
                , VirtualDataSourceView
                , VirtualDataSourceColumn
                , VirtualDataSourceIndex
            )
        )

        item: VirtualDataSourceItem
        payload_d = [item.generate_api_post_payload() for item in vds_objects]
        # add line feeds between json payload dicts for jsonl format
        payload_jsonl = '\n'.join(json.dumps(p) for p in payload_d)
        LOGGER.debug(payload_jsonl)
        async_results = self.async_post_data_payload(f'{self._vds_endpoint}{ds_id}',
                                                    data=payload_jsonl, query_params=params)

        return [JobDetailsVirtualDatasourcePost.from_api_response(item) for item in async_results]

    def post_metadata_jsonl(
            self
            , ds_id: int
            , payload: str
            , query_params: VirtualDataSourceParams = None
    ) -> list[JobDetailsVirtualDatasourcePost]:
        """Post (Create/Update/Delete) Alation Virtual Data source objects

        Args:
            ds_id: (int): Virtual Data Source ID for the metadata objects
            payload (str): A list of Alation virtual data source object definitions as a jsonl payload
            query_params: (VirtualDataSourceParams): a VirtualDataSourceParams object
                    query_params.set_title_descs = "true" - use to enable Title and Description updates
                    query_params.remove_not_seen = "false" - set to true to remove the metadata objects that are not
                                                            specified in the list of vds objects (delete)

        Returns:
            List of JobDetailsVirtualDatasourcePost: Status report of the executed background jobs.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, VirtualDataSourceParams)
        params = query_params.generate_params_dict() if query_params else None
        async_results = self.async_post_data_payload(f'{self._vds_endpoint}{ds_id}', data=payload, query_params=params)

        return [JobDetailsVirtualDatasourcePost.from_api_response(item) for item in async_results]

@property
def vds_endpoint(self) -> str:
    """Return the Bool Config to use the Alation REST API Virtual Data Source Endpoint.

    Returns:
        bool: Config to use the Alation REST API Virtual DataSource Endpoint.

    """
    return self._vds_endpoint


@vds_endpoint.setter
def vds_endpoint(self, vds_endpoint_val: str):
    """Return the Bool Config to use the Alation REST API Virtual Data Source Endpoint.

    Returns:
        bool: Config to use the Alation REST API Virtual DataSource Endpoint.

    """
    self._vds_endpoint = vds_endpoint_val

