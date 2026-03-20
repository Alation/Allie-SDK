import pytest
from allie_sdk.methods.document_hub_folder import *


class TestDocumentModels:

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
            "parent_folder_id": 99,
            "child_documents_count": 12,
            "child_folders_count": 3,
            "nav_links_count": 4,
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
            parent_folder_id = 99,
            child_documents_count = 12,
            child_folders_count = 3,
            nav_links_count = 4,
            custom_fields = [
                {
                "field_id": 0,
                "value": "sample text"
                }
            ]
        )
        

        assert input_transformed == output
    
    def test_document_hub_folder_post_item_model(self):
        
        # Expected input
        input = DocumentHubFolderPostItem(
            title = "My Doc Hub Folder 1"
            , description = "This is the description for Doc Hub Folder 1"
            , document_hub_id = 2
            , template_id = 43
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
            , "template_id": 43
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
        

        assert input_transformed == output
    
    def test_document_hub_folder_put_item_model(self):
        
        # Expected input
        input = DocumentHubFolderPutItem(
            id = 12
            , title = "My Doc Hub Folder 1"
            , description = "This is the description for Doc Hub Folder 1"
            , document_hub_id = 2
            , template_id = 43
            , parent_folder_id = 7
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
            , "template_id": 43
            , "parent_folder_id": 7
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
        

        assert input_transformed == output
