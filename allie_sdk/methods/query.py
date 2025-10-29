"""Alation REST API Query Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from ..models.query_model import Query, QueryCreateRequest

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationQuery(RequestHandler):
    """Interact with the Alation Query APIs."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Create an instance of the Query methods wrapper."""

        super().__init__(session=session, host=host, access_token=access_token)

    def create_query(self, query: QueryCreateRequest) -> Query:
        """Create a new query in Alation."""

        if not query:
            raise InvalidPostBody("Query payload is required for POST requests.")

        validate_rest_payload(payload=[query], expected_types=(QueryCreateRequest,))
        payload = query.generate_api_post_payload()

        query_response = self.post(
            url="/integration/v1/query/",
            body=payload,
        )

        return Query.from_api_response(query_response)

    def get_query_sql(self, query_id: int) -> str:
        """Retrieve the saved SQL text for a query."""

        if query_id is None:
            raise InvalidPostBody("'query_id' must be provided to fetch query SQL text.")

        sql_text = self.get(
            url=f"/integration/v1/query/{query_id}/sql/",
            pagination=False,
        )

        if isinstance(sql_text, bytes):
            return sql_text.decode("utf-8")

        return sql_text
