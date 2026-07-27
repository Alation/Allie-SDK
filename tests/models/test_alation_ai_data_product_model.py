"""Tests for the Alation AI Data Product data models."""

from datetime import datetime

import pytest

from allie_sdk.core.custom_exceptions import InvalidPostBody
from allie_sdk.models.alation_ai_data_product_model import *


class TestAlationAIDataProductModel:
    def test_table_column_info_generate_api_payload(self):
        table_column_info = AlationAIDataProductTableColumnInfo(
            table_id=1,
            column_ids=[11, 12],
        )

        assert table_column_info.generate_api_payload() == {
            "table_id": 1,
            "column_ids": [11, 12],
        }

    def test_table_column_info_requires_fields(self):
        with pytest.raises(InvalidPostBody):
            AlationAIDataProductTableColumnInfo(table_id=None, column_ids=[11]).generate_api_payload()

        with pytest.raises(InvalidPostBody):
            AlationAIDataProductTableColumnInfo(table_id=1, column_ids=[]).generate_api_payload()

    def test_data_product_creation_info_generates_payload(self):
        create_request = AlationAIDataProductCreationInfo(
            table_column_info_list=[
                AlationAIDataProductTableColumnInfo(table_id=1, column_ids=[11, 12]),
            ],
            existing_data_product="version: 1",
        )

        payload = create_request.generate_api_post_payload()

        assert payload == {
            "existing_data_product": "version: 1",
            "table_column_info_list": [
                {
                    "table_id": 1,
                    "column_ids": [11, 12],
                }
            ],
        }

    def test_data_product_to_update_requires_existing_yaml(self):
        with pytest.raises(InvalidPostBody):
            AlationAIDataProductToUpdate(existing_data_product=None).generate_api_put_payload()

    def test_revise_data_product_jobs_params_include_zero_and_lists(self):
        params = AlationAIReviseDataProductJobsParams(
            status=["RUNNING", "COMPLETED"],
            data_product_id="dp-1",
            limit=50,
            offset=0,
        )

        assert params.generate_params_dict() == {
            "status": ["RUNNING", "COMPLETED"],
            "data_product_id": "dp-1",
            "limit": 50,
            "offset": 0,
        }

    def test_revise_data_product_results_page_maps_nested_objects(self):
        api_response = {
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
        }

        result_page = AlationAIReviseDataProductResultsPage.from_api_response(api_response)

        assert result_page == AlationAIReviseDataProductResultsPage(
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

    def test_sql_metric_result_maps_nested_metrics(self):
        api_response = {
            "sql": "SELECT SUM(revenue) FROM sales.orders",
            "status": True,
            "metrics": [
                {
                    "displayName": "Total Revenue",
                    "description": "Total revenue across all orders",
                    "expression": "SUM(orders.revenue)",
                    "columns": ["orders.revenue"],
                    "errors": None,
                    "type": "numeric",
                }
            ],
        }

        result = AlationAISqlMetricResult.from_api_response(api_response)

        assert result == AlationAISqlMetricResult(
            sql="SELECT SUM(revenue) FROM sales.orders",
            status=True,
            metrics=[
                AlationAIMetricWithErrors(
                    displayName="Total Revenue",
                    description="Total revenue across all orders",
                    expression="SUM(orders.revenue)",
                    columns=["orders.revenue"],
                    errors=None,
                    type="numeric",
                )
            ],
        )

    def test_metric_result_with_source_maps_nested_sources(self):
        api_response = {
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

        result = AlationAIMetricResultWithSource.from_api_response(api_response)

        assert result == AlationAIMetricResultWithSource(
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

    def test_get_tables_from_bi_params_requires_values(self):
        with pytest.raises(InvalidPostBody):
            AlationAIGetTablesFromBIParams(type=None, id=1).generate_params_dict()

        with pytest.raises(InvalidPostBody):
            AlationAIGetTablesFromBIParams(type="dashboard", id=None).generate_params_dict()
