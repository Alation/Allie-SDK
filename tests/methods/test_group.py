import requests_mock
from allie_sdk.methods.group import *



MOCK_USER = AlationGroup(
    access_token='test'
    , session=requests.session()
    , host='https://test.com'
)

def test_get_groups(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the Get Group request?
    group_api_response = [
        {
            "display_name": "Stewards",
            "email": "stewards@mycompany.com",
            "id": 10,
            "profile_id": 10,
            "url": "/group/10/"
        }
        , {
            "display_name": "DataGov",
            "email": "datagov@mycompany.com",
            "id": 11,
            "profile_id": 11,
            "url": "/group/11/"
        }
    ]

    success_groups = [ Group.from_api_response(item) for item in group_api_response ]

    # Override the policy API call
    requests_mock.register_uri(
        method = 'GET'
        , url = '/integration/v1/group/'
        , json = group_api_response
        , status_code = 200
    )

    # --- TEST THE FUNCTION --- #
    groups = MOCK_USER.get_groups()

    assert success_groups == groups