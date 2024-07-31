"""Alation REST API Data Quality Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.data_quality_model import  *
from ..models.job_model import *

LOGGER = logging.getLogger()


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

    def get_data_quality_fields(self, query_params: DataQualityFieldParams = None) -> list:
        """Query multiple Alation Data Quality Fields.

        Args:
             query_params (DataQualityFieldParams): REST API Get Filter Values.

        Returns:
            list: Alation Data Quality Fields

        """
        validate_query_params(query_params, DataQualityFieldParams)
        params = query_params.generate_params_dict() if query_params else None
        dq_fields = self.get('/integration/v1/data_quality/fields/', query_params=params)

        if dq_fields:
            return [DataQualityField.from_api_response(item) for item in dq_fields]

    def post_data_quality_fields(self, dq_fields: list) -> list:
        """Post (Create) Alation Data Quality Fields.

        Args:
            dq_fields (list): Alation Data Quality Fields to be created.

        Returns:
            list: execution results

        """
        item: DataQualityFieldItem
        validate_rest_payload(dq_fields, (DataQualityFieldItem,))
        payload = [item.generate_api_post_payload() for item in dq_fields]
        async_results = self._dq_post(payload, 'Fields')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def delete_data_quality_fields(self, dq_fields: list) -> list:
        """Delete Alation Data Quality Fields.

        Args:
            dq_fields (list): Alation Data Quality Fields to be deleted.

        Returns:
            list: execution results

        """
        item: DataQualityField
        validate_rest_payload(dq_fields, (DataQualityField,))
        payload = [item.key for item in dq_fields]
        async_results = self._dq_delete(payload, 'Fields')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def get_data_quality_values(self, query_params: DataQualityValueParams = None) -> list:
        """Query multiple Alation Data Quality Values.

        Args:
            query_params (DataQualityValueParams): REST API Get Filter Values.

        Returns:
            list: DataQualityValue Values

        """
        validate_query_params(query_params, DataQualityValueParams)
        params = query_params.generate_params_dict() if query_params else None
        dq_values = self.get('/integration/v1/data_quality/values/', query_params=params)

        if dq_values:
            return [DataQualityValue.from_api_response(value) for value in dq_values]

    def post_data_quality_values(self, dq_values: list) -> list:
        """Post (Create) Alation Data Quality Values.

        Args:
            dq_values (list): Alation Data Quality Values to be created.

        Returns:
            list: execution results

        """
        item: DataQualityValueItem
        validate_rest_payload(dq_values, (DataQualityValueItem,))
        payload = [item.generate_api_post_payload() for item in dq_values]
        async_results = self._dq_post(payload, 'Values')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def delete_data_quality_values(self, dq_values: list) -> list:
        """Delete Alation Data Quality Values.

        Args:
            dq_values (list): Alation Data Quality Values to be deleted.

        Returns:
            list: execution results

        """
        item: DataQualityValue
        validate_rest_payload(dq_values, (DataQualityValue,))
        payload = [item.generate_api_delete_payload() for item in dq_values]
        async_results = self._dq_delete(payload, 'Values')

        if async_results:
            return [JobDetailsDataQuality.from_api_response(item) for item in async_results]

    def _dq_post(self, dq_payload: list, dq_type: str) -> list:
        """Post (Create) the DQ Fields or Values in Alation.

        Args:
            dq_payload (list): DQ Items to be Created.
            dq_type (str): 'Fields' or 'Values'.

        Returns:
            list: execution results

        """
        results = []
        batches = self._batch_objects(dq_payload)

        for batch in batches:
            try:
                dq_batch = {dq_type.lower(): batch}
                async_result = self.async_post_dict_payload('/integration/v1/data_quality/', dq_batch)
                if async_result:
                    results.extend(async_result)
            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                results.append(batch_error)

        return results

    def _dq_delete(self, dq_payload: list, dq_type: str) -> bool:
        """Delete the DQ Fields or Values in Alation.

        Args:
            dq_payload (list): DQ Items to be Deleted.
            dq_type (str): 'Fields' or 'Values'.

        Returns:
            bool: Returns True if a batch fails

        """
        results = []
        batches = self._batch_objects(dq_payload)

        for batch in batches:
            try:
                dq_batch = {dq_type.lower(): batch}
                async_result = self.async_delete_dict_payload('/integration/v1/data_quality/', dq_batch)
                if async_result:
                    results.extend(async_result)
            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                results.append(batch_error)

        return results