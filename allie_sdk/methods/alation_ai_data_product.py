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
    AlationAIDataProductToUpdate,
    AlationAIExtractMetricsFromBIParams,
    AlationAIGetTablesFromBIParams,
    AlationAIMetricResultWithSource,
    AlationAIReviseDataProductJobsParams,
    AlationAIReviseDataProductRequest,
    AlationAIReviseDataProductResponse,
    AlationAIReviseDataProductResultDetail,
    AlationAIReviseDataProductResultsPage,
    AlationAISqlMetricResult,
    AlationAISqlWithValidation,
    AlationAIAsyncTask,
    AlationAIUpstreamTablesResponse,
)

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationAIDataProduct(RequestHandler):
    """Interact with the Alation AI API Data Product endpoints."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Create an instance of the Data Product methods wrapper."""

        super().__init__(session=session, host=host, access_token=access_token)

    @staticmethod
    def _validate_identifier(value: str, field_name: str):
        """Validate that a required path identifier has been supplied."""

        if value is None:
            raise InvalidPostBody(f"'{field_name}' must be provided for the Data Product request.")

    @staticmethod
    def _validate_data_product_sql_statements(sql_statements: list[str]):
        """Validate SQL statement payloads used by the Data Product AI endpoints."""

        if not sql_statements:
            raise InvalidPostBody(
                "'sql_statements' must include at least one SQL statement for the Data Product request."
            )
        validate_rest_payload(sql_statements, (str,))

    @staticmethod
    def _raise_failed_data_product_task(task: AlationAIAsyncTask):
        """Raise an HTTP error when the data product async task reports failure."""

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

    def create_data_product(
        self,
        alation_ai_data_product: AlationAIDataProductCreationInfo,
        generate_missing_descriptions: bool = True,
        generate_relationships: bool = True,
    ) -> AlationAIDataProductTask:
        """Create a data product from table and column metadata."""

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
        response = self.post(
            url="/ai/api/v1/data_product/create_data_product",
            body=payload,
            query_params={
                "generate_missing_descriptions": generate_missing_descriptions,
                "generate_relationships": generate_relationships,
            },
        )

        return AlationAIDataProductTask.from_api_response(response)

    def get_data_product_task(self, task_id: str, poll_interval_seconds: float = 3) -> str:
        """Poll a data product task until it returns final YAML or fails."""

        self._validate_identifier(task_id, "task_id")
        if poll_interval_seconds < 0:
            raise InvalidPostBody(
                "'poll_interval_seconds' must be greater than or equal to 0 for the Data Product request."
            )

        attempt = 1
        while True:
            LOGGER.info("Fetching data product task %s (attempt %s).", task_id, attempt)
            response = self.get(
                url=f"/ai/api/v1/data_product/get_data_product/{task_id}",
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

    def update_data_product_description(
        self,
        alation_ai_data_product: AlationAIDataProductToUpdate,
    ) -> str:
        """Update an existing data product description from YAML."""

        if not alation_ai_data_product:
            raise InvalidPostBody("Data Product payload is required for PUT requests.")

        validate_rest_payload(
            payload=[alation_ai_data_product],
            expected_types=(AlationAIDataProductToUpdate,),
        )
        payload = alation_ai_data_product.generate_api_put_payload()

        LOGGER.info("Updating data product description.")
        response = self.put(
            url="/ai/api/v1/data_product/update_data_product_description",
            body=payload,
        )

        return response

    def revise_data_product(
        self,
        alation_ai_data_product_id: str,
        revise_request: AlationAIReviseDataProductRequest = None,
    ) -> AlationAIReviseDataProductResponse:
        """Start a revise data product workflow."""

        self._validate_identifier(alation_ai_data_product_id, "alation_ai_data_product_id")

        if revise_request is None:
            revise_request = AlationAIReviseDataProductRequest()

        validate_rest_payload(payload=[revise_request], expected_types=(AlationAIReviseDataProductRequest,))
        payload = revise_request.generate_api_post_payload()

        LOGGER.info(
            "Starting revise data product workflow for %s.",
            alation_ai_data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{alation_ai_data_product_id}/revise_data_product",
            body=payload,
        )

        return AlationAIReviseDataProductResponse.from_api_response(response)

    def get_data_product_revision_jobs(
        self,
        query_params: AlationAIReviseDataProductJobsParams = None,
    ) -> AlationAIReviseDataProductResultsPage:
        """Browse revise data product jobs."""

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
        """Fetch a single revise data product result."""

        self._validate_identifier(result_id, "result_id")

        LOGGER.info("Fetching revise data product result %s.", result_id)
        response = self.get(
            url=f"/ai/api/v1/data_product/revise_data_product_jobs/{result_id}",
            pagination=False,
        )

        return AlationAIReviseDataProductResultDetail.from_api_response(response)

    def validate_data_product_sql(
        self,
        alation_ai_data_product_id: str,
        sql_statements: list[str],
    ) -> list[AlationAISqlWithValidation]:
        """Validate one or more SQL statements against a data product."""

        self._validate_identifier(alation_ai_data_product_id, "alation_ai_data_product_id")
        self._validate_data_product_sql_statements(sql_statements)

        LOGGER.info(
            "Validating %s SQL statement(s) against data product %s.",
            len(sql_statements),
            alation_ai_data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{alation_ai_data_product_id}/validate_sql",
            body=sql_statements,
        )

        if response:
            return [AlationAISqlWithValidation.from_api_response(item) for item in response]
        return []

    def extract_data_product_metrics(
        self,
        alation_ai_data_product_id: str,
        sql_statements: list[str],
    ) -> AlationAIDataProductTask:
        """Extract metrics from one or more SQL statements."""

        self._validate_identifier(alation_ai_data_product_id, "alation_ai_data_product_id")
        self._validate_data_product_sql_statements(sql_statements)

        LOGGER.info(
            "Extracting metrics from %s SQL statement(s) for data product %s.",
            len(sql_statements),
            alation_ai_data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{alation_ai_data_product_id}/extract_metrics",
            body=sql_statements,
        )

        return AlationAIDataProductTask.from_api_response(response)

    def extract_data_product_metrics_from_sample_queries(
        self,
        alation_ai_data_product_id: str,
    ) -> AlationAIDataProductTask:
        """Extract metrics from the sample queries stored on a data product."""

        self._validate_identifier(alation_ai_data_product_id, "alation_ai_data_product_id")

        LOGGER.info(
            "Extracting metrics from sample queries for data product %s.",
            alation_ai_data_product_id,
        )
        response = self.post(
            url=f"/ai/api/v1/data_product/{alation_ai_data_product_id}/extract_metrics_from_sample_queries",
            body=None,
        )

        return AlationAIDataProductTask.from_api_response(response)

    def extract_data_product_metrics_from_bi(
        self,
        alation_ai_data_product_id: str,
        query_params: AlationAIExtractMetricsFromBIParams = None,
    ) -> AlationAIDataProductTask:
        """Extract metrics from downstream BI assets connected to a data product."""

        self._validate_identifier(alation_ai_data_product_id, "alation_ai_data_product_id")
        validate_query_params(query_params, AlationAIExtractMetricsFromBIParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Extracting BI metrics for data product %s.", alation_ai_data_product_id)
        response = self.post(
            url=f"/ai/api/v1/data_product/{alation_ai_data_product_id}/extract_metrics_from_bi",
            body=None,
            query_params=params,
        )

        return AlationAIDataProductTask.from_api_response(response)

    def get_data_product_metrics(self, task_id: str) -> AlationAIAsyncTask | list[AlationAISqlMetricResult]:
        """Retrieve the current status or final SQL metric extraction result."""

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

    def get_data_product_metrics_with_source(self, task_id: str) -> AlationAIAsyncTask | list[AlationAIMetricResultWithSource]:
        """Retrieve metric extraction results including source metadata."""

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

    def get_data_product_tables_from_bi(self, query_params: AlationAIGetTablesFromBIParams) -> AlationAIUpstreamTablesResponse:
        """Resolve upstream tables for a BI dashboard or LookML model folder."""

        if not query_params:
            raise InvalidPostBody("Get Tables From BI query params are required.")

        validate_query_params(query_params, AlationAIGetTablesFromBIParams)
        params = query_params.generate_params_dict()

        LOGGER.info("Fetching upstream tables for BI object %s:%s.", query_params.type, query_params.id)
        response = self.get(
            url="/ai/api/v1/data_product/get_tables_from_bi",
            query_params=params,
            pagination=False,
        )

        if response:
            return AlationAIUpstreamTablesResponse.from_api_response(response)
        return AlationAIUpstreamTablesResponse()

    def create_data_product_from_bi_datasource(
        self,
        datasource_id: int,
        create_product: bool = True,
    ) -> str:
        """Create a data product or preview its spec from a BI datasource."""

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
