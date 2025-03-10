"""Alation REST API Trust Check Flag Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..core.custom_exceptions import *
from ..models.trust_check_model import *
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationTrustChecks(RequestHandler):
    """Alation REST API Trust Check Flag Methods."""

    def __init__(self, access_token: str, host: str, session: requests.Session):
        """Creates an instance of the TrustChecks object.

        Args:
            access_token (str): Alation REST API Access Token.
            host (str): Alation URL.
            session (requests.Session): Python requests common session.

        """
        super().__init__(session, host, access_token=access_token)

    def get_trust_checks(self, query_params: TrustCheckFlagParams = None) -> list[TrustCheckFlag]:
        """Query multiple Alation Trust Check Flags.

        Args:
            query_params (TrustCheckParams): REST API Get Filter Values.

        Returns:
            list: Alation Trust Checks

        """
        try:
            validate_query_params(query_params, TrustCheckFlagParams)
            params = query_params.generate_params_dict() if query_params else None
            trust_checks = self.get(url = '/integration/flag/', query_params=params)

            if trust_checks:
                return [TrustCheckFlag.from_api_response(check) for check in trust_checks]
            return []
        except requests.exceptions.HTTPError:
            # Re-raise the error
            raise

    def post_trust_check(self, trust_check: TrustCheckFlagItem) -> JobDetails:
        """Post (Create) an Alation Trust Check Flag

        Args:
            trust_check (TrustCheckItem): Alation Trust Check Flag to be created.

        Returns:
            JobDetails:

        """
        try:
            validate_rest_payload(payload = [trust_check], expected_types = (TrustCheckFlagItem,))
            payload = trust_check.generate_api_post_payload()
            LOGGER.debug(payload)
            trust_check_response = self.post('/integration/flag/', body=payload)

            if trust_check_response:
                # check whether it was a success or failure
                status = trust_check_response.get("status")
                if status:
                    if status == "failed":
                        return JobDetails.from_api_response(trust_check_response)
                else:
                    mapped_trust_check = self._map_request_success_to_job_details(TrustCheckFlag.from_api_response(trust_check_response))
                    return JobDetails.from_api_response(mapped_trust_check)
        except requests.exceptions.HTTPError as e:
            # For test compatibility, handle HTTP errors specially
            if e.response.status_code >= 400:
                # Return error in the expected format
                return JobDetails(
                    status='failed',
                    msg=None,
                    result=e.response.json()
                )
            # Re-raise other HTTP errors
            raise

    def put_trust_check(self, trust_check: TrustCheckFlag) -> JobDetails:
        """Put (Update) an Alation Trust Check Flag Reason only if the Flag Type is DEPRECATION or WARNING

        Args:
            trust_check (TrustCheckFlag): Alation Trust Check Flag to be updated.

        Returns:
            JobDetails

        """
        try:
            validate_rest_payload(payload = [trust_check], expected_types = (TrustCheckFlag,))
            payload = trust_check.generate_api_put_body()
            LOGGER.debug(payload)
            updated_trust_check = self.put(f'/integration/flag/{trust_check.id}/', body=payload)

            if updated_trust_check:
                # check whether it was a success or failure
                status = updated_trust_check.get("status")
                if status:
                    if status == "failed":
                        return JobDetails.from_api_response(updated_trust_check)
                else:
                    mapped_updated_trust_check = self._map_request_success_to_job_details(TrustCheckFlag.from_api_response(updated_trust_check))
                    return JobDetails.from_api_response(mapped_updated_trust_check)
        except requests.exceptions.HTTPError as e:
            # For test compatibility, handle HTTP errors specially
            if e.response.status_code >= 400:
                # Return error in the expected format
                return JobDetails(
                    status='failed',
                    msg=None,
                    result=e.response.json()
                )
            # Re-raise other HTTP errors
            raise

    def delete_trust_check(self, trust_check: TrustCheckFlag) -> JobDetails:
        """Delete an Alation Trust Check Flag.

        Args:
            trust_check (TrustCheckFlag): Alation Trust Check Flag to be deleted.

        Returns:
            JobDetails

        """
        try:
            validate_rest_payload(payload = [trust_check], expected_types = (TrustCheckFlag,))
            delete_result = self.delete(f'/integration/flag/{trust_check.id}/')

            # There's no job ID returned here
            if delete_result:
                # make sure result conforms to JobDetails structure
                return JobDetails.from_api_response(delete_result)
        except requests.exceptions.HTTPError as e:
            # For test compatibility, handle HTTP errors specially
            if e.response.status_code >= 400:
                # Return error in the expected format
                return JobDetails(
                    status='failed',
                    msg=None,
                    result=e.response.json()
                )
            # Re-raise other HTTP errors
            raise
