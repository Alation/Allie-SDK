"""Alation REST API Domain Methods."""

import logging
import requests


from ..core.request_handler import RequestHandler
from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.domain_model import (
    Domain,
    DomainMembership,
    DomainMembershipRule,
    DomainMembershipRuleRequest,
    DomainParams,
)
from ..models.job_model import JobDetails
from .job import AlationJob

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationDomain(AsyncHandler):
    """Alation REST API Glossary Term Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Glossary Term object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(session = session, host = host, access_token = access_token)

    def get_domains(
        self
        , query_params: DomainParams = None
    ) -> list[Domain]:
        """Get the details of all Alation Domain.

        Args:
            query_params (DomainParams): REST API Get Filter Values.

        Returns:
            list: Alation Domain

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, DomainParams)
        params = query_params.generate_params_dict() if query_params else None
        domains = self.get(
            url = '/integration/v2/domain/'
            , query_params = params
        )

        if domains:
            return [Domain.from_api_response(domain) for domain in domains]
        return []

    def assign_objects_to_domain(
        self
        , domain_membership: DomainMembership
    ) -> list[JobDetails]:
        """
        Assign objects to Alation Domain.

        Args:
            domain_membership: Alation DomainMembership object

        Returns:
            list[JobDetails]: Status report of the executed job.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.

        Other useful info:
            If there are less than a 1000 objects to assign to a given domain, this job will be
            executed synchronously, otherwise asynchronously. This threshold can also be configured
            via alation.domains.bulk_membership.sync_job_max_batch_size in the backend.
            For more info see: https://developer.alation.com/dev/reference/postdomainmembership
        """
        if not domain_membership:
            return []
            
        # make sure input data matches expected structure
        validate_rest_payload(payload = [domain_membership], expected_types = (DomainMembership,))

        # make sure we only include fields with values in the payload
        payload = domain_membership.generate_api_post_payload()

        results = self.post(
            url='/integration/v2/domain/membership/'
            , body = payload
        )

        # check if we get a job id back
        job_id = results.get('job_id')

        if job_id:
            job = AlationJob(self.access_token, self.session, self.host, results)
            job_details = job.check_job_status()
            # job_details example value:
            # [{'msg': 'Job finished in 0.033747 seconds at 2024-10-29 17:17:51.842614+00:00', 'result': None, 'status': 'successful'}]

            return [JobDetails.from_api_response(item) for item in job_details]

            # TODO: Do we have to implement batching here as well?
            # Created issue for this: https://github.com/Alation/Allie-SDK/issues/38

        else:
            # if an error is returned the dict will include a status property
            status = results.get("status")
            if status:
                return [JobDetails.from_api_response(results)]
            else:
                return [
                    JobDetails(
                        status = "successful"
                        , msg = ""
                        , result = None
                    )
                ]

    def get_domain_membership_rules(
        self,
        rules_request: DomainMembershipRuleRequest,
    ) -> list[DomainMembershipRule]:
        """Retrieve membership rules applied to the requested domains."""

        if not rules_request:
            return []

        validate_rest_payload(
            payload=[rules_request],
            expected_types=(DomainMembershipRuleRequest,),
        )

        payload = rules_request.generate_api_post_payload()

        response = self.post(
            url='/integration/v2/domain/membership/view_rules/',
            body=payload
        )

        def _map_rules(items: list) -> list[DomainMembershipRule]:
            return [DomainMembershipRule.from_api_response(item) for item in items]

        if isinstance(response, list):
            return _map_rules(response)

        return []

