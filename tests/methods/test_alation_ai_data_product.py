"""Tests for the Alation AI API Data Product methods."""

import json
from datetime import datetime
from unittest.mock import patch

import pytest
import requests
from requests_mock import Mocker

from allie_sdk.core.custom_exceptions import InvalidPostBody, UnsupportedPostBody
from allie_sdk.methods.alation_ai_data_product import AlationAIDataProduct
from allie_sdk.models.alation_ai_data_product_model import (
    AlationAIDataProductTableColumnInfo,
    AlationAIDataProductTask,
    AlationAIDatasourceTables,
    AlationAIExtractMetricsFromBIParams,
    AlationAIGeneratedRelationship,
    AlationAIGenerateRelationshipsRequest,
    AlationAIGenerateRelationshipsResponse,
    AlationAIGetUpstreamTablesFromBiObjectParams,
    AlationAIGetUpstreamTablesFromBiObjectResponse,
    AlationAIMetricResultWithSource,
    AlationAIMetricSource,
    AlationAIMetricWithErrors,
    AlationAIMetricWithSource,
    AlationAIReviseDataProductJobsParams,
    AlationAIReviseDataProductRequest,
    AlationAIReviseDataProductResponse,
    AlationAIReviseDataProductResultsPage,
    AlationAIReviseDataProductResultSummary,
    AlationAISqlMetricResult,
    AlationAISqlWithValidation,
)
from allie_sdk.models.job_model import JobDetails


