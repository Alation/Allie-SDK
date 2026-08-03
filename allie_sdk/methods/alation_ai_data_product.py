"""Alation AI API Data Product Methods."""

import logging
from time import sleep

import requests

from ..core.custom_exceptions import (
    InvalidPostBody,
    validate_query_params,
    validate_rest_payload,
)
from ..core.request_handler import RequestHandler
from ..models.alation_ai_data_product_model import (
    AlationAIDataProductCreationInfo,
    AlationAIDataProductTask,
    AlationAIExtractMetricsFromBIParams,
    AlationAIGenerateRelationshipsRequest,
    AlationAIGenerateRelationshipsResponse,
    AlationAIGetUpstreamTablesFromBiObjectParams,
    AlationAIMetricResultWithSource,
    AlationAIReviseDataProductJobsParams,
    AlationAIReviseDataProductRequest,
    AlationAIReviseDataProductResponse,
    AlationAIReviseDataProductResultDetail,
    AlationAIReviseDataProductResultsPage,
    AlationAISqlMetricResult,
    AlationAISqlWithValidation,
    AlationAIAsyncTask,
    AlationAIGetUpstreamTablesFromBiObjectResponse,
)

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationAIDataProduct(RequestHandler):
    """Interact with the Alation AI API Data Product endpoints."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Create a data product API methods wrapper.

        Args:
            access_token (str): Alation REST API access token.
            session (requests.Session): Shared requests session used for API calls.
            host (str): Base Alation host URL.
        """

        super().__init__(session=session, host=host, access_token=access_token)

    @staticmethod
    def _validate_identifier(value: str, field_name: str):
        """Validate that a required identifier value is present.

        Args:
            value (str): Identifier value supplied to the API method.
            field_name (str): Human-readable field name used in the error message.

        Raises:
            InvalidPostBody: If the identifier value is missing.
        """

        if value is None:
            raise InvalidPostBody(f"'{field_name}' must be provided for the Data Product request.")

    @staticmethod
    def _validate_data_product_sql_statements(sql_statements: list[str]):
        """Validate SQL statements used by data product AI endpoints.

        Args:
            sql_statements (list[str]): SQL statements to validate before the request is sent.

        Raises:
            InvalidPostBody: If no SQL statements are supplied.
            UnsupportedPostBody: If any SQL statement is not a string.
        """

        if not sql_statements:
            raise InvalidPostBody(
                "'sql_statements' must include at least one SQL statement for the Data Product request."
            )
        validate_rest_payload(sql_statements, (str,))

    @staticmethod
    def _raise_failed_data_product_task(task: AlationAIAsyncTask):
        """Raise an HTTP error for a failed asynchronous data product task.

        Args:
            task (AlationAIAsyncTask): Failed task returned by the Alation AI API.

        Raises:
            requests.exceptions.HTTPError: Always raised with the task failure details.
        """

        error_message = f"Data product task '{task.id}' failed."
        if task.context:
            for key in ("error", "message", "detail", "details"):
                value = task.context.get(key)
                if value:
                    error_message = f"{error_message} {value}"
                    break

        LOGGER.error(error_message)
        error_response = requests.Response()
        error_response.status_code = 500
        error_response._content = error_message.encode("utf-8")
        raise requests.exceptions.HTTPError(error_message, response=error_response)

    def enrich_data_product_spec(
        self,
        alation_ai_data_product: AlationAIDataProductCreationInfo,
        generate_missing_descriptions: bool = True,
        generate_relationships: bool = True,
    ) -> AlationAIDataProductTask:
        """Generate an enriched data product specification from metadata.

        This endpoint builds YAML for a data product based on the supplied table and
        column metadata. It does not create a data product in the Data Products
        Service catalog.

        Args:
            alation_ai_data_product (AlationAIDataProductCreationInfo): Metadata used
                to build the data product specification.
            generate_missing_descriptions (bool): Whether Alation AI should generate
                descriptions for objects that do not already have them.
            generate_relationships (bool): Whether Alation AI should infer
                relationships between the supplied objects.

        Returns:
            AlationAIDataProductTask: Asynchronous task details for the spec
            enrichment job.

        Raises:
            InvalidPostBody: If the payload is missing.
            UnsupportedPostBody: If the payload type is invalid.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        if not alation_ai_data_product:
            raise InvalidPostBody("Data Product payload is required for POST requests.")

        validate_rest_payload(
            payload=[alation_ai_data_product],
            expected_types=(AlationAIDataProductCreationInfo,),
        )
        payload = alation_ai_data_product.generate_api_post_payload()

        LOGGER.info(
            "Creating data product with %s table definition(s).",
            len(alation_ai_data_product.table_column_info_list),
        )
        response = self.put(
            url="/ai/api/v1/data_product/enrich_data_product_spec",
            body=payload,
            query_params={
                "generate_missing_descriptions": generate_missing_descriptions,
                "generate_relationships": generate_relationships,
            },
        )

        return AlationAIDataProductTask.from_api_response(response)

    def get_data_product_task(self, task_id: str, poll_interval_seconds: float = 3) -> str:
        """Poll a data product task until final YAML is available.

        Args:
            task_id (str): Identifier of the asynchronous task to poll.
            poll_interval_seconds (float): Number of seconds to wait between polling
                attempts. Must be greater than or equal to zero.

        Returns:
            str: Final data product YAML returned by the completed task.

        Raises:
            InvalidPostBody: If the task ID is missing or the poll interval is
                negative.
            requests.exceptions.HTTPError: If the task reports failure or the API
                returns a non-success status code.
            ValueError: If the task returns an unexpected status.
        """

        self._validate_identifier(task_id, "task_id")
        if poll_interval_seconds < 0:
            raise InvalidPostBody(
                "'poll_interval_seconds' must be greater than or equal to 0 for the Data Product request."
            )

        attempt = 1
        while True:
            LOGGER.info("Fetching data product task %s (attempt %s).", task_id, attempt)
            response = self.get(
                url=f"/ai/api/v1/data_product/get_data_product_result/{task_id}",
                pagination=False,
            )

            if not isinstance(response, dict):
                LOGGER.info("Data product task %s completed and returned YAML.", task_id)
                return response

            task = AlationAIAsyncTask.from_api_response(response)
            task_status = (task.status or "").lower()

            if task_status == "failed":
                self._raise_failed_data_product_task(task)

            if task_status not in {"pending", "running"}:
                error_message = (
                    f"Data product task '{task_id}' returned unexpected status '{task.status}'."
                )
                LOGGER.error(error_message)
                raise ValueError(error_message)

            LOGGER.info(
                "Data product task %s is %s. Polling again in %s second(s).",
                task_id,
                task_status,
                poll_interval_seconds,
            )
            sleep(poll_interval_seconds)
            attempt += 1

    def generate_relationships(
        self,
        generate_relationships_request: AlationAIGenerateRelationshipsRequest,
    ) -> AlationAIGenerateRelationshipsResponse:
        """Generate JOIN relationships for a data product specification.

        Args:
            generate_relationships_request (AlationAIGenerateRelationshipsRequest):
                Request payload containing the full data product YAML spec.

        Returns:
            AlationAIGenerateRelationshipsResponse: Generated relationships returned
            by the Alation AI API. An empty response object is returned when the API
            response is empty.

        Raises:
            InvalidPostBody: If the request payload is missing.
            UnsupportedPostBody: If the request payload type is invalid.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        if not generate_relationships_request:
            raise InvalidPostBody("Generate Relationships payload is required for POST requests.")

        validate_rest_payload(
            payload=[generate_relationships_request],
            expected_types=(AlationAIGenerateRelationshipsRequest,),
        )
        payload = generate_relationships_request.generate_api_post_payload()

        LOGGER.info("Generating relationships for a data product specification.")
        response = self.post(
            url="/ai/api/v1/data_product/generate_relationships",
            body=payload,
        )

        if response:
            return AlationAIGenerateRelationshipsResponse.from_api_response(response)
        return AlationAIGenerateRelationshipsResponse()

    def revise_data_product(
        self,
        data_product_id: str,
        revise_request: AlationAIReviseDataProductRequest = None,
    ) -> AlationAIReviseDataProductResponse:
        """Start a new "Suggest Fixes" workflow for a data product.

        Args:
            data_product_id (str): Identifier of the data product to revise.
            revise_request (AlationAIReviseDataProductRequest, optional): Additional
                revise workflow options. If omitted, default request settings are
                used.

        Returns:
            AlationAIReviseDataProductResponse: Response describing the started revise
            workflow.

        Raises:
            InvalidPostBody: If the data product ID is missing.
            UnsupportedPostBody: If the revise request has an invalid type.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(data_product_id, "alation_ai_data_product_id")

        if revise_request is None:
            revise_request = AlationAIReviseDataProductRequest()

        validate_rest_payload(payload=[revise_request], expected_types=(AlationAIReviseDataProductRequest,))
        payload = revise_request.generate_api_post_payload()

        LOGGER.info(
            "Starting revise data product workflow for %s.",
            data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{data_product_id}/revise_data_product",
            body=payload,
        )

        return AlationAIReviseDataProductResponse.from_api_response(response)

    def get_data_product_revision_jobs(
        self,
        query_params: AlationAIReviseDataProductJobsParams = None,
    ) -> AlationAIReviseDataProductResultsPage:
        """Retrieve revise data product jobs.

        Running jobs are included by default, and the results can optionally be
        filtered by data product through the query parameters.

        Args:
            query_params (AlationAIReviseDataProductJobsParams, optional): Filters for
                the revise job search.

        Returns:
            AlationAIReviseDataProductResultsPage: Paginated revise job results. An
            empty page object is returned when the API response is empty.

        Raises:
            UnsupportedQueryParams: If the query parameter type is invalid.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        validate_query_params(query_params, AlationAIReviseDataProductJobsParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Fetching revise data product jobs.")
        response = self.get(
            url="/ai/api/v1/data_product/revise_data_product_jobs",
            query_params=params,
            pagination=False,
        )

        if response:
            return AlationAIReviseDataProductResultsPage.from_api_response(response)
        return AlationAIReviseDataProductResultsPage()

    def get_data_product_revision_result(
        self,
        result_id: str,
    ) -> AlationAIReviseDataProductResultDetail:
        """Fetch a single revise data product result.

        Args:
            result_id (str): Identifier of the revise workflow result to retrieve.

        Returns:
            AlationAIReviseDataProductResultDetail: Current status and any available
            result details for the revise workflow.

        Raises:
            InvalidPostBody: If the result ID is missing.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(result_id, "result_id")

        LOGGER.info("Fetching revise data product result %s.", result_id)
        response = self.get(
            url=f"/ai/api/v1/data_product/revise_data_product_jobs/{result_id}",
            pagination=False,
        )

        return AlationAIReviseDataProductResultDetail.from_api_response(response)

    def validate_sql_against_data_product(
        self,
        data_product_id: str,
        sql_statements: list[str],
    ) -> list[AlationAISqlWithValidation]:
        """Validate SQL statements against a data product.

        Args:
            data_product_id (str): Identifier of the data product to validate
                against.
            sql_statements (list[str]): SQL statements to validate.

        Returns:
            list[AlationAISqlWithValidation]: Validation results for each SQL
            statement. Returns an empty list when the API response is empty.

        Raises:
            InvalidPostBody: If the data product ID is missing or no SQL statements
                are provided.
            UnsupportedPostBody: If any SQL statement is not a string.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(data_product_id, "alation_ai_data_product_id")
        self._validate_data_product_sql_statements(sql_statements)

        LOGGER.info(
            "Validating %s SQL statement(s) against data product %s.",
            len(sql_statements),
            data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{data_product_id}/validate_sql",
            body=sql_statements,
        )

        if response:
            return [AlationAISqlWithValidation.from_api_response(item) for item in response]
        return []

    def extract_data_product_metrics(
        self,
        data_product_id: str,
        sql_statements: list[str],
    ) -> AlationAIDataProductTask:
        """Start extracting metrics from SQL statements for a data product.

        Args:
            data_product_id (str): Identifier of the data product to analyze.
            sql_statements (list[str]): SQL statements from which metrics should be
                extracted.

        Returns:
            AlationAIDataProductTask: Asynchronous task details for the metrics
            extraction job.

        Raises:
            InvalidPostBody: If the data product ID is missing or no SQL statements
                are provided.
            UnsupportedPostBody: If any SQL statement is not a string.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(data_product_id, "alation_ai_data_product_id")
        self._validate_data_product_sql_statements(sql_statements)

        LOGGER.info(
            "Extracting metrics from %s SQL statement(s) for data product %s.",
            len(sql_statements),
            data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{data_product_id}/extract_metrics",
            body=sql_statements,
        )

        return AlationAIDataProductTask.from_api_response(response)

    def extract_data_product_metrics_from_sample_queries(
        self,
        data_product_id: str,
    ) -> AlationAIDataProductTask:
        """Start extracting metrics from a data product's sample queries.

        Args:
            data_product_id (str): Identifier of the data product to analyze.

        Returns:
            AlationAIDataProductTask: Asynchronous task details for the metrics
            extraction job.

        Raises:
            InvalidPostBody: If the data product ID is missing.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(data_product_id, "alation_ai_data_product_id")

        LOGGER.info(
            "Extracting metrics from sample queries for data product %s.",
            data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{data_product_id}/extract_metrics_from_sample_queries",
            body=None,
        )

        return AlationAIDataProductTask.from_api_response(response)

    def extract_data_product_metrics_from_bi(
        self,
        data_product_id: str,
        query_params: AlationAIExtractMetricsFromBIParams = None,
    ) -> AlationAIDataProductTask:
        """Start extracting metrics from downstream BI assets.

        Args:
            data_product_id (str): Identifier of the data product to analyze.
            query_params (AlationAIExtractMetricsFromBIParams, optional): Filters or
                options for selecting BI assets to analyze.

        Returns:
            AlationAIDataProductTask: Asynchronous task details for the BI metrics
            extraction job.

        Raises:
            InvalidPostBody: If the data product ID is missing.
            UnsupportedQueryParams: If the query parameter type is invalid.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(data_product_id, "alation_ai_data_product_id")
        validate_query_params(query_params, AlationAIExtractMetricsFromBIParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Extracting BI metrics for data product %s.", data_product_id)
        response = self.post(
            url=f"/ai/api/v1/data_product/{data_product_id}/extract_metrics_from_bi",
            body=None,
            query_params=params,
        )

        return AlationAIDataProductTask.from_api_response(response)

    def get_data_product_metrics_extraction_result(self, task_id: str) -> AlationAIAsyncTask | list[AlationAISqlMetricResult]:
        """Retrieve the current state or final result of a metrics extraction task.

        Args:
            task_id (str): Identifier of the metrics extraction task.

        Returns:
            AlationAIAsyncTask | list[AlationAISqlMetricResult]: The in-progress task
            details when the job is still running, or the extracted metric results
            when the job has completed. Returns an empty list when the API response is
            empty.

        Raises:
            InvalidPostBody: If the task ID is missing.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(task_id, "task_id")

        LOGGER.info("Fetching metric extraction task %s.", task_id)
        response = self.get(
            url=f"/ai/api/v1/data_product/get_metrics/{task_id}",
            pagination=False,
        )

        if isinstance(response, dict):
            return AlationAIAsyncTask.from_api_response(response)
        if response:
            return [AlationAISqlMetricResult.from_api_response(item) for item in response]
        return []

    def get_data_product_metrics_extraction_result_with_source(self, task_id: str) -> AlationAIAsyncTask | list[AlationAIMetricResultWithSource]:
        """Retrieve metrics extraction results including source metadata.

        Args:
            task_id (str): Identifier of the metrics extraction task.

        Returns:
            AlationAIAsyncTask | list[AlationAIMetricResultWithSource]: The
            in-progress task details when the job is still running, or the extracted
            metrics with source metadata when the job has completed. Returns an empty
            list when the API response is empty.

        Raises:
            InvalidPostBody: If the task ID is missing.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        self._validate_identifier(task_id, "task_id")

        LOGGER.info("Fetching metric extraction with source task %s.", task_id)
        response = self.get(
            url=f"/ai/api/v1/data_product/get_metrics_with_source/{task_id}",
            pagination=False,
        )

        if isinstance(response, dict):
            return AlationAIAsyncTask.from_api_response(response)
        if response:
            return [AlationAIMetricResultWithSource.from_api_response(item) for item in response]
        return []

    def get_upstream_tables_from_bi_object(self, query_params: AlationAIGetUpstreamTablesFromBiObjectParams) -> AlationAIGetUpstreamTablesFromBiObjectResponse:
        """Resolve upstream tables for a BI object.

        Args:
            query_params (AlationAIGetUpstreamTablesFromBiObjectParams): BI object
                identifier and type used to resolve upstream tables.

        Returns:
            AlationAIGetUpstreamTablesFromBiObjectResponse: Upstream table resolution
            results. An empty response object is returned when the API response is
            empty.

        Raises:
            InvalidPostBody: If the query parameters are missing.
            UnsupportedQueryParams: If the query parameter type is invalid.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        if not query_params:
            raise InvalidPostBody("Get Tables From BI query params are required.")

        validate_query_params(query_params, AlationAIGetUpstreamTablesFromBiObjectParams)
        params = query_params.generate_params_dict()

        LOGGER.info("Fetching upstream tables for BI object %s:%s.", query_params.type, query_params.id)
        response = self.get(
            url="/ai/api/v1/data_product/get_tables_from_bi",
            query_params=params,
            pagination=False,
        )

        if response:
            return AlationAIGetUpstreamTablesFromBiObjectResponse.from_api_response(response)
        return AlationAIGetUpstreamTablesFromBiObjectResponse()

    def create_data_product_from_bi_source(
        self,
        datasource_id: int,
        create_product: bool = True,
    ) -> str:
        """Create a data product or preview its specification from a BI source.

        Args:
            datasource_id (int): Identifier of the BI datasource to analyze.
            create_product (bool): Whether to create the data product immediately. If
                set to ``False``, the API returns a preview specification instead.

        Returns:
            str: API response payload for the created data product or generated
            specification preview.

        Raises:
            InvalidPostBody: If the datasource ID is missing.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.
        """

        if datasource_id is None:
            raise InvalidPostBody(
                "'datasource_id' must be provided to create a data product from a BI datasource."
            )

        LOGGER.info(
            "Creating data product from BI datasource %s with create_product=%s.",
            datasource_id,
            create_product,
        )
        response = self.post(
            url="/ai/api/v1/data_product/create_from_bi_datasource",
            body=None,
            query_params={
                "datasource_id": datasource_id,
                "create_product": create_product,
            },
        )

        return response
