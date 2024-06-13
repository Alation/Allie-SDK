import unittest
from allie_sdk.methods.policy_group import *


class TestPolicyGroupsModels(unittest.TestCase):

    def test_basic_policy_group_model(self):

        # Expected input
        input = dict(
            description = "All Policies governing human resources"
            , title = "HR policies"
            , id = 2
            , otype='policy_group'
            , ts_created='2023-05-15T13:27:34.347166Z'
            , url='/policy_group/1/'
            , stewards=[]
            , policies_count = 0
        )
        
        # Transformation
        input_transformed = PolicyGroup.from_api_response(input)

        # Expected output
        output = PolicyGroup(
            description = "All Policies governing human resources"
            , title = "HR policies"
            , id = 2
            , otype='policy_group'
            , ts_created='2023-05-15T13:27:34.347166Z'
            , url='/policy_group/1/'
            , stewards=[]
            , policies_count = 0
        )

        self.assertEqual(input_transformed, output)