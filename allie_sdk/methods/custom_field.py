"""Alation REST API Custom Field Methods."""

import logging
import requests
import urllib.parse

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.custom_field_model import *
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationCustomField(AsyncHandler):
    """Alation REST API Custom Field Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the CustomField object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token, session, host)

        self.access_token = access_token
        self.host = host
        self.session = session

    def get_custom_fields(self, query_params: CustomFieldParams = None) -> list:
        """Get the details of all Alation Custom Fields.

        Args:
            query_params (CustomFieldParams): REST API Get Filter Values.

        Returns:
            list: Alation Custom Fields

        """
        validate_query_params(query_params, CustomFieldParams)
        params = query_params.generate_params_dict() if query_params else None
        custom_fields = self.get('/integration/v2/custom_field/', query_params=params)

        if custom_fields:
            return [CustomField.from_api_response(custom_field) for custom_field in custom_fields]

    def get_custom_field_values(self, query_params: CustomFieldValueParams = None) -> list:
        """Get the details of all Alation Custom Field Values.

        Args:
            query_params (CustomFieldValueParams): REST  API Get Filter Values.

        Returns:
            list: Alation Custom Field Values.

        """
        validate_query_params(query_params, CustomFieldValueParams)
        params = query_params.generate_params_dict() if query_params else None
        custom_field_values = self.get('/integration/v2/custom_field_value/', query_params=params)

        if custom_field_values:
            return [CustomFieldValue.from_api_response(value) for value in custom_field_values]

    def get_a_builtin_custom_field(self, field_name: str) -> CustomField:
        """Get the details of a Builtin Alation Custom Field.

        Args:
            field_name (str): Name of the Builtin Custom Field.

        Returns:
            CustomField: Alation Custom Field.

        """
        url_parsed_name = urllib.parse.quote(field_name)
        builtin_details = self.get(f'/integration/v2/custom_field/builtin/{url_parsed_name}/')

        if builtin_details:
            return CustomField.from_api_response(builtin_details)

    def get_a_custom_field(self, field_id: int) -> CustomField:
        """Get the details of an Alation Custom Field.

        Args:
            field_id (int): ID of the Alation Custom Field.

        Returns:
            CustomField: Alation Custom Field.

        """
        field_details = self.get(f'/integration/v2/custom_field/{field_id}/')

        if field_details:
            return CustomField.from_api_response(field_details)

    def post_custom_fields(self, custom_fields: list[CustomFieldItem]) -> list[JobDetailsCustomFieldPost]:
        """Post (Create) Alation Custom Fields.

        Args:
            custom_fields (list): Alation Custom Fields to be created.

        Returns:
            List of JobDetailsCustomFieldPost: Status report of the executed background jobs.

        """
        item: CustomFieldItem
        validate_rest_payload(custom_fields, (CustomFieldItem,))
        payload = [item.generate_api_post_payload() for item in custom_fields]
        async_results = self.async_post('/integration/v2/custom_field/', payload)

        if async_results:
            return [JobDetailsCustomFieldPost.from_api_response(item) for item in async_results]

    def put_custom_field_values(self, custom_field_values: list[CustomFieldValueItem], batch_size: int = 10000) -> list[JobDetails]:
        """Put (Update) Alation Custom Field Values.

        Args:
            custom_field_values (list): Alation Custom Field Values to be updated.
            batch_size (int): REST API PUT Body Size Limit.

        Returns:
             List of JobDetails: Status report of the executed background jobs.

        """
        item: CustomFieldValueItem
        validate_rest_payload(custom_field_values, (CustomFieldValueItem, CustomFieldValue))
        payload = [item.generate_api_put_payload() for item in custom_field_values]
        async_results = self.async_put('/integration/v2/custom_field_value/async/', payload, batch_size)

        if async_results:
            return [JobDetails.from_api_response(item) for item in async_results]
