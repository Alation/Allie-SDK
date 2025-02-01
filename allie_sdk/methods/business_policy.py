"""Alation REST API Policies Methods."""

import logging
import requests

# from ..core.request_handler import RequestHandler
from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import *
from ..models.business_policy_model import *
from ..models.custom_field_model import *
from ..models.custom_template_model import *
from ..models.job_model import *


LOGGER = logging.getLogger('allie_sdk_logger')

class AlationBusinessPolicy(AsyncHandler):
    """Alation REST API Business Policy Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Business Policy  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token = access_token)

    def get_business_policies(
            self
            , query_params:BusinessPolicyParams = None
    ) -> list[BusinessPolicy]:
        """Query multiple Alation Business Policies and return their details
        
        Args:
            query_params (BusinessPolicyParams): REST API Business Policy Query Parameters.
            
        Returns:
            list[BusinessPolicy]: Alation Business Policies
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, BusinessPolicyParams)
        params = query_params.generate_params_dict() if query_params else None

        business_policies = self.get('/integration/v1/business_policies/', query_params = params)

        if business_policies:
            business_policies_checked = [BusinessPolicy.from_api_response(business_policy) for business_policy in business_policies]
            return business_policies_checked
        return []


    def create_business_policies (
            self
            , business_policies: list[BusinessPolicyPostItem]
        ) -> list[JobDetails]:
        """Create Business Policies in Bulk
        
        Args:
            business_policies: list of Allie.BusinessPolicyPostItem objects. This is the main payload which has to conform to the payload outlined here:
            https://developer.alation.com/dev/reference/createpoliciesinbulk

        Returns:
            List of JobDetails: Status report of the executed background jobs.
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        # make sure input data matches expected structure
        item: BusinessPolicyPostItem
        validate_rest_payload(
            payload = business_policies,
            expected_types = (BusinessPolicyPostItem,)
        )
        # make sure we only include fields with values in the payload
        payload = [item.generate_api_post_payload() for item in business_policies]

        # The policy APIs returns a job id which needs to be used in conjunction with the Jobs ID to get the job details
        async_results = self.async_post(
            url = '/integration/v1/business_policies/'
            , payload = payload
        )

        return [JobDetails.from_api_response(item) for item in async_results]

    def update_business_policies (
            self
            , business_policies: list[BusinessPolicyPutItem]
        ) -> list[JobDetails]:
        """Bulk Update Business Policies in Bulk
        
        Args:
            business_policies: This is the main payload which has to conform to the payload outlined here: 
            https://developer.alation.com/dev/reference/updatepoliciesinbulk

        Returns:
            List of JobDetails: Status report of the executed background jobs.
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        # make sure input data matches expected structure
        item: BusinessPolicyPutItem
        validate_rest_payload(
            payload = business_policies,
            expected_types = (BusinessPolicyPutItem,)
        )
        # make sure we only include fields with values in the payload
        payload = [item.generate_api_put_payload() for item in business_policies]

        # The policy APIs returns a job id which needs to be used in conjunction with the Jobs ID to get the job details
        async_results = self.async_put(
            url = '/integration/v1/business_policies/'
            , payload = payload
        )

        return [JobDetails.from_api_response(item) for item in async_results]

         

    def delete_business_policies(
            self
            , business_policies:list[BusinessPolicy]
        )->JobDetails:
        """Bulk delete business policies

        Args:
            business_policies (list): List of BusinessPolicy objects to delete
            
        Returns:
            JobDetails: Status report of the executed delete operation.
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        item: BusinessPolicy
        validate_rest_payload(business_policies, (BusinessPolicy,))
        payload = {'ids': [item.id for item in business_policies]}
        
        delete_result = self.delete(
            url = '/integration/v1/business_policies/'
            , body = payload
        )

        # There's no job ID returned here - make result conform to JobDetails structure
        return JobDetails.from_api_response(delete_result)