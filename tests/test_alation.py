"""Verify CDE credential ownership through the public Alation entry point."""

import pytest
from requests_mock import Mocker

from allie_sdk import Alation
from allie_sdk.methods.cdm_critical_data_element import AlationCDMCriticalDataElement

HOST = "https://test.com"
ALATION_TOKEN = "alation-access-token"
AUTH_URL = f"{HOST}/cde-service/integration/auth/"
ELEMENTS_URL = f"{HOST}/cde-service/integration/cde/"


@pytest.fixture
def alation_client(requests_mock: Mocker) -> Alation:
    """Create an authenticated client without permitting real HTTP requests.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.

    Returns:
        Alation: Client with a validated access token and an empty CDE cache.
    """
    requests_mock.post(
        f"{HOST}/integration/v1/validateAPIAccessToken/",
        json={"api_access_token": ALATION_TOKEN},
    )
    return Alation(host=HOST, access_token=ALATION_TOKEN)


@pytest.mark.parametrize("authentication_mode", ["access", "refresh", "oauth", "disabled"])
def test_cde_authentication_is_lazy(requests_mock: Mocker, authentication_mode: str) -> None:
    """Construct Alation in each authentication mode without contacting CDE.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        authentication_mode (str): Authentication constructor path to exercise.

    Returns:
        None: Asserts that CDE is first contacted by a CDE method call.
    """
    requests_mock.post(f"{HOST}/integration/v1/validateAPIAccessToken/", json={"api_access_token": ALATION_TOKEN})
    requests_mock.post(f"{HOST}/integration/v1/validateRefreshToken/", json={"token_status": "ACTIVE"})
    requests_mock.post(f"{HOST}/integration/v1/createAPIAccessToken/", json={"api_access_token": ALATION_TOKEN})
    requests_mock.post(f"{HOST}/oauth/v2/token", json={"access_token": ALATION_TOKEN})
    authentication = requests_mock.post(AUTH_URL, text="cde-token")
    requests_mock.get(ELEMENTS_URL, json=[])

    if authentication_mode == "access":
        client = Alation(host=HOST, access_token=ALATION_TOKEN)
    elif authentication_mode == "refresh":
        client = Alation(host=HOST, user_id=1, refresh_token="refresh-token")
    elif authentication_mode == "oauth":
        client = Alation(host=HOST, client_id="client", client_secret="secret")
    else:
        client = Alation(host=HOST, disable_authentication=True)
        assert requests_mock.call_count == 0
        with pytest.raises(ValueError, match="No Alation API token available"):
            client.cdm_critical_data_element.get_critical_data_elements()
        client.access_token = ALATION_TOKEN

    assert authentication.call_count == 0
    assert client.cdm_critical_data_element.get_critical_data_elements() == []
    assert authentication.call_count == 1
    assert authentication.last_request.headers["token"] == ALATION_TOKEN


@pytest.mark.parametrize("explicit_token", [None, ALATION_TOKEN])
def test_explicit_exchange_populates_shared_cache(
    requests_mock: Mocker, alation_client: Alation, explicit_token: str | None
) -> None:
    """Reuse an explicit exchange for the configured identity on subsequent calls.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        alation_client (Alation): Authenticated SDK client.
        explicit_token (str | None): Default or explicitly supplied configured token.

    Returns:
        None: Asserts explicit exchanges refresh the cache without an extra lazy exchange.
    """
    authentication = requests_mock.post(AUTH_URL, [{"text": "first-cde-token"}, {"text": "second-cde-token"}])
    requests_mock.get(ELEMENTS_URL, json=[])

    for expected_token in ("first-cde-token", "second-cde-token"):
        response = alation_client.cdm_authentication.create_cde_token(alation_token=explicit_token)
        assert response.token == expected_token
        alation_client.cdm_critical_data_element.get_critical_data_elements()
        assert requests_mock.last_request.headers["CDEToken"] == expected_token

    assert authentication.call_count == 2


