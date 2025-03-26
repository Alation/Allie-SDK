"""Test the Alation REST API Visual Config Methods."""

import requests_mock
import unittest

import allie_sdk as allie
from allie_sdk.methods.visual_config import *


class TestVisualConfig(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationVisualConfig(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_visual_configs(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        api_response = [
            {
                # currently the collection_type_id is not returned
                'id': 1
                , 'component_list_in_config': [
                    {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.source_comments', 'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                    , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'MAIN'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.sample_columns', 'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.sample_content', 'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.published_queries', 'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.sql_view', 'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.table_sql_view', 'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.used_by', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.membership_to_domains', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                    , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.tags', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.properties', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                    , {'label': 'Referenced By', 'components': [
                            {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.mentioned_on', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                            , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.article_backreferences', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                            , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.objectset_backreferences', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                        ]
                        , 'open_by_default': True
                        , 'panel': 'SIDEBAR'
                        , 'is_group': True
                    }
                    , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.policy_backreference', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                ]
                , 'title': 'Table custom fields'
                , 'layout_otype': 'table'
            }
        ]

        # success_response = [VisualConfig.from_api_response(item) for item in api_response]
        success_response = [
            VisualConfig(
                # currently the collection_type_id is not returned
                title='Table custom fields'
                , layout_otype='table'
                , component_list_in_config=[
                    VisualConfigComponent(
                        rendered_otype=None
                        , rendered_oid=None
                        , page_defined_type='catalog.source_comments'
                        , component_type='PAGE_DEFINED'
                        , panel='MAIN'
                    )
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None, component_type='BUILT_IN', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_table.sample_columns', component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_table.sample_content', component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_table.published_queries', component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_table.sql_view', component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_table.table_sql_view', component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.used_by', component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.membership_to_domains', component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None, component_type='BUILT_IN', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.tags', component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_table.properties', component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualGroupedComponent(
                        label='Referenced By'
                        , open_by_default=True
                        , panel='SIDEBAR'
                        , is_group=True
                        , components=[
                            VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.mentioned_on', component_type='PAGE_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.article_backreferences', component_type='PAGE_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.objectset_backreferences', component_type='PAGE_DEFINED', panel='SIDEBAR')
                        ]
                    )
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.policy_backreference', component_type='PAGE_DEFINED', panel='SIDEBAR')
                ]
                , id=1
            )
        ]

        # Override the visual config API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/visual_config/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_response = self.mock_user.get_visual_configs()

        self.assertEqual(success_response, actual_response)

    @requests_mock.Mocker()
    def test_get_a_visual_config(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        api_response = {
                # currently the collection_type_id is not returned
                'id': 1
                , 'component_list_in_config': [
                {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.source_comments',
                 'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None,
                   'component_type': 'BUILT_IN', 'panel': 'MAIN'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.sample_columns',
                   'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.sample_content',
                   'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.published_queries',
                   'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.sql_view',
                   'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.table_sql_view',
                   'component_type': 'PAGE_DEFINED', 'panel': 'MAIN'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.used_by',
                   'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.membership_to_domains',
                   'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None,
                   'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.tags',
                   'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_table.properties',
                   'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                , {'label': 'Referenced By', 'components': [
                    {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.mentioned_on',
                     'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
                    , {'rendered_otype': None, 'rendered_oid': None,
                       'page_defined_type': 'catalog.article_backreferences', 'component_type': 'PAGE_DEFINED',
                       'panel': 'SIDEBAR'}
                    , {'rendered_otype': None, 'rendered_oid': None,
                       'page_defined_type': 'catalog.objectset_backreferences', 'component_type': 'PAGE_DEFINED',
                       'panel': 'SIDEBAR'}
                ]
                    , 'open_by_default': True
                    , 'panel': 'SIDEBAR'
                    , 'is_group': True
                   }
                , {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.policy_backreference',
                   'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}
            ]
                , 'title': 'Table custom fields'
                , 'layout_otype': 'table'
        }


        # success_response = [VisualConfig.from_api_response(item) for item in api_response]
        success_response = VisualConfig(
                # currently the collection_type_id is not returned
                title='Table custom fields'
                , layout_otype='table'
                , component_list_in_config=[
                    VisualConfigComponent(
                        rendered_otype=None
                        , rendered_oid=None
                        , page_defined_type='catalog.source_comments'
                        , component_type='PAGE_DEFINED'
                        , panel='MAIN'
                    )
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None,
                                            component_type='BUILT_IN', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog_table.sample_columns',
                                            component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog_table.sample_content',
                                            component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog_table.published_queries',
                                            component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog_table.sql_view', component_type='PAGE_DEFINED',
                                            panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog_table.table_sql_view',
                                            component_type='PAGE_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.used_by',
                                            component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog.membership_to_domains',
                                            component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None,
                                            component_type='BUILT_IN', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.tags',
                                            component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog_table.properties', component_type='PAGE_DEFINED',
                                            panel='SIDEBAR')
                    , VisualGroupedComponent(
                        label='Referenced By'
                        , open_by_default=True
                        , panel='SIDEBAR'
                        , is_group=True
                        , components=[
                            VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                                  page_defined_type='catalog.mentioned_on',
                                                  component_type='PAGE_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                                    page_defined_type='catalog.article_backreferences',
                                                    component_type='PAGE_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                                    page_defined_type='catalog.objectset_backreferences',
                                                    component_type='PAGE_DEFINED', panel='SIDEBAR')
                        ]
                    )
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                            page_defined_type='catalog.policy_backreference',
                                            component_type='PAGE_DEFINED', panel='SIDEBAR')
                ]
                , id=1
            )


        # Override the visual config API call
        VISUAL_CONFIG_ID = 1

        requests_mock.register_uri(
            method='GET',
            url=f'/integration/visual_config/{VISUAL_CONFIG_ID}/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_response = self.mock_user.get_a_visual_config(
            visual_config_id=VISUAL_CONFIG_ID
        )

        self.assertEqual(success_response, actual_response)

    @requests_mock.Mocker()
    def test_create_visual_config(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        api_response = {'id': 43, 'component_list_in_config': [{'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog_document.document_children', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'MAIN'}, {'label': 'Data Product Info', 'components': [{'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10011, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10012, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10013, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10014, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10015, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}], 'open_by_default': True, 'panel': 'MAIN', 'is_group': True}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10017, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10016, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10018, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}, {'label': 'Owners', 'components': [{'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10019, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'SIDEBAR'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10020, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'SIDEBAR'}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}], 'open_by_default': True, 'panel': 'SIDEBAR', 'is_group': True}, {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10021, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'SIDEBAR'}, {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.membership_to_domains', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}, {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.tags', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}, {'label': 'Referenced By', 'components': [{'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.mentioned_on', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}, {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.article_backreferences', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}, {'rendered_otype': None, 'rendered_oid': None, 'page_defined_type': 'catalog.objectset_backreferences', 'component_type': 'PAGE_DEFINED', 'panel': 'SIDEBAR'}], 'open_by_default': True, 'panel': 'SIDEBAR', 'is_group': True}], 'title': 'Data Product', 'layout_otype': 'glossary_term'}

        # What is the expected response?
        success_response = allie.JobDetails(status='successful', msg='', result=VisualConfig(title='Data Product', layout_otype='glossary_term', component_list_in_config=[VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_document.document_children', component_type='PAGE_DEFINED', panel='SIDEBAR'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None, component_type='BUILT_IN', panel='MAIN'), VisualGroupedComponent(label='Data Product Info', open_by_default=True, panel='MAIN', is_group=True, components=[VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10013, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10014, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10015, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')]), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10017, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10016, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10018, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN'), VisualGroupedComponent(label='Owners', open_by_default=True, panel='SIDEBAR', is_group=True, components=[VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10019, page_defined_type=None, component_type='USER_DEFINED', panel='SIDEBAR'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10020, page_defined_type=None, component_type='USER_DEFINED', panel='SIDEBAR'), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None, component_type='BUILT_IN', panel='SIDEBAR')]), VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10021, page_defined_type=None, component_type='USER_DEFINED', panel='SIDEBAR'), VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.membership_to_domains', component_type='PAGE_DEFINED', panel='SIDEBAR'), VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.tags', component_type='PAGE_DEFINED', panel='SIDEBAR'), VisualGroupedComponent(label='Referenced By', open_by_default=True, panel='SIDEBAR', is_group=True, components=[VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.mentioned_on', component_type='PAGE_DEFINED', panel='SIDEBAR'), VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.article_backreferences', component_type='PAGE_DEFINED', panel='SIDEBAR'), VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.objectset_backreferences', component_type='PAGE_DEFINED', panel='SIDEBAR')])], id=43))

        # Override the visual config API call
        requests_mock.register_uri(
            method='POST',
            url=f'/integration/visual_config/',
            json=api_response,
            status_code=201
        )

        # --- TEST THE FUNCTION --- #
        actual_response = self.mock_user.create_visual_config(
            visual_config = VisualConfigItem(
                collection_type_id = 2
                , title='Data Product'
                , layout_otype='glossary_term'
                , component_list_in_config=[
                    VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog_document.document_children', component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None, component_type='BUILT_IN', panel='MAIN')
                    , VisualGroupedComponent(label='Data Product Info', open_by_default=True, panel='MAIN', is_group=True, components=[
                            VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10013, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10014, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10015, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                        ]
                    )
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10017, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10016, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10018, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                    , VisualGroupedComponent(label='Owners', open_by_default=True, panel='SIDEBAR', is_group=True, components=[
                            VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10019, page_defined_type=None, component_type='USER_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10020, page_defined_type=None, component_type='USER_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None, component_type='BUILT_IN', panel='SIDEBAR')
                        ]
                    )
                    , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10021, page_defined_type=None, component_type='USER_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.membership_to_domains', component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.tags', component_type='PAGE_DEFINED', panel='SIDEBAR')
                    , VisualGroupedComponent(label='Referenced By', open_by_default=True, panel='SIDEBAR', is_group=True, components=[
                            VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.mentioned_on', component_type='PAGE_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.article_backreferences', component_type='PAGE_DEFINED', panel='SIDEBAR')
                            , VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.objectset_backreferences', component_type='PAGE_DEFINED', panel='SIDEBAR')
                        ]
                        )
                ]
            )
        )

        self.assertEqual(success_response, actual_response)