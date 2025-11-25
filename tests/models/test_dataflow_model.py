import pytest
from allie_sdk.models.dataflow_model import *


class TestDataflowModels:

    def test_dataflow_model(self):
        input_dict = {
            "id": 1,
            "external_id": "api/df101",
            "title": "Purchase transaction Transformation",
            "description": "Data flow from customer table to purchase history table",
            "content": "select * from table",
            "group_name": "Snowflake-1"
        }

        input_transformed = Dataflow(**input_dict)

        output = Dataflow(
            id=1,
            external_id="api/df101",
            title="Purchase transaction Transformation",
            description="Data flow from customer table to purchase history table",
            content="select * from table",
            group_name="Snowflake-1"
        )

        assert input_transformed == output

    def test_dataflow_payload_post(self):
        payload_obj = DataflowPayload(
            dataflow_objects=[
                Dataflow(
                    external_id="api/df101",
                    title="Purchase transaction Transformation",
                    description="Data flow from customer table to purchase history table",
                    content="select c.id from customers c",
                    group_name="Snowflake-1",
                )
            ],
            paths=[
                [
                    [DataflowPathObject(otype="table", key="1.schema.Customers")],
                    [DataflowPathObject(otype="dataflow", key="api/df101")],
                    [DataflowPathObject(otype="table", key="1.schema.Purchases")],
                ]
            ],
        )

        expected = {
            "dataflow_objects": [
                {
                    "external_id": "api/df101",
                    "title": "Purchase transaction Transformation",
                    "description": "Data flow from customer table to purchase history table",
                    "content": "select c.id from customers c",
                    "group_name": "Snowflake-1",
                }
            ],
            "paths": [
                [
                    [{"otype": "table", "key": "1.schema.Customers"}],
                    [{"otype": "dataflow", "key": "api/df101"}],
                    [{"otype": "table", "key": "1.schema.Purchases"}],
                ]
            ],
        }

        assert payload_obj.generate_api_post_payload() == expected

    def test_dataflow_patch_item(self):
        item = DataflowPatchItem(
            id=1,
            title="New title",
            description="New description",
            content="select *",
            group_name="Group",
        )

        expected = {
            "id": 1,
            "title": "New title",
            "description": "New description",
            "content": "select *",
            "group_name": "Group",
        }

        assert item.generate_api_patch_payload() == expected
