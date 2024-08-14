"""Alation REST API Glossary Terms Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.glossary_term_model import GlossaryTerm, GlossaryTermItem, GlossaryTermParams
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationGlossaryTerm(AsyncHandler):
    """Alation REST API Glossary Term Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Glossary Term object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token, session, host)

    def get_glossary_terms(self, query_params: GlossaryTermParams = None) -> list:
        """Get the details of all Alation Glossary Terms.

        Args:
            query_params (GlossaryTermParams): REST API Get Filter Values.

        Returns:
            list: Alation Glossary Terms

        """
        validate_query_params(query_params, GlossaryTermParams)
        params = query_params.generate_params_dict() if query_params else None
        glossary_terms = self.get('/integration/v2/term/', query_params=params)

        if glossary_terms:
            return [GlossaryTerm.from_api_response(term) for term in glossary_terms]

    def post_glossary_terms(self, glossary_terms: list) -> list[JobDetailsDocumentPost]:
        """Post (Create) Alation Glossary Terms.

        Args:
            glossary_terms (list): Alation Glossary Terms to be created.
 
        Returns:
            List of JobDetailsDocumentPost: Status report of the executed background jobs.

        """
        item: GlossaryTermItem
        validate_rest_payload(
            payload = glossary_terms,
            expected_types = (GlossaryTermItem,)
        )
        payload = [item.generate_api_post_payload() for item in glossary_terms]

        async_results = self.async_post('/integration/v2/term/', payload)

        if async_results:
            return [JobDetailsDocumentPost.from_api_response(item) for item in async_results]

    def put_glossary_terms(self, glossary_terms: list) -> list[JobDetailsDocumentPut]:
        """Put (Update) Alation Glossary Terms.

        Args:
            glossary_terms (list): Alation Glossary Terms to be updated.

        Returns:
            List of JobDetailsDocumentPut: Status report of the executed background jobs.

        """
        item: GlossaryTermItem
        validate_rest_payload(glossary_terms, (GlossaryTerm, GlossaryTermItem))
        payload = [item.generate_api_put_payload() for item in glossary_terms]
        async_results = self.async_put('/integration/v2/term/', payload)

        if async_results:
            return [JobDetailsDocumentPut.from_api_response(item) for item in async_results]

    def delete_glossary_terms(self, glossary_terms: list) -> bool:
        """Delete Alation Glossary Terms.

        Args:
            glossary_terms (list): Alation Glossary Terms to be deleted.

        Returns:
            bool: Success of the API Delete Call.

        """
        item: GlossaryTerm
        validate_rest_payload(glossary_terms, (GlossaryTerm,))
        payload = {'id': [item.id for item in glossary_terms]}
        delete_result = self.delete('/integration/v2/term/', payload)

        return True if delete_result else False
