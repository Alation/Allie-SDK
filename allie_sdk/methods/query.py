"""Alation REST API Query Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload, validate_query_params
from ..models.job_model import JobDetails
from ..models.query_model import Query, QueryItem, QueryParams

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationQuery(RequestHandler):
    """Interact with the Alation Query APIs."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Create an instance of the Query methods wrapper."""

        super().__init__(session=session, host=host, access_token=access_token)

    def create_query(self, query: QueryItem) -> Query:
        """Create a new query in Alation."""

        if not query:
            raise InvalidPostBody("Query payload is required for POST requests.")

        validate_rest_payload(payload=[query], expected_types=(QueryItem,))
        payload = query.generate_api_post_payload()

        query_response = self.post(
            url="/integration/v1/query/",
            body=payload,
        )

        if query_response:
            datasource_id = query_response.get("datasource_id")
            if datasource_id:
                result = JobDetails(
                    status = "successful"
                    , msg = ""
                    , result = Query.from_api_response(query_response)
                )
            else:
                result = JobDetails(
                    status="failed"
                    , msg=""
                    , result=query_response
                )
        else:
            result = JobDetails(
                status="failed"
                , msg=""
                , result=""
            )

        return result

    def get_queries(
        self
        , query_params: QueryParams = None
    ) -> list[Query]:
        """
        Get a queries based on certain search parameters

        Args:
            query_params (QueryParams): The query search parameters.

        Returns:
            Query: The Query object.
        """


        validate_query_params(query_params, QueryParams)
        params = query_params.generate_params_dict() if query_params else None

        queries = self.get(
            url=f"/integration/v1/query/",
            query_params = params
        )

        if queries:
            return [Query.from_api_response(query) for query in queries]

        return None

    def get_query(
        self
        , query_id: int
    ) -> Query:
        """
        Get a query by ID.

        Args:
            query_id (int): The ID of the query.

        Returns:
            Query: The Query object.
        """

        if query_id is None:
            raise InvalidPostBody("'query_id' must be provided to fetch query SQL text.")

        query = self.get(
            url=f"/integration/v1/query/{query_id}/"
        )

        if query:
            return Query.from_api_response(query)

        return None


    def get_query_sql(self, query_id: int) -> str:
        """
        Retrieve the saved SQL text for a query.

        Args:
            query_id (int): The ID of the query.

        Returns:
            str: The SQL text for the query.
        """

        if query_id is None:
            raise InvalidPostBody("'query_id' must be provided to fetch query SQL text.")

        sql_text = self.get(
            url=f"/integration/v1/query/{query_id}/sql/"
        )

        if isinstance(sql_text, bytes):
            return sql_text.decode("utf-8")

        return sql_text
