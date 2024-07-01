"""Alation REST API Domain Methods."""

import logging
import requests


from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.domain_model import Domain, DomainMembership, DomainParams
from .job import AlationJob

LOGGER = logging.getLogger()


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

        """
        validate_query_params(query_params, DomainParams)
        params = query_params.generate_params_dict() if query_params else None
        domains = self.get(
            url = '/integration/v2/domain/'
            , query_params = params
        )

        if domains:
            return [Domain.from_api_response(domain) for domain in domains]

    def assign_objects_to_domain(
        self
        , domain_membership: DomainMembership
    ) -> DomainMembership:
        """
        Assign objects to Alation Domain.

        Args:
            domain_membership: Alation DomainMembership object

        Other useful info:
            If there are less than a 1000 objects to assign to a given domain, this job will be
            executed synchronously, otherwise asynchronously. This threshold can also be configured
            via alation.domains.bulk_membership.sync_job_max_batch_size in the backend.
            For more info see: https://developer.alation.com/dev/reference/postdomainmembership

        """

        if domain_membership:
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
                job.check_job_status()
                j = job._get_job()
                return j
                # job_status = j.get('status')
                # if job_status == 'successful':
            else:
                return results

