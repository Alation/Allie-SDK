import unittest
from allie_sdk.models.visual_config_model import *


class TestVisualConfigModels(unittest.TestCase):

    def test_visual_config_model(self):
        # Expected input
        input = {
            "id": 20,
            "component_list_in_config": [
                {
                    "rendered_otype": "CUSTOM_FIELD",
                    "rendered_oid": 4,
                    "page_defined_type": None,
                    "component_type": "BUILT_IN",
                    "panel": "MAIN"
                },
                {
                    "rendered_otype": None,
                    "rendered_oid": None,
                    "page_defined_type": "catalog_document_collection.document_collection_links_table",
                    "component_type": "PAGE_DEFINED",
                    "panel": "MAIN"
                },
                {
                    "rendered_otype": None,
                    "rendered_oid": None,
                    "page_defined_type": "catalog_document_collection.properties",
                    "component_type": "PAGE_DEFINED",
                    "panel": "SIDEBAR"
                },
                {
                    "rendered_otype": None,
                    "rendered_oid": None,
                    "page_defined_type": "catalog.membership_to_domains",
                    "component_type": "PAGE_DEFINED",
                    "panel": "SIDEBAR"
                },
                {
                    "rendered_otype": "CUSTOM_FIELD",
                    "rendered_oid": 8,
                    "page_defined_type": None,
                    "component_type": "BUILT_IN",
                    "panel": "MAIN"
                },
                {
                    "rendered_otype": None,
                    "rendered_oid": None,
                    "page_defined_type": "catalog.tags",
                    "component_type": "PAGE_DEFINED",
                    "panel": "SIDEBAR"
                },
                {
                    "label": "Referenced By",
                    "components": [
                        {
                            "rendered_otype": None,
                            "rendered_oid": None,
                            "page_defined_type": "catalog.mentioned_on",
                            "component_type": "PAGE_DEFINED",
                            "panel": "SIDEBAR"
                        },
                        {
                            "rendered_otype": None,
                            "rendered_oid": None,
                            "page_defined_type": "catalog.article_backreferences",
                            "component_type": "PAGE_DEFINED",
                            "panel": "SIDEBAR"
                        },
                        {
                            "rendered_otype": None,
                            "rendered_oid": None,
                            "page_defined_type": "catalog.objectset_backreferences",
                            "component_type": "PAGE_DEFINED",
                            "panel": "SIDEBAR"
                        }
                    ],
                    "open_by_default": None,
                    "panel": "SIDEBAR",
                    "is_group": None
                }
            ],
            "title": "Folder", # => only part of the response to a POST request
            "layout_otype": "glossary_v3"
        }

        # Transformation
        input_transformed = VisualConfig(**input)

        # Expected Output
        output = VisualConfig(
            title='Folder' # => only part of the response to a POST request
            , layout_otype='glossary_v3'
            , component_list_in_config=[
                VisualConfigComponent(
                    rendered_otype='CUSTOM_FIELD'
                    , rendered_oid=4, page_defined_type=None
                    , component_type='BUILT_IN'
                    , panel='MAIN'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog_document_collection.document_collection_links_table'
                    , component_type='PAGE_DEFINED'
                    , panel='MAIN'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog_document_collection.properties'
                    , component_type='PAGE_DEFINED'
                    , panel='SIDEBAR'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog.membership_to_domains'
                    , component_type='PAGE_DEFINED'
                    , panel='SIDEBAR'
                )
                , VisualConfigComponent(
                    rendered_otype='CUSTOM_FIELD'
                    , rendered_oid=8
                    , page_defined_type=None
                    , component_type='BUILT_IN'
                    , panel='MAIN'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog.tags'
                    , component_type='PAGE_DEFINED'
                    , panel='SIDEBAR'
                )
                , VisualGroupedComponent(
                    label='Referenced By'
                    , open_by_default=None
                    , panel='SIDEBAR'
                    , is_group=None
                    , components=[
                        VisualConfigComponent(
                            rendered_otype=None
                            , rendered_oid=None
                            , page_defined_type='catalog.mentioned_on'
                            , component_type='PAGE_DEFINED'
                            , panel='SIDEBAR'
                        )
                        , VisualConfigComponent(
                            rendered_otype=None
                            , rendered_oid=None
                            , page_defined_type='catalog.article_backreferences'
                            , component_type='PAGE_DEFINED'
                            , panel='SIDEBAR'
                        )
                        , VisualConfigComponent(
                            rendered_otype=None
                            , rendered_oid=None
                            , page_defined_type='catalog.objectset_backreferences'
                            , component_type='PAGE_DEFINED'
                            , panel='SIDEBAR'
                        )
                    ]
                )
            ]
            , id=20
        )

        self.assertEqual(input_transformed, output)

    def test_visual_config_item_model(self):
        # Expected input
        input = VisualConfigItem(
            title='Folder'
            , layout_otype='glossary_v3'
            , component_list_in_config=[
                VisualConfigComponent(
                    rendered_otype='CUSTOM_FIELD'
                    , rendered_oid=4
                    , page_defined_type=None
                    , component_type='BUILT_IN'
                    , panel='MAIN'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog_document_collection.document_collection_links_table'
                    , component_type='PAGE_DEFINED'
                    , panel='MAIN'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog_document_collection.properties'
                    , component_type='PAGE_DEFINED'
                    , panel='SIDEBAR'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog.membership_to_domains'
                    , component_type='PAGE_DEFINED'
                    , panel='SIDEBAR'
                )
                , VisualConfigComponent(
                    rendered_otype='CUSTOM_FIELD'
                    , rendered_oid=8
                    , page_defined_type=None
                    , component_type='BUILT_IN'
                    , panel='MAIN'
                )
                , VisualConfigComponent(
                    rendered_otype=None
                    , rendered_oid=None
                    , page_defined_type='catalog.tags'
                    , component_type='PAGE_DEFINED'
                    , panel='SIDEBAR'
                )
                , VisualGroupedComponent(
                    label='Referenced By'
                    , open_by_default=None
                    , panel='SIDEBAR'
                    , is_group=None
                    , components=[
                        VisualConfigComponent(
                            rendered_otype=None
                            , rendered_oid=None
                            , page_defined_type='catalog.mentioned_on'
                            , component_type='PAGE_DEFINED'
                            , panel='SIDEBAR'
                        )
                        , VisualConfigComponent(
                            rendered_otype=None
                            , rendered_oid=None
                            , page_defined_type='catalog.article_backreferences'
                            , component_type='PAGE_DEFINED'
                            , panel='SIDEBAR'
                        )
                        , VisualConfigComponent(
                            rendered_otype=None
                            , rendered_oid=None
                            , page_defined_type='catalog.objectset_backreferences'
                            , component_type='PAGE_DEFINED'
                            , panel='SIDEBAR'
                        )
                    ]
                )
            ]
        )

        # Transformation
        input_transformed = input.generate_api_payload()

        # Expected Output
        output = {
            "component_list_in_config": [
                {
                    "rendered_otype": "CUSTOM_FIELD",
                    "rendered_oid": 4,
                    "page_defined_type": None,
                    "component_type": "BUILT_IN",
                    "panel": "MAIN"
                },
                {
                    "rendered_otype": None,
                    # "rendered_oid": None,
                    "page_defined_type": "catalog_document_collection.document_collection_links_table",
                    "component_type": "PAGE_DEFINED",
                    "panel": "MAIN"
                },
                {
                    "rendered_otype": None,
                    # "rendered_oid": None,
                    "page_defined_type": "catalog_document_collection.properties",
                    "component_type": "PAGE_DEFINED",
                    "panel": "SIDEBAR"
                },
                {
                    "rendered_otype": None,
                    # "rendered_oid": None,
                    "page_defined_type": "catalog.membership_to_domains",
                    "component_type": "PAGE_DEFINED",
                    "panel": "SIDEBAR"
                },
                {
                    "rendered_otype": "CUSTOM_FIELD",
                    "rendered_oid": 8,
                    "page_defined_type": None,
                    "component_type": "BUILT_IN",
                    "panel": "MAIN"
                },
                {
                    "rendered_otype": None,
                    # "rendered_oid": None,
                    "page_defined_type": "catalog.tags",
                    "component_type": "PAGE_DEFINED",
                    "panel": "SIDEBAR"
                },
                {
                    "label": "Referenced By",
                    "components": [
                        {
                            "rendered_otype": None,
                            # "rendered_oid": None,
                            "page_defined_type": "catalog.mentioned_on",
                            "component_type": "PAGE_DEFINED",
                            "panel": "SIDEBAR"
                        },
                        {
                            "rendered_otype": None,
                            # "rendered_oid": None,
                            "page_defined_type": "catalog.article_backreferences",
                            "component_type": "PAGE_DEFINED",
                            "panel": "SIDEBAR"
                        },
                        {
                            "rendered_otype": None,
                            # "rendered_oid": None,
                            "page_defined_type": "catalog.objectset_backreferences",
                            "component_type": "PAGE_DEFINED",
                            "panel": "SIDEBAR"
                        }
                    ],
                    # "open_by_default": None,
                    "panel": "SIDEBAR",
                    # "is_group": None
                }
            ],
            "title": "Folder",
            "layout_otype": "glossary_v3"
        }

        self.assertEqual(input_transformed, output)