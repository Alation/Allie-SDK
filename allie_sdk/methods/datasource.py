import logging
import requests

# from ..core.request_handler import RequestHandler
from ..core.request_handler import RequestHandler
from ..core.custom_exceptions import *
from ..models.datasource_model import (
    OCFDatasource,
    OCFDatasourceGetParams,
    OCFDatasourceParams,
    OCFDatasourcePostItem,
    OCFDatasourcePutItem,
    NativeDatasource,
    NativeDatasourceParams,
)
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')

class AlationDatasource(RequestHandler):
    """Alation REST API Datasource Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Documents  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token=access_token)

    def get_ocf_datasources(self, query_params:OCFDatasourceParams = None) -> list[OCFDatasource]:
        """Query multiple Alation datasources and return their details
        
        Args:
            query_params (OCFDatasourceParams): REST API Datasources Query Parameters.
            
        Returns:
            list[OCFDatasource]: Alation Datasources
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, OCFDatasourceParams)
        params = query_params.generate_params_dict() if query_params else None

        datasources = self.get(url = '/integration/v2/datasource/', query_params = params)

        if datasources:
            datasources_checked = [OCFDatasource.from_api_response(datasource) for datasource in datasources]
            return datasources_checked
        return []

    def get_native_datasources(self, query_params:NativeDatasourceParams = None) -> list[NativeDatasource]:
        """Query multiple Alation datasources and return their details
        
        Args:
            query_params (NativeDatasourceParams): REST API Datasources Query Parameters.
            
        Returns:
            list[NativeDatasource]: Alation NativeDatasources
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, NativeDatasourceParams)
        params = query_params.generate_params_dict() if query_params else None

        datasources = self.get(url = '/integration/v1/datasource/', query_params = params)

        if datasources:
            datasources_checked = [NativeDatasource.from_api_response(datasource) for datasource in datasources]
            return datasources_checked
        return []

    def create_ocf_datasource(self, datasource: OCFDatasourcePostItem) -> OCFDatasource:
        """Create a new OCF datasource."""

        if not datasource:
            raise InvalidPostBody("Datasource payload is required for POST requests.")

        validate_rest_payload(payload=[datasource], expected_types=(OCFDatasourcePostItem,))
        payload = datasource.generate_post_payload()

        datasource_response = self.post(
            url='/integration/v2/datasource/',
            body=payload,
        )

        return OCFDatasource.from_api_response(datasource_response)

    def get_ocf_datasource_by_id(
        self,
        datasource_id: int,
        query_params: OCFDatasourceGetParams = None,
    ) -> OCFDatasource:
        """Retrieve a specific OCF datasource."""

        if datasource_id is None:
            raise InvalidPostBody("'datasource_id' must be provided to retrieve a datasource.")

        validate_query_params(query_params, OCFDatasourceGetParams)
        params = query_params.generate_params_dict() if query_params else None

        datasource = self.get(
            url=f'/integration/v2/datasource/{datasource_id}/',
            query_params=params,
            pagination=False,
        )

        return OCFDatasource.from_api_response(datasource)

    def update_ocf_datasource(
        self,
        datasource_id: int,
        datasource: OCFDatasourcePutItem,
    ) -> OCFDatasource:
        """Update an existing OCF datasource."""

        if datasource_id is None:
            raise InvalidPostBody("'datasource_id' must be provided to update a datasource.")

        if not datasource:
            raise InvalidPostBody("Datasource payload is required for PUT requests.")

        validate_rest_payload(payload=[datasource], expected_types=(OCFDatasourcePutItem,))
        payload = datasource.generate_put_payload()

        datasource_response = self.put(
            url=f'/integration/v2/datasource/{datasource_id}/',
            body=payload,
        )

        return OCFDatasource.from_api_response(datasource_response)

    def delete_ocf_datasource(self, datasource_id: int) -> JobDetails:
        # The original Alation API call doesn't return anything on success
        """Delete an OCF datasource."""

        if datasource_id is None:
            raise InvalidPostBody("'datasource_id' must be provided to delete a datasource.")

        datasource_response = self.delete(
            url = f'/integration/v2/datasource/{datasource_id}/',
            is_async = False,
        )

        if isinstance(datasource_response, dict):
            return JobDetails.from_api_response(datasource_response)

