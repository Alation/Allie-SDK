"""Alation REST API Domains Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..models.custom_template_model import *
from ..core.custom_exceptions import *

LOGGER = logging.getLogger('allie_sdk_logger')

class AlationCustomTemplate(RequestHandler):
    """Alation REST API Domain Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Custom Template object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token = access_token)
        
    def get_custom_templates (self, query_params:CustomTemplateParams = None) -> list[CustomTemplate]:
        """Use the Custom Template API to retrieve details on all Custom Templates
        
        Args:
            query_params (CustomTemplateParams): REST API Custom Template Query Parameters.
 
        Returns:
            list[CustomTemplate]: List of Alation Custom Template objects
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, CustomTemplateParams)
        params = query_params.generate_params_dict() if query_params else None

        custom_templates = self.get(url = '/integration/v1/custom_template/', query_params = params)
        
        if custom_templates:
            custom_template_checked = [CustomTemplate.from_api_response(ct) for ct in custom_templates]
            return custom_template_checked
        return []
