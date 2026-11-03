"""Alation AI API Data Product Methods."""

import logging
from math import isfinite
from time import monotonic, sleep
from typing import NoReturn

import requests

from ..core.custom_exceptions import (
    InvalidPostBody,
    UnsupportedPostBody,
    validate_query_params,
    validate_rest_payload,
)
from ..core.request_handler import RequestHandler
from ..models.alation_ai_data_product_model import (
    AlationAIAsyncTask,
    AlationAIDataProductJobResult,
    AlationAIDataProductTask,
    AlationAIExtractMetricsFromBIParams,
    AlationAIGenerateRelationshipsRequest,
    AlationAIGenerateRelationshipsResponse,
    AlationAIGetUpstreamTablesFromBiObjectParams,
    AlationAIGetUpstreamTablesFromBiObjectResponse,
    AlationAIMetricResultWithSource,
    AlationAIReviseDataProductJobsParams,
    AlationAIReviseDataProductRequest,
    AlationAIReviseDataProductResponse,
    AlationAIReviseDataProductResultDetail,
    AlationAIReviseDataProductResultsPage,
    AlationAISqlMetricResult,
    AlationAISqlWithValidation,
)
from ..models.authentication_model import AuthHeaderType
from ..models.job_model import JobDetails

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationAIDataProduct(RequestHandler):
    """Interact with the Alation AI API Data Product endpoints."""

    def __init__(
            self,
            access_token: str,
            session: requests.Session,
            host: str,
            auth_header_type: AuthHeaderType,
    ) -> None:
        """Create a data product API methods wrapper.

        Args:
            access_token (str): Alation REST API access token.
            session (requests.Session): Shared requests session used for API calls.
            host (str): Base Alation host URL.
            auth_header_type (AuthHeaderType): Authentication header used for API calls.

        Returns:
            None: Initializes the client's connection and authentication settings.
        """

        super().__init__(session=session, host=host, access_token=access_token, auth_header_type=auth_header_type)

    @staticmethod
    def _validate_identifier(value: str, field_name: str) -> None:
        """Validate that a required identifier value is present.

        Args:
            value (str): Identifier value supplied to the API method.
            field_name (str): Human-readable field name used in the error message.

        Returns:
            None: Returns without a value when the identifier is valid.

        Raises:
            InvalidPostBody: If the identifier is not a non-empty string or contains
                only whitespace.
        """

        if not isinstance(value, str) or not value.strip():
            error_message = f"'{field_name}' must be a non-empty string for the Data Product request."
            LOGGER.error(error_message)
            raise InvalidPostBody(error_message)

    @staticmethod
    def _validate_data_product_sql_statements(sql_statements: list[str]) -> None:
        """Validate SQL statements used by data product AI endpoints.

        Args:
            sql_statements (list[str]): SQL statements to validate before the request is sent.

        Returns:
            None: Returns without a value when a non-empty list of strings is supplied.

        Raises:
            InvalidPostBody: If no SQL statements are supplied.
            UnsupportedPostBody: If the payload is not a list or any SQL statement
                is not a string.
        """

        if sql_statements is not None and not isinstance(sql_statements, list):
            error_message = "'sql_statements' must be a list of SQL strings for the Data Product request."
            LOGGER.error(error_message)
            raise UnsupportedPostBody(error_message)
        if not sql_statements:
            error_message = "'sql_statements' must include at least one SQL statement for the Data Product request."
            LOGGER.error(error_message)
            raise InvalidPostBody(error_message)
        validate_rest_payload(sql_statements, (str,))

    @staticmethod
    def _raise_failed_data_product_job_result(task_id: str, job_result: AlationAIDataProductJobResult) -> NoReturn:
        """Raise an HTTP error for a failed data product creation result.

        Args:
            task_id (str): Identifier of the task that failed.
            job_result (AlationAIDataProductJobResult): Failed job result payload.

        Returns:
            NoReturn: Always raises an error containing the job failure details.

        Raises:
            requests.exceptions.HTTPError: Always raised with the job failure details.
        """

        error_message = f"Data product task '{task_id}' failed."
        if job_result.error:
            error_message = f"{error_message} {job_result.error}"

        LOGGER.error(error_message)
        error_response = requests.Response()
        error_response.status_code = 500
        error_response._content = error_message.encode("utf-8")
        raise requests.exceptions.HTTPError(error_message, response=error_response)

    def get_data_product_creation_result(
            self,
            task_id: str,
            poll_interval_seconds: float = 3,
            timeout_seconds: float | None = 300,
    ) -> str:
        """Poll a data product task until final YAML is available.

        Args:
            task_id (str): Identifier of the asynchronous task to poll.
            poll_interval_seconds (float): Number of seconds to wait between polling
                attempts. Must be finite and greater than or equal to zero.
            timeout_seconds (float | None): Maximum time to keep polling, in seconds.
                Defaults to 300. Must be finite and greater than zero, or None to
                disable the timeout. Checked between HTTP requests; an in-flight
                request is not interrupted.

        Returns:
            str: Final data product YAML returned by the completed task.

        Raises:
            InvalidPostBody: If the task ID, poll interval, or timeout is invalid.
            requests.exceptions.HTTPError: If the task reports failure or the API
                returns a non-success status code.
            TimeoutError: If the polling deadline is reached without a final result.
            ValueError: If the task returns an unexpected status.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/get_data_product_result#get-data-product-creation-result
        """

        self._validate_identifier(task_id, "task_id")
        if not isfinite(poll_interval_seconds) or poll_interval_seconds < 0:
            error_message = "'poll_interval_seconds' must be finite and greater than or equal to 0 for the Data Product request."
            LOGGER.error(error_message)
            raise InvalidPostBody(error_message)
        if timeout_seconds is not None and (not isfinite(timeout_seconds) or timeout_seconds <= 0):
            error_message = "'timeout_seconds' must be finite and greater than 0, or None, for the Data Product request."
            LOGGER.error(error_message)
            raise InvalidPostBody(error_message)

        deadline = monotonic() + timeout_seconds if timeout_seconds is not None else None
        attempt = 1
        while True:
            if deadline is not None and monotonic() >= deadline:
                error_message = f"Data product task '{task_id}' did not complete within {timeout_seconds} seconds."
                LOGGER.error(error_message)
                raise TimeoutError(error_message)

            LOGGER.info(f"Fetching data product task {task_id} (attempt {attempt}).")
            response = self.get(
                url=f"/ai/api/v1/data_product/get_data_product_result/{task_id}",
                pagination=False,
            )

            if not isinstance(response, dict):
                error_message = (
                    f"Data product task '{task_id}' returned unsupported response type "
                    f"'{type(response).__name__}' from '/ai/api/v1/data_product/get_data_product_result/{{task_id}}'."
                )
                LOGGER.error(error_message)
                raise ValueError(error_message)

            job_result = AlationAIDataProductJobResult.from_api_response(response)
            task_status = (job_result.status or "").lower()

            if task_status == "completed":
                if job_result.data is None:
                    error_message = (
                        f"Data product task '{task_id}' completed without returning YAML data."
                    )
                    LOGGER.error(error_message)
                    raise ValueError(error_message)

                LOGGER.info("Data product task %s completed and returned YAML.", task_id)
                return job_result.data

            if task_status == "failed":
                self._raise_failed_data_product_job_result(task_id, job_result)

            if task_status not in {"pending", "running"}:
                error_message = (
                    f"Data product task '{task_id}' returned unexpected status "
                    f"'{response.get('status')}'."
                )
                LOGGER.error(error_message)
                raise ValueError(error_message)

            sleep_seconds = poll_interval_seconds
            if deadline is not None:
                sleep_seconds = max(0, min(poll_interval_seconds, deadline - monotonic()))
            LOGGER.info(
                "Data product task %s is %s. Polling again in %s second(s).",
                task_id,
                task_status,
                sleep_seconds,
            )
            sleep(sleep_seconds)
            attempt += 1

    def generate_relationships(
        self,
        generate_relationships_request: AlationAIGenerateRelationshipsRequest,
    ) -> JobDetails:
        """Generate JOIN relationships for a data product specification.

        Args:
            generate_relationships_request (AlationAIGenerateRelationshipsRequest):
                Request payload containing the full data product YAML spec.

        Returns:
            JobDetails: Operation status with an AlationAIGenerateRelationshipsResponse
            in result. An empty response object is nested when the API response is
            empty.

        Raises:
            InvalidPostBody: If the request payload is missing.
            UnsupportedPostBody: If the request payload type is invalid.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/generate_relationships_endpoint
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

        relationships = AlationAIGenerateRelationshipsResponse.from_api_response(response) if response else AlationAIGenerateRelationshipsResponse()
        mapped_response = self._map_request_success_to_job_details(response_data=relationships)
        return JobDetails.from_api_response(mapped_response)

    def initiate_revise_data_product_workflow(
        self,
        data_product_id: str,
        revise_request: AlationAIReviseDataProductRequest = None,
    ) -> JobDetails:
        """Start a new "Suggest Fixes" workflow for a data product.

        Args:
            data_product_id (str): Identifier of the data product to revise.
            revise_request (AlationAIReviseDataProductRequest, optional): Additional
                revise workflow options. If omitted, default request settings are
                used.

        Returns:
            JobDetails: Operation status with an AlationAIReviseDataProductResponse
            describing the started revise workflow in result.

        Raises:
            InvalidPostBody: If the data product ID is missing.
            UnsupportedPostBody: If the revise request has an invalid type.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/initiate_revise_data_product
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

        revise_result = AlationAIReviseDataProductResponse.from_api_response(response)
        mapped_response = self._map_request_success_to_job_details(response_data=revise_result)
        return JobDetails.from_api_response(mapped_response)

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

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/get_all_revise_data_product_results
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

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/get_revise_data_product_result
        """

        self._validate_identifier(result_id, "result_id")

        LOGGER.info("Fetching revise data product result %s.", result_id)
        response = self.get(
            url=f"/ai/api/v1/data_product/revise_data_product_jobs/{result_id}",
            pagination=False,
        )

        return AlationAIReviseDataProductResultDetail.from_api_response(response)

    def validate_sql(
        self,
        data_product_id: str,
        sql_statements: list[str],
    ) -> JobDetails:
        """
        Validate SQL statements against a data product.
        Note: This function just validates the query syntactically, it doesn't check whether the columns
        or tables exist. Use extract_metrics_from_sql_statements instead if your goal is to check whether the
        columns or tables exist in the data product.

        Args:
            data_product_id (str): Identifier of the data product to validate
                against. This is required to detect the SQL dialect.
            sql_statements (list[str]): SQL statements to validate.

        Returns:
            JobDetails: Operation status with a list of AlationAISqlWithValidation
            objects in result. The result is an empty list when the API response is
            empty.

        Raises:
            InvalidPostBody: If the data product ID is missing or no SQL statements
                are provided.
            UnsupportedPostBody: If the payload is not a list or any SQL statement
                is not a string.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/validate_sql
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

        validation_results = [AlationAISqlWithValidation.from_api_response(item) for item in response] if response else []
        mapped_response = self._map_request_success_to_job_details(response_data=validation_results)
        return JobDetails.from_api_response(mapped_response)

    def extract_metrics_from_sql_statements(
        self,
        data_product_id: str,
        sql_statements: list[str],
    ) -> JobDetails:
        """Extract metrics from SQL statements for a data product.

        Note: This function also checks whether the columns or tables exist in the data product.

        Args:
            data_product_id (str): Identifier of the data product to analyze.
            sql_statements (list[str]): SQL statements from which metrics should be
                extracted.

        Returns:
            JobDetails: Operation status with an AlationAIDataProductTask in result
            containing the metrics extraction task ID.

        Raises:
            InvalidPostBody: If the data product ID is missing or no SQL statements
                are provided.
            UnsupportedPostBody: If the payload is not a list or any SQL statement
                is not a string.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/extract_metrics
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

        task = AlationAIDataProductTask.from_api_response(response)
        mapped_response = self._map_request_success_to_job_details(response_data=task)
        return JobDetails.from_api_response(mapped_response)

    def extract_data_product_metrics_from_sample_queries(
        self,
        data_product_id: str,
    ) -> JobDetails:
        """Start extracting metrics from a data product's sample queries.

        Args:
            data_product_id (str): Identifier of the data product to analyze.

        Returns:
            JobDetails: Operation status with an AlationAIDataProductTask in result
            containing the metrics extraction task ID.

        Raises:
            InvalidPostBody: If the data product ID is missing.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/extract_metrics_from_sample_queries
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

        task = AlationAIDataProductTask.from_api_response(response)
        mapped_response = self._map_request_success_to_job_details(response_data=task)
        return JobDetails.from_api_response(mapped_response)

    def extract_data_product_metrics_from_bi(
        self,
        data_product_id: str,
        query_params: AlationAIExtractMetricsFromBIParams = None,
    ) -> JobDetails:
        """Start extracting metrics from downstream BI assets.

        Args:
            data_product_id (str): Identifier of the data product to analyze.
            query_params (AlationAIExtractMetricsFromBIParams, optional): Filters or
                options for selecting BI assets to analyze.

        Returns:
            JobDetails: Operation status with an AlationAIDataProductTask in result
            containing the BI metrics extraction task ID.

        Raises:
            InvalidPostBody: If the data product ID is missing.
            UnsupportedQueryParams: If the query parameter type is invalid.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/extract_metrics_from_bi
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

        task = AlationAIDataProductTask.from_api_response(response)
        mapped_response = self._map_request_success_to_job_details(response_data=task)
        return JobDetails.from_api_response(mapped_response)

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

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/get_metrics
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

        Documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/get_metrics_with_source
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

        Documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/get_tables_from_bi
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
    ) -> JobDetails:
        """Create a data product or preview its specification from a BI source.

        Args:
            datasource_id (int): Identifier of the BI datasource to analyze.
            create_product (bool): Whether to create the data product immediately. If
                set to ``False``, the API returns a preview specification instead.

        Returns:
            JobDetails: Operation status with the API response payload for the
            created data product or generated specification preview in result.

        Raises:
            InvalidPostBody: If the datasource ID is missing.
            requests.exceptions.HTTPError: If the API returns a non-success status
                code.

        Official documentation: https://documentation.alation.com/api-reference/alation-cloud-service-latest/alation-ai-api/data-product/create_data_product_from_bi_datasource
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

        mapped_response = self._map_request_success_to_job_details(response_data=response)
        return JobDetails.from_api_response(mapped_response)
