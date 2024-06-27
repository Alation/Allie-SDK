import logging
import requests

# from ..core.request_handler import RequestHandler
from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import *
from ..models.datasource_model import *

LOGGER = logging.getLogger()

class AlationDatasource(AsyncHandler):
    """Alation REST API Documents Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Documents  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token=access_token)

    def get_ocf_datasources(self, query_params:OCFDatasourceParams = None) -> list:
        """Query multiple Alation datasources and return their details
        Args:
            query_params (DatasourcesParams): REST API Datasources Query Parameters.
        Returns:
            list: Alation Datasources
        """

        validate_query_params(query_params, OCFDatasourceParams)
        params = query_params.generate_params_dict() if query_params else None

        datasources = self.get(url = '/integration/v2/datasource/', query_params = params)

        if datasources:
            datasources_checked = [OCFDatasource.from_api_response(datasource) for datasource in datasources]
            return datasources_checked

    def get_native_datasources(self, query_params:NativeDatasourceParams = None) -> list:
        """Query multiple Alation datasources and return their details
        Args:
            query_params (NativeDatasourcesParams): REST API Datasources Query Parameters.
        Returns:
            list: Alation NativeDatasources
        """

        validate_query_params(query_params, NativeDatasourceParams)
        params = query_params.generate_params_dict() if query_params else None

        datasources = self.get(url = '/integration/v1/datasource/', query_params = params)

        if datasources:
            datasources_checked = [NativeDatasource.from_api_response(datasource) for datasource in datasources]
            return datasources_checked