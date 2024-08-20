import unittest
from allie_sdk.methods.document_hub_folder import *


class TestDocumentModels(unittest.TestCase):

    def test_document_hub_folder_model(self):
        
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
            "document_hub_id": 1,
            "custom_fields": [
                {
                "field_id": 0,
                "value": "sample text"
                }
            ]
        }

        # Transformation
        input_transformed = DocumentHubFolder(**input)

        # Expected Output
        output = DocumentHubFolder(
            id = 1,
            deleted = False,
            ts_deleted = "2022-07-05T15:09:40.421916Z",
            ts_created = "2022-07-05T15:09:40.421916Z",
            ts_updated = "2022-07-05T15:09:40.421916Z",
            title = "Sales",
            description = "Relevant data and articles for Sales Analytics",
            template_id = 47,
            document_hub_id = 1,
            custom_fields = [
                {
                "field_id": 0,
                "value": "sample text"
                }
            ]
        )
        

        self.assertEqual(input_transformed, output)
    
    def test_document_hub_folder_post_item_model(self):
        
        # Expected input
        input = DocumentHubFolderPostItem(
            title = "My Doc Hub Folder 1"
            , description = "This is the description for Doc Hub Folder 1"
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
            "title": "My Doc Hub Folder 1"
            , "description": "This is the description for Doc Hub Folder 1"
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
    
    def test_document_hub_folder_put_item_model(self):
        
        # Expected input
        input = DocumentHubFolderPutItem(
            id = 12
            , title = "My Doc Hub Folder 1"
            , description = "This is the description for Doc Hub Folder 1"
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
            , "title": "My Doc Hub Folder 1"
            , "description": "This is the description for Doc Hub Folder 1"
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