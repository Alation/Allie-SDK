import requests_mock
from allie_sdk.methods.domain import *



MOCK_USER = AlationDomain(
    access_token='test'
    , session=requests.session()
    , host='https://test.com'
)

def test_get_domains(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the domain request?
    domain_api_response = [
        {
            "id": 1,
            "title": "Sales",
            "description": "Relevant data and articles for Sales Analytics",
            "parent_id": 2
        }
        , {
            "id": 2,
            "title": "Marketing",
            "description": "Relevant data and articles for Marketing Analytics",
            "parent_id": 2
        }
    ]

    success_domains = [ Domain.from_api_response(item) for item in domain_api_response ]

    # Override the policy API call
    requests_mock.register_uri(
        method = 'GET'
        , url = '/integration/v2/domain/'
        , json = domain_api_response
        , status_code = 200
    )

    # --- TEST THE FUNCTION --- #
    domains = MOCK_USER.get_domains()

    assert success_domains == domains


def test_assign_objects_to_domain(requests_mock):
    # --- PREPARE THE TEST SETUP --- #

    domain_api_response = {'exclude': False, 'id': 179, 'oid': [21, 23], 'otype': 'glossary_v3'}

    # Override the domain API call
    requests_mock.register_uri(
        method = 'POST'
        , url = '/integration/v2/domain/membership/'
        , json = domain_api_response
        , status_code = 201 # 202 if using async
    )

    # --- TEST THE FUNCTION --- #
    create_domain_membership_result = MOCK_USER.assign_objects_to_domain(
        DomainMembership(
            id = 179
            , oid = [21, 23]
            , otype = 'glossary_v3'
        )
    )

    function_expected_result = {'exclude': False, 'id': 179, 'oid': [21, 23], 'otype': 'glossary_v3'}
    assert function_expected_result == create_domain_membership_result