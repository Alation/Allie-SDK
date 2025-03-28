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
                'id': 50
                , 'component_list_in_config': [
                        {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'MAIN'}
                        , {'label': 'Data Product Info', 'components': [
                                {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10011, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                                , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10012, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                            ], 'open_by_default': True, 'panel': 'MAIN', 'is_group': True}
                    , {'label': 'Owners', 'components': [
                            {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}
                        ], 'open_by_default': True, 'panel': 'SIDEBAR', 'is_group': True}
                ], 'title': 'Data Product', 'layout_otype': 'glossary_term'
            }
        ]


        success_response = [
            VisualConfig(
                title='Data Product'
                , layout_otype='glossary_term'
                , component_list_in_config=[
                        VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None, component_type='BUILT_IN', panel='MAIN')
                        , VisualGroupedComponent(label='Data Product Info', open_by_default=True, panel='MAIN', is_group=True, components=[
                                VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                                , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            ]
                        )
                        , VisualGroupedComponent(label='Owners', open_by_default=True, panel='SIDEBAR', is_group=True, components=[
                                VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None, component_type='BUILT_IN', panel='SIDEBAR')
                            ]
                        )
                ]
                , id=50
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
    def test_get_visual_configs_by_otype(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        api_response = [
            {
                'id': 50
                , 'component_list_in_config': [
                {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None,
                 'component_type': 'BUILT_IN', 'panel': 'MAIN'}
                , {'label': 'Data Product Info', 'components': [
                    {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10011, 'page_defined_type': None,
                     'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                    , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10012, 'page_defined_type': None,
                       'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                ], 'open_by_default': True, 'panel': 'MAIN', 'is_group': True}
                , {'label': 'Owners', 'components': [
                    {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None,
                     'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}
                ], 'open_by_default': True, 'panel': 'SIDEBAR', 'is_group': True}
            ], 'title': 'Data Product', 'layout_otype': 'glossary_term'
            }
        ]

        success_response = [
            VisualConfig(
                title='Data Product'
                , layout_otype='glossary_term'
                , component_list_in_config=[
                    VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None,
                                          component_type='BUILT_IN', panel='MAIN')
                    ,
                    VisualGroupedComponent(label='Data Product Info', open_by_default=True, panel='MAIN', is_group=True,
                                           components=[
                                               VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011,
                                                                     page_defined_type=None,
                                                                     component_type='USER_DEFINED', panel='MAIN')
                                               ,
                                               VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012,
                                                                     page_defined_type=None,
                                                                     component_type='USER_DEFINED', panel='MAIN')
                                           ]
                                           )
                    , VisualGroupedComponent(label='Owners', open_by_default=True, panel='SIDEBAR', is_group=True,
                                             components=[
                                                 VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8,
                                                                       page_defined_type=None,
                                                                       component_type='BUILT_IN', panel='SIDEBAR')
                                             ]
                                             )
                ]
                , id=50
            )
        ]

        # Override the visual config API call
        otype = 'glossary_term'
        requests_mock.register_uri(
            method='GET',
            url=f'/integration/visual_config/{otype}/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_response = self.mock_user.get_visual_configs(
            otype=otype
        )

        self.assertEqual(success_response, actual_response)

    @requests_mock.Mocker()
    def test_get_a_visual_config(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        api_response = {
                'id': 50
                , 'component_list_in_config': [
                        {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'MAIN'}
                        , {'label': 'Data Product Info', 'components': [
                                {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10011, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                                , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10012, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                            ], 'open_by_default': True, 'panel': 'MAIN', 'is_group': True}
                    , {'label': 'Owners', 'components': [
                            {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}
                        ], 'open_by_default': True, 'panel': 'SIDEBAR', 'is_group': True}
                ], 'title': 'Data Product', 'layout_otype': 'glossary_term'
            }


        success_response = VisualConfig(
                title='Data Product'
                , layout_otype='glossary_term'
                , component_list_in_config=[
                        VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None, component_type='BUILT_IN', panel='MAIN')
                        , VisualGroupedComponent(label='Data Product Info', open_by_default=True, panel='MAIN', is_group=True, components=[
                                VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                                , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            ]
                        )
                        , VisualGroupedComponent(label='Owners', open_by_default=True, panel='SIDEBAR', is_group=True, components=[
                                VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None, component_type='BUILT_IN', panel='SIDEBAR')
                            ]
                        )
                ]
                , id=50
            )


        # Override the visual config API call
        VISUAL_CONFIG_ID = 50

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

        # What does the response look like for the document request?
        api_response = {
            'id': 45
            , 'component_list_in_config': [
                {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'MAIN'}
                , {'label': 'Data Product Info', 'components': [
                        {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10011, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                        , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10012, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                    ], 'open_by_default': True, 'panel': 'MAIN', 'is_group': True}
                , {'label': 'Owners', 'components': [
                        {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}
                    ], 'open_by_default': True, 'panel': 'SIDEBAR', 'is_group': True}
            ]
            , 'title': 'Data Product'
            , 'layout_otype': 'glossary_term'
        }

        # What is the expected response?
        success_response = allie.JobDetails(
            status='successful'
            , msg=''
            , result=VisualConfig(
                layout_otype='glossary_term'
                , component_list_in_config=[
                        VisualConfigComponent(
                            rendered_otype='CUSTOM_FIELD'
                            , rendered_oid=4
                            , page_defined_type=None
                            , component_type='BUILT_IN'
                            , panel='MAIN'
                        )
                        , VisualGroupedComponent(
                            label='Data Product Info'
                            , open_by_default=True
                            , panel='MAIN'
                            , is_group=True
                            , components=[
                                VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                                , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            ]
                        ), VisualGroupedComponent(
                            label='Owners'
                            , open_by_default=True
                            , panel='SIDEBAR'
                            , is_group=True
                            , components=[
                                    VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None, component_type='BUILT_IN', panel='SIDEBAR')
                                ]
                        )
                ]
                , title = 'Data Product'
                , id=45
            )
        )

        # What is the INPUT?
        # Override the visual config API call
        requests_mock.register_uri(
            method='POST',
            url=f'/integration/visual_config/',
            json=api_response,
            status_code=201
        )

        # --- TEST THE FUNCTION --- #
        actual_response = self.mock_user.create_visual_config(
            VisualConfigItem(
                collection_type_id=2
                , title='Data Product'
                , layout_otype='glossary_term'
                , component_list_in_config=[
                    VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=4
                        , page_defined_type=None
                        , component_type='BUILT_IN'
                        , panel='MAIN'
                    )
                    , VisualGroupedComponent(
                        label='Data Product Info'
                        , open_by_default=True
                        , panel='MAIN'
                        , is_group=True
                        , components=[
                            allie.VisualConfigComponent(
                                rendered_otype='CUSTOM_FIELD'
                                , rendered_oid=10011
                                , page_defined_type=None
                                , component_type='USER_DEFINED'
                                , panel='MAIN'
                            )
                            , allie.VisualConfigComponent(
                                rendered_otype='CUSTOM_FIELD'
                                , rendered_oid=10012
                                , page_defined_type=None
                                , component_type='USER_DEFINED'
                                , panel='MAIN'
                            )
                        ]
                    )
                    , VisualGroupedComponent(
                        label='Owners'
                        , open_by_default=True
                        , panel='SIDEBAR'
                        , is_group=True
                        , components=[
                            allie.VisualConfigComponent(
                                rendered_otype='CUSTOM_FIELD'
                                , rendered_oid=8
                                , page_defined_type=None
                                , component_type='BUILT_IN'
                                , panel='SIDEBAR'
                            )
                        ]
                    )
                ]
            )
        )


        self.assertEqual(success_response, actual_response)

    @requests_mock.Mocker()
    def test_update_visual_config(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        api_response = {
            'id': 50
            , 'component_list_in_config': [
                    {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 4, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'MAIN'}
                    , {'label': 'Data Product Info', 'components': [
                            {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10011, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                            , {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 10012, 'page_defined_type': None, 'component_type': 'USER_DEFINED', 'panel': 'MAIN'}
                        ], 'open_by_default': True, 'panel': 'MAIN', 'is_group': True}
                    , {'label': 'Owners', 'components': [
                            {'rendered_otype': 'CUSTOM_FIELD', 'rendered_oid': 8, 'page_defined_type': None, 'component_type': 'BUILT_IN', 'panel': 'SIDEBAR'}
                        ], 'open_by_default': True, 'panel': 'SIDEBAR', 'is_group': True}
            ]
            , 'title': 'Data Product UPDATED custom fields'
            , 'layout_otype': 'glossary_term'
        }

        # What is the expected response?
        success_response = allie.JobDetails(
            status='successful'
            , msg=''
            , result=VisualConfig(
                title='Data Product UPDATED custom fields'
                , layout_otype='glossary_term'
                , component_list_in_config=[
                        VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None, component_type='BUILT_IN', panel='MAIN')
                        , VisualGroupedComponent(label='Data Product Info', open_by_default=True, panel='MAIN', is_group=True, components=[
                                VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                                , VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012, page_defined_type=None, component_type='USER_DEFINED', panel='MAIN')
                            ]
                        )
                        , VisualGroupedComponent(label='Owners', open_by_default=True, panel='SIDEBAR', is_group=True, components=[
                                VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None, component_type='BUILT_IN', panel='SIDEBAR')
                            ]
                        )
                ]
                , id=50
            )
        )

        # Override the visual config API call
        requests_mock.register_uri(
            method='PUT',
            url=f'/integration/visual_config/50/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_response = self.mock_user.update_visual_config(
            visual_config=allie.VisualConfigItem(
                collection_type_id = 2
                , title='Data Product UPDATED'
                , layout_otype='glossary_term'
                , component_list_in_config=[
                    allie.VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=4
                        , page_defined_type=None
                        , component_type='BUILT_IN'
                        , panel='MAIN'
                    )
                    , allie.VisualGroupedComponent(
                        label='Data Product Info'
                        , open_by_default=True
                        , panel='MAIN'
                        , is_group=True
                        , components=[
                            allie.VisualConfigComponent(
                                rendered_otype='CUSTOM_FIELD'
                                , rendered_oid=10011
                                , page_defined_type=None
                                , component_type='USER_DEFINED'
                                , panel='MAIN'
                            )
                            , allie.VisualConfigComponent(
                                rendered_otype='CUSTOM_FIELD'
                                , rendered_oid=10012
                                , page_defined_type=None
                                , component_type='USER_DEFINED'
                                , panel='MAIN'
                            )
                        ]
                    )
                    , allie.VisualGroupedComponent(
                        label='Owners'
                        , open_by_default=True
                        , panel='SIDEBAR'
                        , is_group=True
                        , components=[
                            allie.VisualConfigComponent(
                                rendered_otype='CUSTOM_FIELD'
                                , rendered_oid=8
                                , page_defined_type=None
                                , component_type='BUILT_IN'
                                , panel='SIDEBAR'
                            )
                        ]
                    )
                ]
            )
            , visual_config_id = 50
        )

        self.assertEqual(success_response, actual_response)

    @requests_mock.Mocker()
    def test_delete_visual_config_error(self, requests_mock):

        # What does the response look like for the document request?
        api_response = {
            "detail": "Delete is not supported for glossary_term"
            , "code": "400000"
        }

        # What is the expected response?
        success_response = allie.JobDetails(
            status='failed'
            , msg=None
            , result={'detail': 'Delete is not supported for glossary_term', 'code': '400000'}
        )

        # Override the visual config API call
        requests_mock.register_uri(
            method='DELETE',
            url=f'/integration/visual_config/50/',
            json=api_response,
            status_code=400
        )

        # --- TEST THE FUNCTION --- #
        actual_response = self.mock_user.delete_visual_config(
            visual_config_id=50
        )

        self.assertEqual(success_response, actual_response)

