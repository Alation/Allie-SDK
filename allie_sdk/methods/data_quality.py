"""Alation REST API Data Quality Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.data_quality_model import  *
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationDataQuality(AsyncHandler):
    """Alation REST API Data Quality Methods."""

    def __init__(self, access_token: str, host: str, session: requests.Session):
        """Creates an instance of the DataQuality object.

        Args:
            access_token (str): Alation REST API Access Token.
            host (str): Alation URL.
            session (requests.Session): Python requests common session.

        """
        super().__init__(access_token, session, host)

    def get_data_quality_fields(self, query_params: DataQualityFieldParams = None) -> list[DataQualityField]:
        """Query multiple Alation Data Quality Fields.

        Args:
             query_params (DataQualityFieldParams): REST API Get Filter Values.

        Returns:
            list: Alation Data Quality Fields

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, DataQualityFieldParams)
        params = query_params.generate_params_dict() if query_params else None
        
        dq_fields = self.get(
            url = '/integration/v1/data_quality/fields/'
            , query_params=params
        )
        return [DataQualityField.from_api_response(item) for item in dq_fields]

    def post_data_quality_fields(self, dq_fields: list) -> list[JobDetailsDataQuality]:
        """Post (Create) Alation Data Quality Fields.

        Args:
            dq_fields (list): Alation Data Quality Fields to be created.

        Returns:
            list: execution results

        """
        item: DataQualityFieldItem
        validate_rest_payload(dq_fields, expected_types = (DataQualityFieldItem,))
        payload = [item.generate_api_post_payload() for item in dq_fields]
        async_results = self._dq_post(payload, dq_type = 'Fields')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def delete_data_quality_fields(self, dq_fields: list) -> list[JobDetailsDataQuality]:
        """Delete Alation Data Quality Fields.

        Args:
            dq_fields (list): Alation Data Quality Fields to be deleted.

        Returns:
            list: execution results

        """
        item: DataQualityField
        validate_rest_payload(dq_fields, expected_types = (DataQualityField,))
        payload = [item.key for item in dq_fields]
        async_results = self._dq_delete(payload, dq_type ='Fields')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def get_data_quality_values(self, query_params: DataQualityValueParams = None) -> list[DataQualityValue]:
        """Query multiple Alation Data Quality Values.

        Args:
            query_params (DataQualityValueParams): REST API Get Filter Values.

        Returns:
            list: DataQualityValue Values

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, DataQualityValueParams)
        params = query_params.generate_params_dict() if query_params else None
        
        dq_values = self.get('/integration/v1/data_quality/values/', query_params=params)
        
        if dq_values:
            return [DataQualityValue.from_api_response(value) for value in dq_values]
        # adding below lines as a temporary solution to this issue
        # https://github.com/Alation/Allie-SDK/issues/36
        return []

    def post_data_quality_values(self, dq_values: list) -> list:
        """Post (Create) Alation Data Quality Values.

        Args:
            dq_values (list): Alation Data Quality Values to be created.

        Returns:
            list: execution results

        """
        item: DataQualityValueItem
        validate_rest_payload(dq_values, expected_types = (DataQualityValueItem,))
        payload = [item.generate_api_post_payload() for item in dq_values]
        async_results = self._dq_post(payload, dq_type = 'Values')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def delete_data_quality_values(self, dq_values: list) -> list[JobDetailsDataQuality]:
        """Delete Alation Data Quality Values.

        Args:
            dq_values (list): Alation Data Quality Values to be deleted.

        Returns:
            list: execution results

        """
        item: DataQualityValue
        validate_rest_payload(dq_values, expected_types = (DataQualityValue,))
        payload = [item.generate_api_delete_payload() for item in dq_values]
        async_results = self._dq_delete(payload, dq_type = 'Values')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def _dq_post(self, dq_payload: list, dq_type: str) -> list:
        """Post (Create) the DQ Fields or Values in Alation.

        Args:
            dq_payload (list): DQ Items to be Created.
            dq_type (str): 'Fields' or 'Values'.

        Returns:
            list: execution results

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        results = []
        batches = self._batch_objects(dq_payload)

        for batch in batches:
            dq_batch = {dq_type.lower(): batch}
            async_result = self.async_post_dict_payload(
                url = '/integration/v1/data_quality/'
                , payload = dq_batch
            )
            if async_result:
                results.extend(async_result)

        return results

    def _dq_delete(self, dq_payload: list, dq_type: str) -> list:
        """Delete the DQ Fields or Values in Alation.

        Args:
            dq_payload (list): DQ Items to be Deleted.
            dq_type (str): 'Fields' or 'Values'.

        Returns:
            list: execution results

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        results = []
        batches = self._batch_objects(dq_payload)

        for batch in batches:
            """
            The payload has to be a dict: 
            - The first property/key is either `fields` or `values`. 
            - And the value of this key is a list of the actual field or value dictionaries.
            
            Example: 
            
            {
                'values': 
                    [
                        {'field_key': 'sdk-test-1', 'object_key': '1.public.parts'}
                        , {'field_key': 'sdk-test-2', 'object_key': '1.public.sales'}
                    ]
            }
            """
            dq_batch = {
                dq_type.lower(): batch
            }

            async_result = self.async_delete_dict_payload(
                url = '/integration/v1/data_quality/'
                , payload = dq_batch
            )
            if async_result:
                results.extend(async_result)

        return results