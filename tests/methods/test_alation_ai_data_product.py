"""Tests for the Alation AI API Data Product methods."""

from datetime import datetime
import json
from unittest.mock import patch

import pytest
import requests

from allie_sdk.methods.alation_ai_data_product import AlationAIDataProduct
from allie_sdk.models.alation_ai_data_product_model import (
    AlationAIDataProductCreationInfo,
    AlationAIDataProductTask,
    AlationAIDatasourceTables,
    AlationAIExtractMetricsFromBIParams,
    AlationAIGenerateRelationshipsRequest,
    AlationAIGenerateRelationshipsResponse,
    AlationAIGeneratedRelationship,
    AlationAIGetUpstreamTablesFromBiObjectParams,
    AlationAIMetricResultWithSource,
    AlationAIMetricSource,
    AlationAIMetricWithErrors,
    AlationAIMetricWithSource,
    AlationAIReviseDataProductJobsParams,
    AlationAIReviseDataProductRequest,
    AlationAIReviseDataProductResponse,
    AlationAIReviseDataProductResultSummary,
    AlationAIReviseDataProductResultsPage,
    AlationAISqlMetricResult,
    AlationAISqlWithValidation,
    AlationAIDataProductTableColumnInfo,
    AlationAIGetUpstreamTablesFromBiObjectResponse,
)


class TestAlationAIDataProduct:
    def setup_method(self):
        self.mock_alation_ai_data_product = AlationAIDataProduct(
            access_token="test-token",
            session=requests.session(),
            host="https://test.com",
        )

    def test_enrich_data_product_spec(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/enrich_data_product_spec",
            json={"task_id": "task-1"},
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.enrich_data_product_spec(
            AlationAIDataProductCreationInfo(
                table_column_info_list=[
                    AlationAIDataProductTableColumnInfo(table_id=1, column_ids=[11, 12]),
                ]
            )
        )

        assert result == AlationAIDataProductTask(task_id="task-1")
        request = requests_mock.request_history[0]
        assert request.headers["Token"] == "test-token"
        assert request.qs["generate_missing_descriptions"] == ["true"]

    def test_enrich_data_product_spec_with_existing_data_product(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/enrich_data_product_spec",
            json={"task_id": "task-2"},
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.enrich_data_product_spec(
            AlationAIDataProductCreationInfo(
                table_column_info_list=[
                    AlationAIDataProductTableColumnInfo(table_id=1, column_ids=[11, 12]),
                ],
                existing_data_product="version: 1",
            )
        )

        assert result == AlationAIDataProductTask(task_id="task-2")
        request = requests_mock.request_history[0]
        payload = json.loads(request.text)
        assert payload["existing_data_product"] == "version: 1"
        assert payload["table_column_info_list"] == [
            {
                "table_id": 1,
                "column_ids": [11, 12],
            }
        ]

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
            result = self.mock_alation_ai_data_product.get_data_product_task(
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
            self.mock_alation_ai_data_product.get_data_product_task("task-2")

    def test_get_data_product_task_raises_for_legacy_string_response(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/ai/api/v1/data_product/get_data_product_result/task-3",
            text="version: 1\nname: Sales Metrics",
            status_code=200,
        )

        with pytest.raises(ValueError, match="unsupported response type 'str'"):
            self.mock_alation_ai_data_product.get_data_product_task("task-3")

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
            self.mock_alation_ai_data_product.get_data_product_task("task-4")

    def test_generate_relationships(self, requests_mock):
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

        assert result == AlationAIGenerateRelationshipsResponse(
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
        )
        request = requests_mock.request_history[0]
        assert request.headers["Token"] == "test-token"
        assert json.loads(request.text) == {
            "spec_yaml": "version: 1\nname: Sales Metrics",
        }

    def test_revise_data_product(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/dp-1/revise_data_product",
            json={
                "result_id": "result-1",
                "chat_id": "chat-1",
            },
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.revise_data_product(
            "dp-1",
            AlationAIReviseDataProductRequest(message="Please tighten the metric descriptions."),
        )

        assert result == AlationAIReviseDataProductResponse(
            result_id="result-1",
            chat_id="chat-1",
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

    def test_validate_sql_against_data_product(self, requests_mock):
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

        assert result == [
            AlationAISqlWithValidation(
                sql="SELECT 1",
                status=True,
                error=None,
            )
        ]

    def test_extract_metrics_from_sql_statements(self, requests_mock):
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

        assert result == AlationAIDataProductTask(task_id="metrics-task-1")

    def test_extract_data_product_metrics_from_sample_queries(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/ai/api/v1/data_product/dp-1/extract_metrics_from_sample_queries",
            json={"task_id": "metrics-task-2"},
            status_code=200,
        )

        result = self.mock_alation_ai_data_product.extract_data_product_metrics_from_sample_queries(
            "dp-1"
        )

        assert result == AlationAIDataProductTask(task_id="metrics-task-2")

    def test_extract_data_product_metrics_from_bi(self, requests_mock):
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

        assert result == AlationAIDataProductTask(task_id="metrics-task-3")
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

    def test_create_data_product_from_bi_source(self, requests_mock):
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

        assert result == "version: 1\nname: Revenue Dashboard"
        request = requests_mock.request_history[0]
        assert request.qs["datasource_id"] == ["5"]
        assert request.qs["create_product"] == ["false"]
