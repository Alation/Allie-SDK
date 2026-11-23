"""Tests for shared REST requests and success response mapping."""

from email import policy
from email.parser import BytesParser
from unittest.mock import patch

import pytest
import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth
from requests_mock import Mocker

from allie_sdk import AuthHeaderType
from allie_sdk.core.request_handler import RequestHandler
from allie_sdk.models.authentication_model import AuthHeaderTypeInput


class TestRequestHandler:

    def setup_method(self) -> None:
        """Configure a request handler for tests expecting bearer authentication.

        Args:
            None.

        Returns:
            None: Initializes the session, host, access token, and request handler.
        """
        self.session = requests.Session()
        self.host = "https://test.alation.com"
        self.access_token = "test_token"
        self.handler = RequestHandler(self.session, self.host, self.access_token, auth_header_type="Authorization")

    @pytest.mark.parametrize("http_method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
    @pytest.mark.parametrize(
        ("auth_header_type", "expected_auth_headers"),
        [
            pytest.param(None, {"Token": "test_token"}, id="default-token"),
            pytest.param("Token", {"Token": "test_token"}, id="explicit-token"),
            pytest.param("Authorization", {"Authorization": "Bearer test_token"}, id="bearer"),
            pytest.param(AuthHeaderType.TOKEN, {"Token": "test_token"}, id="token-enum"),
            pytest.param(AuthHeaderType.BEARER, {"Authorization": "Bearer test_token"}, id="bearer-enum"),
        ],
    )
    def test_authentication_headers(
        self,
        requests_mock: Mocker,
        http_method: str,
        auth_header_type: AuthHeaderTypeInput | None,
        expected_auth_headers: dict[str, str],
    ) -> None:
        """Verify each HTTP method sends only the selected authentication header.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            http_method (str): HTTP method whose authentication header is checked.
            auth_header_type (AuthHeaderTypeInput | None): Explicit authentication mode,
                or None to exercise the constructor's default.
            expected_auth_headers (dict[str, str]): Authentication headers expected
                on the outgoing request, excluding unrelated HTTP headers.

        Returns:
            None: Asserts the request uses the expected header name and token format.
        """
        if auth_header_type is None:
            handler = RequestHandler(self.session, self.host, self.access_token)
        else:
            handler = RequestHandler(self.session, self.host, self.access_token, auth_header_type=auth_header_type)
        requests_mock.register_uri(http_method, f"{self.host}/test/authentication", json={"id": 1})

        request_method = getattr(handler, http_method.lower())
        request_method("/test/authentication", body={"name": "Test"})

        actual_auth_headers = {
            header_name: requests_mock.last_request.headers[header_name]
            for header_name in ("Token", "Authorization")
            if header_name in requests_mock.last_request.headers
        }
        assert actual_auth_headers == expected_auth_headers

    @pytest.mark.parametrize("access_token", [None, "", "test-token"], ids=["no-token", "empty-token", "with-token"])
    @pytest.mark.parametrize("invalid_mode", ["Typo", "Bearer", "token", "", None, 1, ["Token"]])
    def test_invalid_authentication_mode_is_always_rejected(
        self, access_token: str | None, invalid_mode: object
    ) -> None:
        """Reject invalid authentication modes before configuring the caller's session.

        Args:
            access_token (str | None): Token supplied with the invalid mode.
            invalid_mode (object): Unsupported string or non-string authentication mode.

        Returns:
            None: Asserts informative validation errors regardless of token presence.
        """
        with patch.object(self.session, "mount", wraps=self.session.mount) as mount:
            with pytest.raises(ValueError) as exception:
                RequestHandler(
                    self.session, self.host, access_token=access_token,
                    auth_header_type=invalid_mode,  # type: ignore[arg-type]
                )

        message = str(exception.value)
        assert repr(invalid_mode) in message
        assert "'Token'" in message
        assert "'Authorization'" in message
        mount.assert_not_called()

    @pytest.mark.parametrize("http_method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
    @pytest.mark.parametrize("auth_header_type", ["Token", "Authorization", AuthHeaderType.TOKEN, AuthHeaderType.BEARER])
    @pytest.mark.parametrize("initial_token", [None, "original-token"], ids=["initially-unauthenticated", "initially-authenticated"])
    def test_access_token_changes_update_authentication(
        self,
        requests_mock: Mocker,
        http_method: str,
        auth_header_type: AuthHeaderTypeInput,
        initial_token: str | None,
    ) -> None:
        """Send the latest token and remove old credentials when tokens are cleared.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            http_method (str): HTTP verb used after each token update.
            auth_header_type (AuthHeaderTypeInput): Enum member or legacy string mode.
            initial_token (str | None): Initial credentials, if any.

        Returns:
            None: Asserts token rotation, removal and restoration preserve the selected mode.
        """
        handler = RequestHandler(self.session, self.host, initial_token, auth_header_type=auth_header_type)
        expected_mode = AuthHeaderType.TOKEN if auth_header_type == "Token" else AuthHeaderType.BEARER
        assert handler.auth_header_type is expected_mode
        handler.headers["X-Request-ID"] = "preserved"
        handler.headers["authorization" if expected_mode is AuthHeaderType.TOKEN else "token"] = "obsolete-credential"
        requests_mock.register_uri(http_method, f"{self.host}/test/token-changes", json={"id": 1})
        options = {"pagination": False} if http_method == "GET" else {}

        for replacement_token in ("replacement-token", None, "restored-token", ""):
            handler.access_token = replacement_token
            getattr(handler, http_method.lower())("/test/token-changes", body=None, **options)

            expected_authentication = {}
            if replacement_token:
                value = replacement_token if expected_mode is AuthHeaderType.TOKEN else f"Bearer {replacement_token}"
                expected_authentication = {expected_mode.value: value}
            actual_authentication = {
                name: requests_mock.last_request.headers[name]
                for name in ("Token", "Authorization", "CDEToken")
                if name in requests_mock.last_request.headers
            }
            assert actual_authentication == expected_authentication
            assert {name: value for name, value in handler.headers.items() if name in ("Token", "Authorization")} == expected_authentication
            assert handler.access_token == replacement_token
            assert handler.auth_header_type is expected_mode
            assert requests_mock.last_request.headers["X-Request-ID"] == "preserved"
            assert handler.headers["Content-Type"] == "application/json; charset=utf-8"

    
    def test_delete(self, requests_mock):
        requests_mock.delete('https://test.alation.com/test/delete', json={'message': 'Deleted successfully'}, status_code=204)
        result = self.handler.delete('/test/delete')
        assert result == {'msg': '',
         'result': {'message': 'Deleted successfully'},
         'status': 'successful'}
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
    def test_delete_error(self, requests_mock):
        requests_mock.delete('https://test.alation.com/test/delete', json={'error': 'Not found'}, status_code=404)
        with pytest.raises(HTTPError) as context:
            self.handler.delete('/test/delete')
        assert context.value.response.status_code == 404

    
    def test_get(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test'}])
        result = self.handler.get('/test/get')
        assert result == [{'id': 1, 'name': 'Test'}]
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
    def test_get_empty_response(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[])
        result = self.handler.get('/test/get')
        assert result == []

    
    def test_get_error(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json={'error': 'Unauthorized'}, status_code=401)
        with pytest.raises(HTTPError) as context:
            self.handler.get('/test/get')
        assert context.value.response.status_code == 401

    
    def test_get_with_pagination(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test 1'}],
              headers={'X-Next-Page': '/test/get?page=2'})
        requests_mock.get('https://test.alation.com/test/get?page=2', json=[{'id': 2, 'name': 'Test 2'}])
        result = self.handler.get('/test/get')
        assert result == [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}]
        assert requests_mock.call_count == 2

    
    def test_get_with_pagination_error(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test 1'}],
              headers={'X-Next-Page': '/test/get?page=2'})
        requests_mock.get('https://test.alation.com/test/get?page=2', json={'error': 'Server error'}, status_code=500)

        with pytest.raises(HTTPError) as context:
            self.handler.get('/test/get')
        assert context.value.response.status_code == 500

    def test_get_nested_results(self, requests_mock):
        requests_mock.get(
            'https://test.alation.com/test/nested-get',
            json={
                'count': 2,
                'next': '/test/nested-get?limit=1&offset=1',
                'previous': None,
                'results': [{'id': 1, 'name': 'Test 1'}],
            },
        )
        requests_mock.get(
            'https://test.alation.com/test/nested-get?limit=1&offset=1',
            json={
                'count': 2,
                'next': None,
                'previous': '/test/nested-get?limit=1&offset=0',
                'results': [{'id': 2, 'name': 'Test 2'}],
            },
        )

        result = self.handler.get_nested_results('/test/nested-get')

        assert result == [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}]
        assert requests_mock.call_count == 2

    def test_get_nested_results_error(self, requests_mock):
        requests_mock.get(
            'https://test.alation.com/test/nested-get',
            json={
                'count': 2,
                'next': '/test/nested-get?limit=1&offset=1',
                'previous': None,
                'results': [{'id': 1, 'name': 'Test 1'}],
            },
        )
        requests_mock.get(
            'https://test.alation.com/test/nested-get?limit=1&offset=1',
            json={'error': 'Server error'},
            status_code=500,
        )

        with pytest.raises(HTTPError) as context:
            self.handler.get_nested_results('/test/nested-get')

        assert context.value.response.status_code == 500

    
    def test_patch(self, requests_mock):
        requests_mock.patch('https://test.alation.com/test/patch', json={'id': 1, 'name': 'Updated Test'})
        result = self.handler.patch('/test/patch', {'name': 'Updated Test'})
        assert result == {'id': 1, 'name': 'Updated Test'}
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
    def test_patch_error(self, requests_mock):
        requests_mock.patch('https://test.alation.com/test/patch', json={'error': 'Bad request'}, status_code=400)
        with pytest.raises(HTTPError) as context:
            self.handler.patch('/test/patch', {'name': 'Updated Test'})
        assert context.value.response.status_code == 400

    
    def test_post(self, requests_mock):
        requests_mock.post('https://test.alation.com/test/post', json={'id': 2, 'name': 'New Test'})
        result = self.handler.post('/test/post', {'name': 'New Test'})
        assert result == {'id': 2, 'name': 'New Test'}
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    @pytest.mark.parametrize(
        "body",
        [
            pytest.param({"name": "Example +&=", "metadata": {"active": True}}, id="dictionary"),
            pytest.param([{"name": "First"}, {"name": "Second"}], id="list"),
            pytest.param({}, id="empty-dictionary"),
            pytest.param([], id="empty-list"),
        ],
    )
    def test_post_json_body(self, requests_mock: Mocker, body: dict[str, object] | list[object]) -> None:
        """Preserve JSON encoding and bearer authentication for ordinary POSTs.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            body (dict[str, object] | list[object]): JSON payload to send.

        Returns:
            None: Asserts the request retains its JSON content type, data and authentication.
        """
        response_body = {"id": 2}
        requests_mock.post(f"{self.host}/test/post", json=response_body)

        result = self.handler.post("/test/post", body)

        assert result == response_body
        assert requests_mock.last_request.json() == body
        assert requests_mock.last_request.headers["Content-Type"] == "application/json; charset=utf-8"
        assert requests_mock.last_request.headers["Authorization"] == f"Bearer {self.access_token}"
        assert "Token" not in requests_mock.last_request.headers

    @pytest.mark.parametrize("method_name", ["post", "post_paginated"])
    @pytest.mark.parametrize("auth_header_type", [None, "Token", "Authorization"], ids=["no-token", "token", "bearer"])
    @pytest.mark.parametrize(
        "headers",
        [
            pytest.param(None, id="default-headers"),
            pytest.param({}, id="empty-headers"),
            pytest.param({"X-Request-ID": "request-id"}, id="additional-header"),
            pytest.param({"content-type": "application/x-yaml", "X-Request-ID": "request-id"}, id="custom-headers"),
        ],
    )
    def test_post_headers_preserve_defaults_and_inputs(
        self,
        requests_mock: Mocker,
        method_name: str,
        auth_header_type: AuthHeaderTypeInput | None,
        headers: dict[str, str] | None,
    ) -> None:
        """Merge POST headers without changing caller inputs or authentication modes.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): Ordinary or paginated POST method to exercise.
            auth_header_type (AuthHeaderTypeInput | None): Configured token header, or
                None to exercise a handler without an access token.
            headers (dict[str, str] | None): Optional per-request header overrides.

        Returns:
            None: Asserts every request uses the merged headers and inputs remain intact.
        """
        headers = headers.copy() if headers is not None else None
        handler = RequestHandler(
            self.session,
            self.host,
            access_token=self.access_token if auth_header_type else None,
            auth_header_type=auth_header_type or "Token",
        )
        original_default_headers = handler.headers.copy()
        original_request_headers = headers.copy() if headers is not None else None
        response_headers = {"X-Next-Page": "/test/post?page=2"} if method_name == "post_paginated" else {}
        requests_mock.post(f"{self.host}/test/post", json=[{"id": 1}], headers=response_headers)
        requests_mock.post(f"{self.host}/test/post?page=2", json=[{"id": 2}])

        result = getattr(handler, method_name)("/test/post", body="name: Example", headers=headers)

        assert result == ([{"id": 1}, {"id": 2}] if method_name == "post_paginated" else [{"id": 1}])
        assert len(requests_mock.request_history) == (2 if method_name == "post_paginated" else 1)
        expected_authentication = {}
        if auth_header_type == "Token":
            expected_authentication = {"Token": self.access_token}
        elif auth_header_type == "Authorization":
            expected_authentication = {"Authorization": f"Bearer {self.access_token}"}
        for outgoing_request in requests_mock.request_history:
            actual_authentication = {
                name: outgoing_request.headers[name]
                for name in ("Token", "Authorization")
                if name in outgoing_request.headers
            }
            assert actual_authentication == expected_authentication
            expected_content_type = (headers or {}).get("content-type", original_default_headers["Content-Type"])
            assert outgoing_request.headers["Content-Type"] == expected_content_type
            if headers:
                assert outgoing_request.headers["X-Request-ID"] == headers["X-Request-ID"]
        assert headers == original_request_headers
        assert handler.headers == original_default_headers

    @pytest.mark.parametrize("auth_header_type", ["Token", "Authorization"])
    @pytest.mark.parametrize("authentication_override", ["Token", "authorization", "cdetoken", "basic-auth"])
    def test_post_explicit_authentication_overrides_defaults(
        self,
        requests_mock: Mocker,
        auth_header_type: AuthHeaderTypeInput,
        authentication_override: str,
    ) -> None:
        """Apply explicit POST authentication without sending inherited credentials.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            auth_header_type (AuthHeaderTypeInput): Configured default authentication header.
            authentication_override (str): Explicit header or Requests authentication handler.

        Returns:
            None: Asserts only the selected request authentication is sent and inputs are intact.
        """
        handler = RequestHandler(self.session, self.host, self.access_token, auth_header_type=auth_header_type)
        original_default_headers = handler.headers.copy()
        headers = {"X-Request-ID": "request-id"}
        auth = None
        if authentication_override == "basic-auth":
            auth = HTTPBasicAuth("client", "secret")
            expected_authentication = {"Authorization": "Basic Y2xpZW50OnNlY3JldA=="}
        elif authentication_override == "authorization":
            headers["authorization"] = "Bearer request-token"
            expected_authentication = {"Authorization": "Bearer request-token"}
        elif authentication_override == "cdetoken":
            headers["cdetoken"] = "cde-token"
            expected_authentication = {"CDEToken": "cde-token"}
        else:
            headers["Token"] = "request-token"
            expected_authentication = {"Token": "request-token"}
        original_request_headers = headers.copy()
        requests_mock.post(f"{self.host}/test/post", json={"id": 1})

        handler.post("/test/post", body={"name": "Example"}, headers=headers, auth=auth)

        actual_authentication = {
            name: requests_mock.last_request.headers[name]
            for name in ("Token", "Authorization", "CDEToken")
            if name in requests_mock.last_request.headers
        }
        assert actual_authentication == expected_authentication
        assert headers == original_request_headers
        assert handler.headers == original_default_headers

    @pytest.mark.parametrize("method_name", ["get", "patch", "put"])
    @pytest.mark.parametrize("auth_header_type", ["Token", "Authorization"])
    def test_shared_header_handling(
        self, requests_mock: Mocker, method_name: str, auth_header_type: AuthHeaderTypeInput
    ) -> None:
        """Preserve authentication and header inputs across the core verb wrappers.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): Core HTTP method to exercise.
            auth_header_type (AuthHeaderTypeInput): Configured authentication mode.

        Returns:
            None: Asserts merged headers, JSON encoding and unchanged input dictionaries.
        """
        handler = RequestHandler(self.session, self.host, self.access_token, auth_header_type=auth_header_type)
        headers = {"content-type": "application/json", "X-Request-ID": "example"}
        original_headers = headers.copy()
        original_defaults = handler.headers.copy()
        requests_mock.register_uri(method_name.upper(), f"{self.host}/test/shared", json={"id": 1})
        options = {"pagination": False} if method_name == "get" else {}

        result = getattr(handler, method_name)("/test/shared", body={"name": "Example"}, headers=headers, **options)

        assert result == {"id": 1}
        assert requests_mock.last_request.json() == {"name": "Example"}
        assert requests_mock.last_request.headers["Content-Type"] == "application/json"
        assert requests_mock.last_request.headers["X-Request-ID"] == "example"
        actual_authentication = {
            name: requests_mock.last_request.headers[name]
            for name in ("Token", "Authorization", "CDEToken")
            if name in requests_mock.last_request.headers
        }
        expected_token = self.access_token if auth_header_type == "Token" else f"Bearer {self.access_token}"
        assert actual_authentication == {auth_header_type: expected_token}
        assert headers == original_headers
        assert handler.headers == original_defaults

    @pytest.mark.parametrize("method_name", ["get", "post", "patch", "put", "delete"])
    @pytest.mark.parametrize(
        ("content", "expected", "status_code"),
        [
            pytest.param(b'{"id": 1}', {"id": 1}, 200, id="json-object"),
            pytest.param(b'[1, 2]', [1, 2], 200, id="json-list"),
            pytest.param(b'"job-key"', "job-key", 202, id="json-string"),
            pytest.param("caf\u00e9".encode("utf-8"), "caf\u00e9", 200, id="utf8-text"),
            pytest.param(b"\xff\x00", b"\xff\x00", 200, id="binary"),
            pytest.param(b"", "", 204, id="empty"),
        ],
    )
    def test_shared_response_decoding(
        self, requests_mock: Mocker, method_name: str, content: bytes, expected: object, status_code: int
    ) -> None:
        """Keep existing parsed return values for every core HTTP verb.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): Core HTTP method to exercise.
            content (bytes): Server response body.
            expected (object): Expected parsed payload.
            status_code (int): Successful HTTP status.

        Returns:
            None: Asserts JSON, text, binary and empty responses keep their values.
        """
        requests_mock.register_uri(method_name.upper(), f"{self.host}/test/shared", content=content, status_code=status_code)
        options = {"pagination": False} if method_name == "get" else {"is_async": True} if method_name == "delete" else {}

        result = getattr(self.handler, method_name)("/test/shared", body=None, **options)

        assert result == expected

    @pytest.mark.parametrize("is_async", [False, True])
    def test_delete_return_mapping(self, requests_mock: Mocker, is_async: bool) -> None:
        """Keep the distinction between core synchronous and asynchronous DELETE results.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            is_async (bool): Whether to return the raw decoded payload.

        Returns:
            None: Asserts only synchronous DELETE wraps the response in job details.
        """
        response_body = {"job_id": 7}
        requests_mock.delete(f"{self.host}/test/delete", json=response_body)

        result = self.handler.delete("/test/delete", is_async=is_async)

        assert result == (response_body if is_async else {"status": "successful", "msg": "", "result": response_body})

    def test_get_string_body_remains_json_encoded(self, requests_mock: Mocker) -> None:
        """Preserve the existing GET convention that string bodies are JSON values.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Asserts consolidation does not turn a JSON string body into raw text.
        """
        requests_mock.get(f"{self.host}/test/get", json=[])

        self.handler.get("/test/get", body="Example", pagination=False)

        assert requests_mock.last_request.json() == "Example"

    @pytest.mark.parametrize("method_name", ["post", "put"])
    def test_multipart_requests(self, requests_mock: Mocker, method_name: str) -> None:
        """Send multipart fields and files without inheriting a JSON content type.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): Upload-capable core HTTP method.

        Returns:
            None: Asserts the multipart fields, file bytes and input headers are preserved.
        """
        headers = {"content-type": "application/json", "X-Request-ID": "upload"}
        original_headers = headers.copy()
        original_defaults = self.handler.headers.copy()
        requests_mock.register_uri(method_name.upper(), f"{self.host}/test/upload", json={"id": 1})

        result = getattr(self.handler, method_name)(
            "/test/upload", body={"description": "Example"}, headers=headers,
            files={"file": ("example.txt", b"File contents", "text/plain")},
        )

        outgoing_request = requests_mock.last_request
        content_type = outgoing_request.headers["Content-Type"]
        assert content_type.startswith("multipart/form-data; boundary=")
        message = BytesParser(policy=policy.default).parsebytes(
            f"Content-Type: {content_type}\r\n\r\n".encode("ascii") + outgoing_request.body
        )
        fields = {
            part.get_param("name", header="content-disposition"): part.get_payload(decode=True)
            for part in message.iter_parts()
        }
        assert fields == {"description": b"Example", "file": b"File contents"}
        assert outgoing_request.headers["Authorization"] == f"Bearer {self.access_token}"
        assert result == {"id": 1}
        assert headers == original_headers
        assert self.handler.headers == original_defaults

    def test_post_paginated(self, requests_mock):
        requests_mock.post(
            'https://test.alation.com/test/post',
            json=[{'id': 1, 'name': 'Test 1'}],
            headers={'X-Next-Page': '/test/post?skip=1&limit=1'},
        )
        requests_mock.post(
            'https://test.alation.com/test/post?skip=1&limit=1',
            json=[{'id': 2, 'name': 'Test 2'}],
        )

        result = self.handler.post_paginated('/test/post', {'name': 'New Test'})

        assert result == [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}]
        assert requests_mock.call_count == 2
        assert requests_mock.request_history[0].json() == {'name': 'New Test'}
        assert requests_mock.request_history[1].json() == {'name': 'New Test'}

    def test_post_paginated_error(self, requests_mock):
        requests_mock.post(
            'https://test.alation.com/test/post',
            json=[{'id': 1, 'name': 'Test 1'}],
            headers={'X-Next-Page': '/test/post?skip=1&limit=1'},
        )
        requests_mock.post(
            'https://test.alation.com/test/post?skip=1&limit=1',
            json={'error': 'Server error'},
            status_code=500,
        )

        with pytest.raises(HTTPError) as context:
            self.handler.post_paginated('/test/post', {'name': 'New Test'})

        assert context.value.response.status_code == 500

    
    def test_post_error(self, requests_mock):
        requests_mock.post('https://test.alation.com/test/post', json={'error': 'Server error'}, status_code=500)
        with pytest.raises(HTTPError) as context:
            self.handler.post('/test/post', {'name': 'New Test'})
        assert context.value.response.status_code == 500

    
    def test_put(self, requests_mock):
        requests_mock.put('https://test.alation.com/test/put', json={'id': 3, 'name': 'Put Test'})
        result = self.handler.put('/test/put', {'name': 'Put Test'})
        assert result == {'id': 3, 'name': 'Put Test'}
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
    def test_put_error(self, requests_mock):
        requests_mock.put('https://test.alation.com/test/put', json={'error': 'Not found'}, status_code=404)
        with pytest.raises(HTTPError) as context:
            self.handler.put('/test/put', {'name': 'Put Test'})
        assert context.value.response.status_code == 404


