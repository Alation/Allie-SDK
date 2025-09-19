import unittest
from allie_sdk.methods.document import *


class TestDocumentModels(unittest.TestCase):

    def test_document_model(self):
        
        # Expected input
        input = {
            "id": 1,
            "deleted": False,
            "ts_deleted": "2022-07-05T15:09:40.421916Z",
            "ts_created": "2022-07-05T15:09:40.421916Z",
            "ts_updated": "2022-07-05T15:09:40.421916Z",
            "title": "Sales",
            "description": "Relevant data and articles for Sales Analytics",
            "template_id": 47,
            "parent_folder_id": 1,
            "parent_document_id": 99,
            "nav_link_folder_ids": [14,165],
            "document_hub_id": 1,
            "custom_fields": [
                {
                "field_id": 0,
                "value": "sample text"
                }
            ]
        }

        # Transformation
        input_transformed = Document(**input)

        # Expected Output
        output = Document(
            id = 1,
            deleted = False,
            ts_deleted = "2022-07-05T15:09:40.421916Z",
            # is_public = True, => was removed Apr 2024
            ts_created = "2022-07-05T15:09:40.421916Z",
            ts_updated = "2022-07-05T15:09:40.421916Z",
            # otype = "glossary_term", => was removed Apr 2024
            title = "Sales",
            description = "Relevant data and articles for Sales Analytics",
            template_id = 47,
            parent_folder_id = 1,
            parent_document_id = 99,
            nav_link_folder_ids = [
                14,
                165
            ],
            document_hub_id = 1,
            custom_fields = [
                {
                "field_id": 0,
                "value": "sample text"
                }
            ]
        )
        

        self.assertEqual(input_transformed, output)
    
    def test_document_post_item_model(self):
        
        # Expected input
        input = DocumentPostItem(
            title = "My KPI 1"
            , description = "This is the description for KPI 1"
            , template_id = 12
            , parent_folder_id = 1
            , parent_document_id = 2
            , nav_link_folder_ids = [ 6 ]
            , document_hub_id = 2
            , custom_fields = [
                CustomFieldValueItem(
                    field_id = 44
                    , value = [
                        CustomFieldDictValueItem(
                            otype = "glossary_term"
                            , oid = 159
                        )
                    ]
                )
            ]
        )

        # Transformation
        input_transformed = input.generate_api_post_payload()

        # Expected Output
        output = {
            "title": "My KPI 1"
            , "description": "This is the description for KPI 1"
            , "template_id": 12
            , "parent_folder_id": 1
            , "parent_document_id": 2
            , "nav_link_folder_ids": [ 6 ]
            , "document_hub_id": 2
            , "custom_fields": [
                {
                    "field_id": 44
                    , "value": [
                        {
                            "otype": "glossary_term"
                            , "oid": 159
                        }
                    ]
                }
            ]
        }
        

        self.assertEqual(input_transformed, output)
    
    def test_document_put_item_model(self):
        
        # Expected input
        input = DocumentPutItem(
            id = 12
            , title = "My KPI 1"
            , description = "This is the description for KPI 1"
            , template_id = 12
            , parent_folder_id = 1
            , parent_document_id = 2
            , nav_link_folder_ids = [ 6 ]
            , document_hub_id = 2
            , custom_fields = [
                CustomFieldValueItem(
                    field_id = 44
                    , value = [
                        CustomFieldDictValueItem(
                            otype = "glossary_term"
                            , oid = 159
                        )
                    ]
                )
            ]
        )

        # Transformation
        input_transformed = input.generate_api_put_payload()

        # Expected Output
        output = {
            "id": 12
            , "title": "My KPI 1"
            , "description": "This is the description for KPI 1"
            , "template_id": 12
            , "parent_folder_id": 1
            , "parent_document_id": 2
            , "nav_link_folder_ids": [ 6 ]
            , "document_hub_id": 2
            , "custom_fields": [
                {
                    "field_id": 44
                    , "value": [
                        {
                            "otype": "glossary_term"
                            , "oid": 159
                        }
                    ]
                }
            ]
        }


        self.assertEqual(input_transformed, output)