class TestAlationAIDataProduct:
    def setup_method(self):
        self.mock_alation_ai_data_product = AlationAIDataProduct(
            access_token="test-token",
            session=requests.session(),
            host="https://test.com",
            auth_header_type="Token",
        )

    def test_get_data_product_task_polls_until_yaml(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_data_product_result/task-1",
            response_list=[
                {
                    "json": {
                        "status": "pending",
                        "data": None,
                        "error": None,
                    },
                    "status_code": 200,
                },
                {
                    "json": {
                        "status": "completed",
                        "data": "version: 1\nname: Sales Metrics",
                        "error": None,
                    },
                    "status_code": 200,
                },
            ],
        )

        with patch("allie_sdk.methods.alation_ai_data_product.sleep", return_value=None) as mock_sleep:
            result = self.mock_alation_ai_data_product.get_data_product_creation_result(
                "task-1",
                poll_interval_seconds=0,
            )

        assert result == "version: 1\nname: Sales Metrics"
        mock_sleep.assert_called_once_with(0)
        request = requests_mock.request_history[0]
        assert request.headers["Token"] == "test-token"
        assert len(requests_mock.request_history) == 2

    def test_get_data_product_task_raises_when_task_fails(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_data_product_result/task-2",
            json={
                "status": "failed",
                "data": None,
                "error": "Generation failed.",
            },
            status_code=200,
        )

        with pytest.raises(requests.exceptions.HTTPError, match="Generation failed."):
            self.mock_alation_ai_data_product.get_data_product_creation_result("task-2")

    def test_get_data_product_task_raises_for_legacy_string_response(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_data_product_result/task-3",
            text="version: 1\nname: Sales Metrics",
            status_code=200,
        )

        with pytest.raises(ValueError, match="unsupported response type 'str'"):
            self.mock_alation_ai_data_product.get_data_product_creation_result("task-3")

    def test_get_data_product_task_raises_when_completed_result_has_no_yaml(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_data_product_result/task-4",
            json={
                "status": "completed",
                "data": None,
                "error": None,
            },
            status_code=200,
        )

        with pytest.raises(ValueError, match="completed without returning YAML data"):
            self.mock_alation_ai_data_product.get_data_product_creation_result("task-4")

    def test_generate_relationships(self, requests_mock: Mocker) -> None:
        """Return generated relationship models inside successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.

        Returns:
            None: Assertions verify the nested response and request payload.
        """
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/generate_relationships",
            json={
                "relationships": [
                    {
                        "name": "orders_to_customers",
                        "left_table": "orders",
                        "right_table": "customers",
                        "expression": "orders.customer_id = customers.id",
                        "sql_dialect": "postgres",
                        "cardinality": "many_to_one",
                        "left_nullable": False,
                        "right_nullable": False,
                        "notes": "Generated from primary key inference.",
                    }
                ]
            },
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.generate_relationships(
            AlationAIGenerateRelationshipsRequest(data_product_spec_yaml="version: 1\nname: Sales Metrics")
        )

        assert result == JobDetails(
            status="successful",
            msg="",
            result=AlationAIGenerateRelationshipsResponse(
                relationships=[
                    AlationAIGeneratedRelationship(
                        name="orders_to_customers",
                        left_table="orders",
                        right_table="customers",
                        expression="orders.customer_id = customers.id",
                        sql_dialect="postgres",
                        cardinality="many_to_one",
                        left_nullable=False,
                        right_nullable=False,
                        notes="Generated from primary key inference.",
                    )
                ]
            ),
        )
        request = requests_mock.request_history[0]
        assert request.headers["Token"] == "test-token"
        assert json.loads(request.text) == {
            "spec_yaml": "version: 1\nname: Sales Metrics",
        }

    def test_revise_data_product(self, requests_mock: Mocker) -> None:
        """Return revise workflow identifiers inside successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.

        Returns:
            None: Assertions verify the nested revise response model.
        """
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/dp-1/revise_data_product",
            json={
                "result_id": "result-1",
                "chat_id": "chat-1",
            },
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.initiate_revise_data_product_workflow(
            "dp-1",
            AlationAIReviseDataProductRequest(message="Please tighten the metric descriptions."),
        )

        assert result == JobDetails(
            status="successful",
            msg="",
            result=AlationAIReviseDataProductResponse(
                result_id="result-1",
                chat_id="chat-1",
            ),
        )

    def test_get_data_product_revision_jobs(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/revise_data_product_jobs",
            json={
                "data": [
                    {
                        "result_id": "result-1",
                        "chat_id": "chat-1",
                        "data_product_id": "dp-1",
                        "status": "RUNNING",
                        "created_at": "2026-06-10T12:00:00.000000Z",
                        "updated_at": "2026-06-10T12:05:00.000000Z",
                    }
                ],
                "total": 1,
            },
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.get_data_product_revision_jobs(
            AlationAIReviseDataProductJobsParams(
                status=["RUNNING", "COMPLETED"],
                limit=50,
                offset=0,
            )
        )

        assert result == AlationAIReviseDataProductResultsPage(
            data=[
                AlationAIReviseDataProductResultSummary(
                    result_id="result-1",
                    chat_id="chat-1",
                    data_product_id="dp-1",
                    status="RUNNING",
                    created_at=datetime(2026, 6, 10, 12, 0, 0),
                    updated_at=datetime(2026, 6, 10, 12, 5, 0),
                )
            ],
            total=1,
        )
        request = requests_mock.request_history[0]
        assert request.qs["status"] == ["running", "completed"]
        assert request.qs["limit"] == ["50"]
        assert request.qs["offset"] == ["0"]

    def test_get_data_product_revision_result(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/revise_data_product_jobs/result-1",
            json={
                "result_id": "result-1",
                "chat_id": "chat-1",
                "data_product_id": "dp-1",
                "status": "COMPLETED",
                "created_at": "2026-06-10T12:00:00.000000Z",
                "updated_at": "2026-06-10T12:10:00.000000Z",
                "message": "Improve metric quality.",
                "summary": "Updated several metric descriptions.",
                "initial_data_product_yaml": "version: 1",
                "final_data_product_yaml": "version: 2",
            },
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.get_data_product_revision_result(
            "result-1"
        )

        assert result.result_id == "result-1"
        assert result.summary == "Updated several metric descriptions."

    def test_validate_sql_against_data_product(self, requests_mock: Mocker) -> None:
        """Return SQL validation models inside successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.

        Returns:
            None: Assertions verify the nested validation result list.
        """
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/dp-1/validate_sql",
            json=[
                {
                    "sql": "SELECT 1",
                    "status": True,
                    "error": None,
                }
            ],
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.validate_sql(
            "dp-1",
            ["SELECT 1"],
        )

        assert result == JobDetails(
            status="successful",
            msg="",
            result=[
                AlationAISqlWithValidation(
                    sql="SELECT 1",
                    status=True,
                    error=None,
                )
            ],
        )

    def test_extract_metrics_from_sql_statements(self, requests_mock: Mocker) -> None:
        """Return the SQL metric extraction task inside successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.

        Returns:
            None: Assertions verify the nested task model.
        """
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/dp-1/extract_metrics",
            json={"task_id": "metrics-task-1"},
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.extract_metrics_from_sql_statements(
            "dp-1",
            ["SELECT SUM(revenue) FROM sales"],
        )

        assert result == JobDetails(
            status="successful",
            msg="",
            result=AlationAIDataProductTask(task_id="metrics-task-1"),
        )

    def test_extract_data_product_metrics_from_sample_queries(self, requests_mock: Mocker) -> None:
        """Return the sample query extraction task inside successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.

        Returns:
            None: Assertions verify the nested task model.
        """
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/dp-1/extract_metrics_from_sample_queries",
            json={"task_id": "metrics-task-2"},
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.extract_data_product_metrics_from_sample_queries(
            "dp-1"
        )

        assert result == JobDetails(
            status="successful",
            msg="",
            result=AlationAIDataProductTask(task_id="metrics-task-2"),
        )

    def test_extract_data_product_metrics_from_bi(self, requests_mock: Mocker) -> None:
        """Return the BI extraction task inside successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.

        Returns:
            None: Assertions verify the nested task and request parameters.
        """
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/dp-1/extract_metrics_from_bi",
            json={"task_id": "metrics-task-3"},
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.extract_data_product_metrics_from_bi(
            "dp-1",
            AlationAIExtractMetricsFromBIParams(
                dashboard_ids=[1, 2],
                lookml_model_folder_ids=[3],
            ),
        )

        assert result == JobDetails(
            status="successful",
            msg="",
            result=AlationAIDataProductTask(task_id="metrics-task-3"),
        )
        request = requests_mock.request_history[0]
        assert request.qs["dashboard_ids"] == ["1", "2"]
        assert request.qs["lookml_model_folder_ids"] == ["3"]

    def test_get_data_product_metrics_extraction_result(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_metrics/task-3",
            json=[
                {
                    "sql": "SELECT SUM(revenue) FROM sales.orders",
                    "status": True,
                    "metrics": [
                        {
                            "displayName": "Total Revenue",
                            "description": "Total revenue across all orders",
                            "expression": "SUM(orders.revenue)",
                            "columns": ["orders.revenue"],
                            "type": "numeric",
                        }
                    ],
                }
            ],
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.get_data_product_metrics_extraction_result("task-3")

        assert result == [
            AlationAISqlMetricResult(
                sql="SELECT SUM(revenue) FROM sales.orders",
                status=True,
                metrics=[
                    AlationAIMetricWithErrors(
                        displayName="Total Revenue",
                        description="Total revenue across all orders",
                        expression="SUM(orders.revenue)",
                        columns=["orders.revenue"],
                        type="numeric",
                    )
                ],
            )
        ]

    def test_get_data_product_metrics_extraction_result_with_source(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_metrics_with_source/task-4",
            json=[
                {
                    "status": True,
                    "metrics": [
                        {
                            "displayName": "Total Revenue",
                            "description": "Total revenue across all orders",
                            "expression": "SUM(orders.revenue)",
                            "sources": [
                                {
                                    "source_type": "tableau",
                                    "source_name": "Revenue Dashboard",
                                    "original_expression": "SUM([Revenue])",
                                    "extracted_at": "2026-06-10T12:10:00.000000Z",
                                    "source_url": "https://example.com/report",
                                    "catalog_url": "/bi/1/",
                                }
                            ],
                        }
                    ],
                }
            ],
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.get_data_product_metrics_extraction_result_with_source(
            "task-4"
        )

        assert result == [
            AlationAIMetricResultWithSource(
                status=True,
                metrics=[
                    AlationAIMetricWithSource(
                        displayName="Total Revenue",
                        description="Total revenue across all orders",
                        expression="SUM(orders.revenue)",
                        sources=[
                            AlationAIMetricSource(
                                source_type="tableau",
                                source_name="Revenue Dashboard",
                                original_expression="SUM([Revenue])",
                                extracted_at=datetime(2026, 6, 10, 12, 10, 0),
                                source_url="https://example.com/report",
                                catalog_url="/bi/1/",
                            )
                        ],
                    )
                ],
            )
        ]

    def test_get_upstream_tables_from_bi_object(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_tables_from_bi",
            json={
                "datasources": [
                    {
                        "datasource_id": 1,
                        "tables": [
                            {
                                "table_id": 100,
                                "column_ids": [1001, 1002],
                            }
                        ],
                    }
                ]
            },
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.get_upstream_tables_from_bi_object(
            AlationAIGetUpstreamTablesFromBiObjectParams(type="dashboard", id=99)
        )

        assert result == AlationAIGetUpstreamTablesFromBiObjectResponse(
            datasources=[
                AlationAIDatasourceTables(
                    datasource_id=1,
                    tables=[
                        AlationAIDataProductTableColumnInfo(
                            table_id=100,
                            column_ids=[1001, 1002],
                        )
                    ],
                )
            ]
        )
        request = requests_mock.request_history[0]
        assert request.qs["type"] == ["dashboard"]
        assert request.qs["id"] == ["99"]

    def test_create_data_product_from_bi_source(self, requests_mock: Mocker) -> None:
        """Return the BI specification preview inside successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.

        Returns:
            None: Assertions verify the nested YAML and request parameters.
        """
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/create_from_bi_datasource",
            text="version: 1\nname: Revenue Dashboard",
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.create_data_product_from_bi_source(
            datasource_id=5,
            create_product=False,
        )

        assert result == JobDetails(
            status="successful",
            msg="",
            result="version: 1\nname: Revenue Dashboard",
        )
        request = requests_mock.request_history[0]
        assert request.qs["datasource_id"] == ["5"]
        assert request.qs["create_product"] == ["false"]

    @pytest.mark.parametrize("status_code", [200, 204])
    @pytest.mark.parametrize(
        "method_name, arguments, url, empty_response, expected_result",
        [
            (
                "generate_relationships",
                (AlationAIGenerateRelationshipsRequest(data_product_spec_yaml="version: 1"),),
                "/ai/api/v1/data_product/generate_relationships",
                {},
                AlationAIGenerateRelationshipsResponse(),
            ),
            (
                "validate_sql",
                ("dp-1", ["SELECT 1"]),
                "/ai/api/v1/data_product/dp-1/validate_sql",
                [],
                [],
            ),
        ],
    )
    def test_empty_results_are_nested_in_job_details(
        self,
        requests_mock: Mocker,
        status_code: int,
        method_name: str,
        arguments: tuple[object, ...],
        url: str,
        empty_response: dict | list,
        expected_result: AlationAIGenerateRelationshipsResponse | list,
    ) -> None:
        """Preserve empty relationship and validation results within job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.
            status_code (int): Successful response status to exercise.
            method_name (str): Data product method to invoke.
            arguments (tuple[object, ...]): Positional method arguments.
            url (str): Endpoint whose response is mocked.
            empty_response (dict | list): Empty JSON payload for HTTP 200.
            expected_result (AlationAIGenerateRelationshipsResponse | list): Nested
                empty result expected from the method.

        Returns:
            None: Assertions verify successful job details with the empty result.
        """
        if status_code == 204:
            requests_mock.post(url, status_code=status_code, text="")
        else:
            requests_mock.post(url, status_code=status_code, json=empty_response)

        result = getattr(self.mock_alation_ai_data_product, method_name)(*arguments)

        assert result == JobDetails(status="successful", msg="", result=expected_result)

    @pytest.mark.parametrize(
        "method_name, arguments, url",
        [
            (
                "generate_relationships",
                (AlationAIGenerateRelationshipsRequest(data_product_spec_yaml="version: 1"),),
                "/ai/api/v1/data_product/generate_relationships",
            ),
            (
                "initiate_revise_data_product_workflow",
                ("dp-1",),
                "/ai/api/v1/data_product/dp-1/revise_data_product",
            ),
            (
                "validate_sql",
                ("dp-1", ["SELECT 1"]),
                "/ai/api/v1/data_product/dp-1/validate_sql",
            ),
            (
                "extract_metrics_from_sql_statements",
                ("dp-1", ["SELECT COUNT(*) FROM sales"]),
                "/ai/api/v1/data_product/dp-1/extract_metrics",
            ),
            (
                "extract_data_product_metrics_from_sample_queries",
                ("dp-1",),
                "/ai/api/v1/data_product/dp-1/extract_metrics_from_sample_queries",
            ),
            (
                "extract_data_product_metrics_from_bi",
                ("dp-1",),
                "/ai/api/v1/data_product/dp-1/extract_metrics_from_bi",
            ),
            (
                "create_data_product_from_bi_source",
                (5,),
                "/ai/api/v1/data_product/create_from_bi_datasource",
            ),
        ],
    )
    def test_post_methods_raise_for_http_errors(
        self,
        requests_mock: Mocker,
        method_name: str,
        arguments: tuple[object, ...],
        url: str,
    ) -> None:
        """Keep API failures from being wrapped as successful job details.

        Args:
            requests_mock (Mocker): Mock HTTP responses and record requests.
            method_name (str): Data product method to invoke.
            arguments (tuple[object, ...]): Positional method arguments.
            url (str): Endpoint whose failed response is mocked.

        Returns:
            None: Assertions verify that HTTP errors reach the caller.
        """
        requests_mock.post(url, status_code=500, json={"detail": "AI request failed."})

        with pytest.raises(requests.exceptions.HTTPError):
            getattr(self.mock_alation_ai_data_product, method_name)(*arguments)

    @pytest.mark.parametrize("method_name", ["validate_sql", "extract_metrics_from_sql_statements"])
    @pytest.mark.parametrize(
        "sql_statements, expected_exception",
        [
            (None, InvalidPostBody),
            ([], InvalidPostBody),
            ("SELECT 1", UnsupportedPostBody),
            ("", UnsupportedPostBody),
            (("SELECT 1",), UnsupportedPostBody),
            ({"SELECT 1": "query"}, UnsupportedPostBody),
            ({}, UnsupportedPostBody),
            (42, UnsupportedPostBody),
            (["SELECT 1", 42], UnsupportedPostBody),
        ],
    )
    def test_sql_methods_reject_invalid_payloads_before_request(
        self,
        requests_mock: Mocker,
        method_name: str,
        sql_statements: object,
        expected_exception: type[Exception],
    ) -> None:
        """Reject missing SQL and invalid containers or elements before HTTP calls.

        Args:
            requests_mock (Mocker): Record whether any HTTP request is attempted.
            method_name (str): SQL data product method to invoke.
            sql_statements (object): Invalid SQL payload to reject.
            expected_exception (type[Exception]): Required validation exception.

        Returns:
            None: Assertions verify validation errors and the absence of requests.
        """
        with pytest.raises(expected_exception):
            getattr(self.mock_alation_ai_data_product, method_name)("dp-1", sql_statements)

        assert not requests_mock.called

    @pytest.mark.parametrize("identifier", [None, "", " ", "\t\n", 42])
    @pytest.mark.parametrize(
        "method_name, remaining_arguments",
        [
            ("get_data_product_creation_result", ()),
            ("initiate_revise_data_product_workflow", ()),
            ("get_data_product_revision_result", ()),
            ("validate_sql", (["SELECT 1"],)),
            ("extract_metrics_from_sql_statements", (["SELECT 1"],)),
            ("extract_data_product_metrics_from_sample_queries", ()),
            ("extract_data_product_metrics_from_bi", ()),
            ("get_data_product_metrics_extraction_result", ()),
            ("get_data_product_metrics_extraction_result_with_source", ()),
        ],
    )
    def test_methods_reject_invalid_identifiers_before_request(
        self,
        requests_mock: Mocker,
        identifier: object,
        method_name: str,
        remaining_arguments: tuple[object, ...],
    ) -> None:
        """Reject missing, blank, and non-string identifiers in each affected method.

        Args:
            requests_mock (Mocker): Record whether any HTTP request is attempted.
            identifier (object): Invalid identifier to reject.
            method_name (str): Method requiring a string identifier.
            remaining_arguments (tuple[object, ...]): Other required method arguments.

        Returns:
            None: Assertions verify validation errors and the absence of requests.
        """
        with pytest.raises(InvalidPostBody, match="non-empty string"):
            getattr(self.mock_alation_ai_data_product, method_name)(identifier, *remaining_arguments)

        assert not requests_mock.called

    @pytest.mark.parametrize("task_status", ["pending", "running"])
    def test_creation_polling_times_out_and_caps_sleep(
        self,
        requests_mock: Mocker,
        task_status: str,
    ) -> None:
        """Stop polling at the deadline and cap sleep to the remaining time.

        Args:
            requests_mock (Mocker): Return a task that remains unfinished.
            task_status (str): Non-terminal task status to exercise.

        Returns:
            None: Assertions verify timeout details, capped sleep, and request count.
        """
        requests_mock.get(
            "/ai/api/v1/data_product/get_data_product_result/task-timeout",
            json={"status": task_status, "data": None, "error": None},
        )

        with (
            patch("allie_sdk.methods.alation_ai_data_product.monotonic", side_effect=[100, 100, 104, 105]),
            patch("allie_sdk.methods.alation_ai_data_product.sleep") as mocked_sleep,
        ):
            with pytest.raises(TimeoutError, match="task-timeout.*5 seconds"):
                self.mock_alation_ai_data_product.get_data_product_creation_result(
                    "task-timeout",
                    poll_interval_seconds=3,
                    timeout_seconds=5,
                )

        mocked_sleep.assert_called_once_with(1)
        assert requests_mock.call_count == 1

    def test_creation_polling_has_a_default_timeout(self, requests_mock: Mocker) -> None:
        """Apply the five-minute deadline when no timeout is supplied.

        Args:
            requests_mock (Mocker): Record whether any HTTP request is attempted.

        Returns:
            None: Assertions verify timeout before a request after the deadline.
        """
        with patch("allie_sdk.methods.alation_ai_data_product.monotonic", side_effect=[100, 400]):
            with pytest.raises(TimeoutError, match="300 seconds"):
                self.mock_alation_ai_data_product.get_data_product_creation_result("task-timeout")

        assert not requests_mock.called

    @pytest.mark.parametrize("timeout_seconds", [10, None])
    def test_creation_polling_completes_with_configured_timeout(
        self,
        requests_mock: Mocker,
        timeout_seconds: float | None,
    ) -> None:
        """Complete polling with a configured deadline or an explicitly disabled one.

        Args:
            requests_mock (Mocker): Return a pending task followed by completed YAML.
            timeout_seconds (float | None): Time limit or None to disable the deadline.

        Returns:
            None: Assertions verify returned YAML, sleep, and disabled clock checks.
        """
        requests_mock.get(
            "/ai/api/v1/data_product/get_data_product_result/task-complete",
            response_list=[
                {"json": {"status": "pending", "data": None, "error": None}},
                {"json": {"status": "completed", "data": "version: 1", "error": None}},
            ],
        )

        with (
            patch("allie_sdk.methods.alation_ai_data_product.monotonic", side_effect=[100, 100, 101, 104]) as mocked_clock,
            patch("allie_sdk.methods.alation_ai_data_product.sleep") as mocked_sleep,
        ):
            result = self.mock_alation_ai_data_product.get_data_product_creation_result(
                "task-complete",
                timeout_seconds=timeout_seconds,
            )

        assert result == "version: 1"
        assert requests_mock.call_count == 2
        mocked_sleep.assert_called_once_with(3)
        if timeout_seconds is None:
            mocked_clock.assert_not_called()

    @pytest.mark.parametrize(
        "parameter_name, invalid_value",
        [
            ("poll_interval_seconds", -1),
            ("poll_interval_seconds", float("nan")),
            ("poll_interval_seconds", float("inf")),
            ("timeout_seconds", -1),
            ("timeout_seconds", 0),
            ("timeout_seconds", float("nan")),
            ("timeout_seconds", float("inf")),
        ],
    )
    def test_creation_polling_rejects_invalid_timing_before_request(
        self,
        requests_mock: Mocker,
        parameter_name: str,
        invalid_value: float,
    ) -> None:
        """Reject negative and non-finite polling settings before HTTP calls.

        Args:
            requests_mock (Mocker): Record whether any HTTP request is attempted.
            parameter_name (str): Timing parameter to validate.
            invalid_value (float): Unsupported timing value.

        Returns:
            None: Assertions verify a clear validation error without requests.
        """
        with pytest.raises(InvalidPostBody, match=parameter_name):
            self.mock_alation_ai_data_product.get_data_product_creation_result(
                "task-1",
                **{parameter_name: invalid_value},
            )

        assert not requests_mock.called
