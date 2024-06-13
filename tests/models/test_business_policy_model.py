import unittest
from allie_sdk.methods.business_policy import *


class TestBusinessPolicyModels(unittest.TestCase):

    def test_business_policy_model(self):
        
        # Expected input
        input = dict(
            id=1
            , title='Policy 1'
            , description='Policy wording ...'
            , otype='business_policy'
            , ts_created='2023-05-15T13:27:34.347166Z'
            , url='/policy/1/'
            , stewards=
                [
                    {
                        "otype": "user",
                        "otype_display_name": "User",
                        "id": 6,
                        "name": "Diethard Steiner",
                        "title": "",
                        "url": "/user/6/",
                        "deleted": False,
                        "snippet": "",
                        "photo_url": "/static/img/user.png",
                        "email": "diethard.steiner@outlook.com"
                    }
                ]
        )

        # Transformation
        input_transformed = BusinessPolicy(**input)

        # Expected Output
        output = BusinessPolicy(
            id=1
            , title='Policy 1'
            , description='Policy wording ...'
            , otype='business_policy'
            , ts_created='2023-05-15T13:27:34.347166Z'
            , url='/policy/1/'
            , stewards = [
                dict( # <= standard dict here because the data class will automatically convert this to the BusinessPolicyStewardsField class via the __init__ method
                    otype = "user"
                    , otype_display_name = "User"
                    , id = 6
                    , name = "Diethard Steiner"
                    , title = ""
                    , url = "/user/6/"
                    , deleted = False
                    , snippet = ""
                    , photo_url = "/static/img/user.png"
                    , email = "diethard.steiner@outlook.com"
                )
            ]
        )

        self.assertEqual(input_transformed, output)
    
    def test_business_policy_post_item_model(self):

        # Expected Input
        input = BusinessPolicyPostItem(
            title = "A Financial Policy"
            , description = "Lorem ipsum ... bibendum euismod erat. Nulla vitae justo ac. "
            , template_id = 43
            , fields = [
                CustomFieldValueItem(
                    field_id = 8
                    , value = [
                        CustomFieldDictValueItem(
                            otype = "user"
                            , oid = 3
                        )
                        , CustomFieldDictValueItem(
                            otype = "groupprofile"
                            , oid = 3
                        )
                    ]
                )
            ]
            , policy_group_ids = [1, 3]
        )

        # Transformation
        input_transformed = input.generate_api_post_payload()

        # Expected Output
        output = {
                "title": "A Financial Policy",
                "description": "Lorem ipsum ... bibendum euismod erat. Nulla vitae justo ac. ",
                "template_id": 43,
                "fields": [
                    {
                        "field_id": 8,
                        "value": [
                        {
                            "otype": "user",
                            "oid": 3
                        },
                        {
                            "otype": "groupprofile",
                            "oid": 3
                        }
                        ]
                    }
                ],
                "policy_group_ids": [
                    1,
                    3
                ]
            }

        self.assertEqual(input_transformed, output)
    
    def test_business_policy_put_item(self):

        # Expected input
        input = BusinessPolicyPutItem(
            id = 1
            , title = "A Financial Policy"
            , description = "Lorem ipsum ... bibendum euismod erat. Nulla vitae justo ac. "
            , template_id = 43
            , fields = [
                CustomFieldValueItem(
                    field_id = 8
                    , value = [
                        CustomFieldDictValueItem(
                            otype = "user"
                            , oid = 3
                        )
                        , CustomFieldDictValueItem(
                            otype = "groupprofile"
                            , oid = 3
                        )
                    ]
                )
            ]
            , policy_group_ids = BusinessPolicyGroupIds(
                remove = [ 1, 2 ]
            )
        )

        # Transformation
        input_transformed = input.generate_api_put_payload()

        # Expected output
        output = {
                "id": 1,
                "title": "A Financial Policy",
                "description": "Lorem ipsum ... bibendum euismod erat. Nulla vitae justo ac. ",
                "template_id": 43,
                "fields": [
                    {
                        "field_id": 8,
                        "value": [
                        {
                            "otype": "user",
                            "oid": 3
                        },
                        {
                            "otype": "groupprofile",
                            "oid": 3
                        }
                        ]
                    }
                ],
                "policy_group_ids": {
                    "remove": [
                        1,
                        2
                    ]
                }
            }

        self.assertEqual(input_transformed, output)