class TestRequestSuccessMapping:
    @pytest.mark.parametrize("use_keyword_argument", [False, True], ids=["positional", "keyword"])
    @pytest.mark.parametrize(
        "response_data",
        [
            pytest.param({"id": 1}, id="dictionary"),
            pytest.param([{"id": 1}], id="list"),
            pytest.param("Completed", id="text"),
            pytest.param(None, id="none"),
            pytest.param({}, id="empty-dictionary"),
            pytest.param([], id="empty-list"),
            pytest.param("", id="empty-text"),
        ],
    )
    def test_response_remains_in_result(self, response_data: object, use_keyword_argument: bool) -> None:
        """Preserve response payloads and the default empty success message.

        Args:
            response_data (object): API response payload to preserve.
            use_keyword_argument (bool): Whether to pass the payload by name.

        Returns:
            None: Asserts the success mapping retains the existing contract.
        """
        if use_keyword_argument:
            result = RequestHandler._map_request_success_to_job_details(response_data=response_data)
        else:
            result = RequestHandler._map_request_success_to_job_details(response_data)

        assert result == {"status": "successful", "msg": "", "result": response_data}

    def test_success_without_response(self) -> None:
        """Support successful endpoints that return no response content.

        Args:
            None.

        Returns:
            None: Asserts an omitted payload maps to a successful empty result.
        """
        result = RequestHandler._map_request_success_to_job_details()

        assert result == {"status": "successful", "msg": "", "result": None}

    @pytest.mark.parametrize("message", ["Data product updated", None])
    def test_success_with_message_only(self, message: str | None) -> None:
        """Preserve explicit messages when no response payload is supplied.

        Args:
            message (str | None): Message supplied by the API, including None.

        Returns:
            None: Asserts message-only calls retain the supplied message.
        """
        result = RequestHandler._map_request_success_to_job_details(msg=message)

        assert result == {"status": "successful", "msg": message, "result": None}

    def test_success_with_response_and_message(self) -> None:
        """Keep the response payload and explicit success message separate.

        Args:
            None.

        Returns:
            None: Asserts a positional payload supports a keyword message.
        """
        response_data = {"product_id": "finance:sales"}

        result = RequestHandler._map_request_success_to_job_details(response_data, msg="Data product updated")

        assert result == {"status": "successful", "msg": "Data product updated", "result": response_data}