@pytest.mark.parametrize("warm_cache", [False, True])
def test_exchange_for_another_identity_does_not_replace_shared_credentials(
    requests_mock: Mocker, alation_client: Alation, warm_cache: bool
) -> None:
    """Keep per-call credential overrides isolated from the configured identity.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        alation_client (Alation): Authenticated SDK client.
        warm_cache (bool): Whether to obtain the configured identity's CDE token first.

    Returns:
        None: Asserts overrides neither seed nor replace the shared CDE cache.
    """
    configured_exchange = requests_mock.post(AUTH_URL, text="configured-cde-token")
    override_exchange = requests_mock.post(AUTH_URL, request_headers={"token": "other-identity"}, text="other-cde-token")
    requests_mock.get(ELEMENTS_URL, json=[])
    if warm_cache:
        alation_client.cdm_critical_data_element.get_critical_data_elements()

    response = alation_client.cdm_authentication.create_cde_token(alation_token="other-identity")
    alation_client.cdm_critical_data_element.get_critical_data_elements()

    assert response.token == "other-cde-token"
    assert override_exchange.call_count == 1
    assert configured_exchange.call_count == 1
    assert alation_client.access_token == ALATION_TOKEN
    assert alation_client.cdm_authentication.access_token == ALATION_TOKEN
    assert requests_mock.last_request.headers["CDEToken"] == "configured-cde-token"


def test_access_token_rotation_invalidates_all_cde_clients(requests_mock: Mocker, alation_client: Alation) -> None:
    """Propagate a parent credential replacement to existing CDE consumers.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        alation_client (Alation): Authenticated SDK client.

    Returns:
        None: Asserts consumers exchange once for each distinct parent credential.
    """
    authentication = requests_mock.post(AUTH_URL, [{"text": "first-cde-token"}, {"text": "second-cde-token"}])
    requests_mock.get(ELEMENTS_URL, json=[])
    another_client = AlationCDMCriticalDataElement(
        session=alation_client.cdm_authentication.s, host=HOST, token_manager=alation_client._cde_token_manager
    )
    alation_client.cdm_critical_data_element.get_critical_data_elements()

    alation_client.access_token = "replacement-alation-token"
    assert alation_client.cdm_authentication.access_token == "replacement-alation-token"
    assert another_client.access_token == "replacement-alation-token"
    another_client.get_critical_data_elements()
    alation_client.access_token = "replacement-alation-token"
    alation_client.cdm_critical_data_element.get_critical_data_elements()

    assert authentication.call_count == 2
    assert [request.headers["token"] for request in authentication.request_history] == [ALATION_TOKEN, "replacement-alation-token"]
    assert requests_mock.last_request.headers["CDEToken"] == "second-cde-token"


@pytest.mark.parametrize("cleared_token", [None, ""])
def test_clearing_parent_credentials_discards_cached_token(
    requests_mock: Mocker, alation_client: Alation, cleared_token: str | None
) -> None:
    """Block cached authentication after clearing and exchange again after restoring.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        alation_client (Alation): Authenticated SDK client.
        cleared_token (str | None): Empty value used to clear parent credentials.

    Returns:
        None: Asserts credentials cannot survive a clear-and-restore cycle.
    """
    authentication = requests_mock.post(AUTH_URL, [{"text": "first-cde-token"}, {"text": "second-cde-token"}])
    data_request = requests_mock.get(ELEMENTS_URL, json=[])
    alation_client.cdm_critical_data_element.get_critical_data_elements()

    alation_client.access_token = cleared_token
    with pytest.raises(ValueError, match="No Alation API token available"):
        alation_client.cdm_critical_data_element.get_critical_data_elements()
    with pytest.raises(ValueError, match="No Alation API token available"):
        alation_client.cdm_authentication.create_cde_token()
    assert authentication.call_count == 1
    assert data_request.call_count == 1

    alation_client.access_token = ALATION_TOKEN
    alation_client.cdm_critical_data_element.get_critical_data_elements()
    assert authentication.call_count == 2
    assert requests_mock.last_request.headers["CDEToken"] == "second-cde-token"


def test_separate_alation_instances_have_isolated_caches(requests_mock: Mocker, alation_client: Alation) -> None:
    """Keep independently constructed clients isolated even with identical credentials.

    Args:
        requests_mock (Mocker): Fixture intercepting HTTP requests.
        alation_client (Alation): First authenticated SDK client.

    Returns:
        None: Asserts each Alation instance obtains and retains its own CDE token.
    """
    authentication = requests_mock.post(AUTH_URL, [{"text": "first-cde-token"}, {"text": "second-cde-token"}])
    requests_mock.get(ELEMENTS_URL, json=[])
    another_client = Alation(host=HOST, access_token=ALATION_TOKEN)

    alation_client.cdm_critical_data_element.get_critical_data_elements()
    another_client.cdm_critical_data_element.get_critical_data_elements()
    assert requests_mock.last_request.headers["CDEToken"] == "second-cde-token"
    alation_client.cdm_critical_data_element.get_critical_data_elements()
    assert requests_mock.last_request.headers["CDEToken"] == "first-cde-token"
    assert authentication.call_count == 2
