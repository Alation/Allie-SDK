import requests_mock
from allie_sdk.methods.policy_group import *

MOCK_USER = AlationPolicyGroup(
    access_token='test'
    , session=requests.session()
    , host='https://test.com'
)

def test_get_policy_groups(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the Get Policy request?
    policy_group_api_response = [
        {
            "description": "All Policies governing human resources",
            "title": "HR policies",
            "id": 2,
            "otype": "policy_group",
            "ts_created": "2022-11-16T07:04:32.888040Z",
            "url": "/policy_group/1/",
            "stewards": [],
            "policies_count": 0
        }
        , {
            "description": "All Policies governing freelancers",
            "title": "HR policies",
            "id": 3,
            "otype": "policy_group",
            "ts_created": "2022-11-17T07:04:32.888040Z",
            "url": "/policy_group/1/",
            "stewards": [],
            "policies_count": 0
        }
    ]

    success_policy_groups = [PolicyGroup(**pg) for pg in policy_group_api_response]

    # Override the policy API call
    requests_mock.register_uri(
        method = 'GET'
        , url = '/integration/v1/policy_group'
        , json = policy_group_api_response
        , status_code = 200
    )

    # --- TEST THE FUNCTION --- #
    policy_groups = MOCK_USER.get_policy_groups()

    assert success_policy_groups == policy_groups