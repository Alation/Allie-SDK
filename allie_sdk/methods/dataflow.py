import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.dataflow_model import Dataflow, DataflowPatchItem, DataflowPayload, DataflowParams
from ..models.job_model import JobDetails, JobDetailsDataflowPost, JobDetailsDataflowDelete

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationDataflow(AsyncHandler):
    """Alation REST API Dataflow Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Dataflow object."""
        super().__init__(session=session, host=host, access_token=access_token)

    def get_dataflows(
        self, object_ids: list[int | str] = None, query_params: DataflowParams = None
    ) -> DataflowPayload:
        """Retrieve dataflow objects and their paths."""
        validate_query_params(query_params, DataflowParams)
        if object_ids:
            validate_rest_payload(object_ids, (int, str))
        params = query_params.generate_params_dict() if query_params else None
        data = self.get(
            '/integration/v2/dataflow/',
            query_params=params,
            pagination=False,
            body=object_ids,
        )
        if data:
            return DataflowPayload.from_api_response(data)
        return DataflowPayload()

    def create_or_replace_dataflows(self, payload: DataflowPayload) -> list[JobDetailsDataflowPost]:
        """Create or replace dataflow objects with lineage paths."""
        if payload is None:
            return []
        validate_rest_payload([payload], (DataflowPayload,))
        payload_dict = payload.generate_api_post_payload()
        async_results = self.async_post_dict_payload('/integration/v2/dataflow/', payload_dict)
        if async_results:
            return [JobDetailsDataflowPost.from_api_response(item) for item in async_results]
        return []

    def update_dataflows(self, dataflows: list[DataflowPatchItem]) -> list[JobDetailsDataflowPost]:
        """Update multiple dataflow objects."""
        item: DataflowPatchItem
        validate_rest_payload(dataflows, (DataflowPatchItem,))
        payload = [item.generate_api_patch_payload() for item in dataflows]
        async_results = self.async_patch('/integration/v2/dataflow/', payload=payload)
        if async_results:
            # return [JobDetails.from_api_response(async_results['result']
            return [JobDetailsDataflowPost.from_api_response(item) for item in async_results]
        return []

    def delete_dataflows(
        self, object_ids: list[int | str], query_params: DataflowParams = None
    ) -> list[JobDetails]:
        """Delete multiple dataflow objects."""
        validate_query_params(query_params, DataflowParams)
        if not object_ids:
            return []
        validate_rest_payload(object_ids, (int, str))
        params = query_params.generate_params_dict() if query_params else None
        async_results = self.async_delete(
            '/integration/v2/dataflow/', payload=object_ids, query_params=params
        )
        if async_results:
            return [JobDetailsDataflowDelete.from_api_response(item) for item in async_results]
        return []

