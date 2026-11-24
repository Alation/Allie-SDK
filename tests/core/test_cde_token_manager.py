"""Verify shared CDE token lifecycles across independently constructed consumers."""

import pytest
import requests
from requests_mock import Mocker

from allie_sdk.core.cde_token_manager import CDETokenManager
from allie_sdk.methods.cdm_authentication import AlationCDMAuthentication
from allie_sdk.methods.cdm_critical_data_element import AlationCDMCriticalDataElement

HOST = "https://test.com"
AUTH_URL = f"{HOST}/cde-service/integration/auth/"
ELEMENTS_URL = f"{HOST}/cde-service/integration/cde/"


@pytest.mark.parametrize("rejected_status", [401, 403])
def test_shared_refresh_is_reused_by_other_consumers(requests_mock: Mocker, rejected_status: int) -> None:
    """Share explicit creation, rejection recovery and later requests through one manager.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        rejected_status (int): Authentication rejection causing the single retry.

    Returns:
        None: Asserts two consumers reuse both the original and refreshed CDE token.
    """
    manager = CDETokenManager("alation-token")
    session = requests.Session()
    authentication_client = AlationCDMAuthentication(session=session, host=HOST, token_manager=manager)
    first_client = AlationCDMCriticalDataElement(session=session, host=HOST, token_manager=manager)
    second_client = AlationCDMCriticalDataElement(session=session, host=HOST, token_manager=manager)
    authentication = requests_mock.post(AUTH_URL, [{"text": "first-token"}, {"text": "refreshed-token"}])
    data_request = requests_mock.get(ELEMENTS_URL, [{"status_code": rejected_status}, {"json": []}])

    assert authentication.call_count == 0
    authentication_client.create_cde_token()
    first_client.get_critical_data_elements()
    second_client.get_critical_data_elements()

    assert authentication.call_count == 2
    assert [request.headers["CDEToken"] for request in data_request.request_history] == [
        "first-token", "refreshed-token", "refreshed-token"
    ]
    assert all("Token" not in request.headers and "Authorization" not in request.headers for request in data_request.request_history)


def test_failed_refresh_does_not_restore_rejected_credentials(requests_mock: Mocker) -> None:
    """Retry the exchange after a failed refresh instead of reusing a rejected token.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.

    Returns:
        None: Asserts exchange failures propagate and rejected credentials stay discarded.
    """
    manager = CDETokenManager("alation-token")
    client = AlationCDMCriticalDataElement(session=requests.Session(), host=HOST, token_manager=manager)
    authentication = requests_mock.post(AUTH_URL, [
        {"text": "rejected-token"}, {"status_code": 401, "text": "invalid credentials"}, {"text": "fresh-token"}
    ])
    data_request = requests_mock.get(ELEMENTS_URL, [{"status_code": 401}, {"json": []}])

    with pytest.raises(requests.HTTPError) as exception:
        client.get_critical_data_elements()
    assert exception.value.response.status_code == 401
    assert data_request.call_count == 1

    client.get_critical_data_elements()
    assert authentication.call_count == 3
    assert data_request.last_request.headers["CDEToken"] == "fresh-token"


@pytest.mark.parametrize("credential_owner", ["authentication", "elements"])
def test_replacing_a_consumer_credential_invalidates_shared_state(requests_mock: Mocker, credential_owner: str) -> None:
    """Retain direct access-token replacement support when consumers share a manager.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        credential_owner (str): Consumer on which the credential is replaced.

    Returns:
        None: Asserts sibling consumers use the new credential and a fresh CDE token.
    """
    manager = CDETokenManager("original-alation-token")
    session = requests.Session()
    authentication_client = AlationCDMAuthentication(session=session, host=HOST, token_manager=manager)
    elements_client = AlationCDMCriticalDataElement(session=session, host=HOST, token_manager=manager)
    authentication = requests_mock.post(AUTH_URL, [{"text": "first-token"}, {"text": "fresh-token"}])
    requests_mock.get(ELEMENTS_URL, json=[])
    elements_client.get_critical_data_elements()

    if credential_owner == "authentication":
        authentication_client.access_token = "replacement-alation-token"
    else:
        elements_client.access_token = "replacement-alation-token"
    authentication_client.create_cde_token()
    elements_client.get_critical_data_elements()

    assert elements_client.access_token == authentication_client.access_token == "replacement-alation-token"
    assert authentication.call_count == 2
    assert authentication.last_request.headers["token"] == "replacement-alation-token"
    assert requests_mock.last_request.headers["CDEToken"] == "fresh-token"


@pytest.mark.parametrize("client_class", [AlationCDMAuthentication, AlationCDMCriticalDataElement])
def test_conflicting_constructor_credentials_are_rejected(
    client_class: type[AlationCDMAuthentication] | type[AlationCDMCriticalDataElement],
) -> None:
    """Reject ambiguous identities instead of silently changing shared credentials.

    Args:
        client_class (type[AlationCDMAuthentication] | type[AlationCDMCriticalDataElement]):
            Consumer constructor receiving the conflicting arguments.

    Returns:
        None: Asserts a conflicting credential raises without altering the manager.
    """
    manager = CDETokenManager("configured-alation-token")

    with pytest.raises(ValueError, match="access_token must match"):
        client_class(access_token="other-alation-token", session=requests.Session(), host=HOST, token_manager=manager)

    assert manager.access_token == "configured-alation-token"
