"""Route all Alation API Calls through the same core request functions."""

import json
import logging
from typing import Any, TypeAlias

import requests
from requests.auth import AuthBase
from requests.structures import CaseInsensitiveDict

from urllib.parse import urlparse
from requests.adapters import HTTPAdapter, Retry
from ..models.job_model import *
from ..models.authentication_model import AuthHeaderType, AuthHeaderTypeInput

RequestBody: TypeAlias = dict[str, Any] | list[Any] | str | bytes

API_LOGGER = logging.getLogger("allie_sdk_logger")
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]
SUCCESS_CODES = [200, 201, 202, 204]



class RequestHandler(object):
    """Route all Alation API Calls through same core request functions."""

    def __init__(
        self,
        session: requests.Session,
        host: str,
        access_token: str | None = None,
        page_size: int = 1000,
        auth_header_type: AuthHeaderTypeInput = AuthHeaderType.TOKEN,
    ) -> None:
        """Creates an instance of the RequestHandler object.

        Args:
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
            access_token (str | None): Alation REST API Access Token. None or an
                empty string sends no default authentication header.
            page_size (int): Page size of REST API Get Calls.
            auth_header_type (AuthHeaderTypeInput): Token or Bearer authentication.
                Accepts enum members or the existing "Token" and "Authorization"
                strings. Defaults to AuthHeaderType.TOKEN.

        Returns:
            None: Initializes the session, request defaults and validated authentication mode.

        Raises:
            ValueError: If the authentication mode is unsupported, even without a token.
        """
        try:
            self._auth_header_type = AuthHeaderType(auth_header_type)
        except (TypeError, ValueError) as error:
            error_message = (
                f"Invalid auth_header_type {auth_header_type!r}. "
                f"Expected one of: {', '.join(repr(mode.value) for mode in AuthHeaderType)}."
            )
            API_LOGGER.error(error_message)
            raise ValueError(error_message) from error

        self.s = session
        self.host = host.rstrip('/')
        self.page_size = page_size

        retries = Retry(total=5, backoff_factor=0.2, status_forcelist=RETRY_STATUS_CODES)
        self.s.mount('http://', HTTPAdapter(max_retries=retries))
        self.s.mount('https://', HTTPAdapter(max_retries=retries))

        self.headers = {"Content-Type": "application/json; charset=utf-8"}
        self.access_token = access_token

    @property
    def auth_header_type(self) -> AuthHeaderType:
        """Return the normalized authentication mode selected at construction.

        Args:
            None.

        Returns:
            AuthHeaderType: Validated Token or Bearer authentication mode.
        """
        return self._auth_header_type

    @property
    def access_token(self) -> str | None:
        """Return the access token currently used for default authentication.

        Args:
            None.

        Returns:
            str | None: Current token, or None when no token is configured.
        """
        return self._access_token

    @access_token.setter
    def access_token(self, token: str | None) -> None:
        """Synchronize default authentication headers when the access token changes.

        Args:
            token (str | None): Replacement token. None or an empty string removes
                default authentication. Other request defaults are preserved.

        Returns:
            None: Stores the token and replaces the default authentication header.
        """
        self._access_token = token
        request_headers = CaseInsensitiveDict(self.headers)
        request_headers.pop("Token", None)
        request_headers.pop("Authorization", None)
        if token:
            prefix = "Bearer " if self.auth_header_type is AuthHeaderType.BEARER else ""
            request_headers[self.auth_header_type.value] = f"{prefix}{token}"
        self.headers = dict(request_headers)
        API_LOGGER.debug("Updated default authentication headers.")

    def delete(
        self,
        url: str,
        body: RequestBody | None = None,
        query_params: dict | None = None,
        is_async: bool = False
    ) -> dict | list:
        """API Delete Request.

        Args:
            url (str): DELETE API Call URL.
            body (RequestBody | None): Optional DELETE API body. Defaults to None.
            is_async (bool): If True, return raw response for async handling.
            query_params (dict): DELETE API Call Query Parameters.


        Returns:
            dict | list: API Response Body.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        api_response = self._request("DELETE", self.host + url, body=body, params=query_params)
        self._log_response(api_response, "DELETE")
        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()
        response_data = self._parse_response(api_response)
        if is_async:
            return response_data
        return self._map_request_success_to_job_details(response_data)

    def get(
        self,
        url: str,
        query_params: dict | None = None,
        pagination: bool = True,
        body: RequestBody | None = None,
        headers: dict | None = None,
    ) -> Any:
        """API Get Request.

        Args:
            url (str): GET API Call URL.
            query_params (dict): GET API Call Query Parameters.
            pagination (bool): Fetch all API results that meet the Query Parameters.
            body (RequestBody | None): Optional GET request body. Defaults to None.
            headers (dict): Optional GET API Call Headers.

        Returns:
            any: API Response Body in JSON.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        returned_items = []
        if query_params is None:
            query_params = {}
        if pagination:
            query_params['limit'] = self.page_size

        api_response = self._api_single_get(
            self.host + url, params=query_params, body=body, headers=headers
        )
        # Check status and raise error if needed
        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()
            
        returned_items = self._parse_response(api_response)
        if isinstance(returned_items, (str, bytes)):
            return returned_items

        if pagination:
            while 'X-Next-Page' in api_response.headers:
                next_url = api_response.headers.get('X-Next-Page')
                api_response = self._api_single_get(self.host + next_url, headers=headers)
                
                # Check status of paginated request and raise error if needed
                if api_response.status_code not in SUCCESS_CODES:
                    api_response.raise_for_status()
                
                response_data = self._parse_response(api_response)
                returned_items.extend(response_data)

        return returned_items

    def get_nested_results(
            self,
            url: str,
            query_params: dict | None = None,
            pagination: bool = True,
            body: RequestBody | None = None,
            headers: dict | None = None,
    ) -> list:
        """API GET request for paginated responses wrapped in a results envelope.

        This supports response bodies shaped like::

            {
                "count": 2,
                "next": "/path/?limit=1&offset=1",
                "previous": None,
                "results": [...]
            }

        This is DRF-style pagination with `next` and `results`, not the header-based list pagination.
        DRF = Django REST Framework.

        Args:
            url (str): GET API Call URL.
            query_params (dict): GET API Call Query Parameters.
            pagination (bool): Follow the ``next`` URL until every result is fetched.
            body (RequestBody | None): Optional GET request body. Defaults to None.
            headers (dict): Optional headers merged with defaults without mutation.

        Returns:
            list: Flattened list of items from the ``results`` property.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
            ValueError: If the API response does not contain a ``results`` list.
        """
        returned_items = []
        if query_params is None:
            query_params = {}
        else:
            query_params = query_params.copy()

        if pagination and "limit" not in query_params:
            query_params["limit"] = self.page_size

        api_response = self._api_single_get(
            self.host + url, params=query_params, body=body, headers=headers
        )
        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()

        response_data = self._parse_response(api_response)

        if not isinstance(response_data, dict) or not isinstance(response_data.get("results"), list):
            raise ValueError("Nested GET requests must return a dictionary containing a 'results' list.")

        returned_items.extend(response_data["results"])

        next_url = response_data.get("next") if pagination else None
        while next_url:
            parsed_next_url = urlparse(next_url)
            request_url = next_url if parsed_next_url.scheme else self.host + next_url
            api_response = self._api_single_get(request_url, body=body, headers=headers)

            if api_response.status_code not in SUCCESS_CODES:
                api_response.raise_for_status()

            response_data = self._parse_response(api_response)

            if not isinstance(response_data, dict) or not isinstance(response_data.get("results"), list):
                raise ValueError("Nested GET requests must return a dictionary containing a 'results' list.")

            returned_items.extend(response_data["results"])
            next_url = response_data.get("next")

        return returned_items

    def patch(
        self,
        url: str,
        body: RequestBody | None,
        query_params: dict | None = None,
        headers: dict | None = None
    ) -> dict:
        """API Patch Request.

        Args:
            url (str): PATCH API Call URL.
            body (RequestBody | None): PATCH API body, or None to send no body.
            query_params (dict): PATCH API Call Query Parameters.
            headers (dict): Headers merged with defaults without mutation. Explicit
                authentication headers replace the configured authentication.

        Returns:
            dict: API Response Body in JSON.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        api_response = self._request("PATCH", self.host + url, body=body, params=query_params, headers=headers)
        self._log_response(api_response, "PATCH")
        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()
        return self._parse_response(api_response)

    def post(
        self,
        url: str,
        body: RequestBody | None,
        query_params: dict | None = None,
        headers: dict | None = None,
        files: dict | None = None,
        *,
        auth: AuthBase | None = None,
    ) -> dict | list:
        """API Post Request.

        Args:
            url (str): POST API Call URL.
            body (RequestBody | None): POST API body. Dictionaries and lists are
                JSON-encoded; strings and bytes are sent unchanged. None sends no body.
            query_params (dict): POST API Call Query Parameters.
            headers (dict): Per-request headers merged case-insensitively with
                defaults without mutating either. Explicit authentication headers
                replace the configured authentication for this request.
            files: (dict) POST API Call upload files
            auth (AuthBase | None): Optional Requests authentication handler,
                replacing default authentication for this request.

        Returns:
            dict | list: API Response Body.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        if query_params is None:
            query_params = {}

        api_response = self._api_single_post(
            self.host + url,
            body=body,
            params=query_params,
            headers=headers,
            files=files,
            auth=auth,
        )

        response_data = self._parse_response(api_response)

        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()

        return response_data

    def post_paginated(
        self,
        url: str,
        body: RequestBody | None,
        query_params: dict | None = None,
        headers: dict | None = None,
        files: dict | None = None,
    ) -> dict | list:
        """API Post Request with pagination support via ``X-Next-Page``.

        Args:
            url (str): POST API Call URL.
            body (RequestBody | None): POST API body, or None to send no body.
            query_params (dict): POST API Call Query Parameters.
            headers (dict): Per-request headers merged case-insensitively with
                defaults without mutating either. Explicit authentication headers
                replace the configured authentication for these requests.
            files: (dict) POST API Call upload files

        Returns:
            dict | list: API Response Body.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
            ValueError: If the API returns paginated data in a non-list response shape.
        """
        if query_params is None:
            query_params = {}

        api_response = self._api_single_post(
            self.host + url,
            body=body,
            params=query_params,
            headers=headers,
            files=files,
        )

        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()

        returned_items = self._parse_response(api_response)

        if not isinstance(returned_items, list):
            if "X-Next-Page" in api_response.headers:
                raise ValueError("Paginated POST requests must return list responses.")
            return returned_items

        while "X-Next-Page" in api_response.headers:
            next_url = api_response.headers.get("X-Next-Page")
            if not next_url:
                break

            parsed_next_url = urlparse(next_url)
            request_url = next_url if parsed_next_url.scheme else self.host + next_url
            api_response = self._api_single_post(
                request_url,
                body=body,
                headers=headers,
                files=files,
            )

            if api_response.status_code not in SUCCESS_CODES:
                api_response.raise_for_status()

            response_data = self._parse_response(api_response)

            if not isinstance(response_data, list):
                raise ValueError("Paginated POST requests must return list responses.")

            returned_items.extend(response_data)

        return returned_items

    def put(
        self,
        url: str,
        body: RequestBody | None,
        query_params: dict | None = None,
        headers: dict | None = None,
        files: dict | None = None,
    ) -> dict | list:
        """API Put Request.

        Args:
            url (str): PUT API Call URL.
            body (RequestBody | None): PUT API body, or None to send no body.
            query_params (dict): PUT API Call Query Parameters.
            headers (dict): Headers merged with defaults without mutation. Explicit
                authentication headers replace the configured authentication.
            files (dict): Optional multipart uploads.

        Returns:
            dict | list: API Response Body.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        api_response = self._request(
            "PUT", self.host + url, body=body, params=query_params, headers=headers, files=files
        )
        self._log_response(api_response, "PUT")
        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()
        return self._parse_response(api_response)

    def _api_single_get(
            self,
            url: str,
            params: dict | None = None,
            body: RequestBody | None = None,
            headers: dict | None = None
    ) -> requests.Response:
        """Run a Single REST API Get Call. Helper function for paginated results.

        Args:
            url (str): GET API Call URL.
            params (dict): GET API Call Query Parameters.
            body (RequestBody | None): Optional GET request body. Defaults to None.
            headers (dict): Optional GET API Call Headers.

        Returns:
            requests.Response: API GET Response.

        Note:
            This is a helper method that doesn't raise exceptions directly.
            The calling method is responsible for checking status codes and raising exceptions.
        """
        # Preserve the GET contract: every supplied body represents a JSON value.
        request_body = json.dumps(body, default=str) if body is not None else None
        api_response = self._request("GET", url, body=request_body, params=params, headers=headers)
        self._log_response(api_response, "GET")
        return api_response

    def _api_single_post(
        self,
        url: str,
        body: RequestBody | None,
        params: dict | None = None,
        headers: dict | None = None,
        files: dict | None = None,
        *,
        auth: AuthBase | None = None,
    ) -> requests.Response:
        """Run a Single REST API Post Call.

        Args:
            url (str): POST API Call URL.
            body (RequestBody | None): POST API body, or None to send no body.
            params (dict): POST API Call Query Parameters.
            headers (dict): Per-request headers merged case-insensitively with
                defaults without mutating either. Explicit authentication headers
                replace the configured authentication for this request.
            files: (dict) POST API Call upload files
            auth (AuthBase | None): Optional Requests authentication handler,
                replacing default authentication for this request.

        Returns:
            requests.Response: API POST Response.

        Note:
            This is a helper method that doesn't raise exceptions directly.
            The calling method is responsible for checking status codes and raising exceptions.
        """
        api_response = self._request(
            "POST", url, body=body, params=params, headers=headers, files=files, auth=auth
        )
        self._log_response(api_response, "POST")
        return api_response

    def _request(
        self,
        method: str,
        url: str,
        body: RequestBody | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        files: dict | None = None,
        *,
        auth: AuthBase | None = None,
    ) -> requests.Response:
        """Send one HTTP request through the shared session without checking status.

        Args:
            method (str): HTTP verb.
            url (str): Absolute request URL.
            body (RequestBody | None): Dictionaries and lists are JSON-encoded unless
                uploading files; other bodies are passed through unchanged.
            params (dict | None): Query string parameters.
            headers (dict | None): Case-insensitive overrides for default headers.
                Explicit Token, Authorization or CDEToken replaces default authentication.
                Neither the defaults nor the supplied headers are mutated.
            files (dict | None): Multipart uploads. Requests supplies their content type.
            auth (AuthBase | None): Requests authentication replacing default credentials.

        Returns:
            requests.Response: Raw response, allowing authentication adapters to retry
            before logging and checking the final status.

        Raises:
            requests.RequestException: If preparing or sending the request fails.
        """
        request_headers = CaseInsensitiveDict(self.headers)
        custom_headers = CaseInsensitiveDict(headers or {})
        authentication_headers = ("Token", "Authorization", "CDEToken")
        if auth is not None or any(name in custom_headers for name in authentication_headers):
            for name in authentication_headers:
                request_headers.pop(name, None)
        request_headers.update(custom_headers)

        if files:
            request_headers.pop("Content-Type", None)
        elif isinstance(body, (dict, list)):
            body = json.dumps(body, default=str)

        return self.s.request(
            method, url, data=body, params=params, headers=request_headers, files=files, auth=auth
        )

    @staticmethod
    def _parse_response(api_response: requests.Response) -> Any:
        """Decode a response as JSON, UTF-8 text, or undecodable bytes.

        Args:
            api_response (requests.Response): Response to decode.

        Returns:
            Any: Parsed JSON, text (including an empty string), or binary content.
        """
        try:
            return api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                return api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                return api_response.content

    def _log_response(self, api_response: requests.Response, method: str) -> None:
        """Log a final HTTP response without raising or changing its return value.

        Args:
            api_response (requests.Response): Final response after any authentication retry.
            method (str): HTTP verb used for the request.

        Returns:
            None: Writes a success or error log using the common response decoder.
        """
        response_data = self._parse_response(api_response)
        log_url = self._format_log_url(api_response.url)
        log_details = {"Method": method, "URL": api_response.url, "Response": api_response.status_code}
        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data, log_details, message=f"Error submitting the {method} Request to: {log_url}"
            )
        else:
            log_details["Objects Returned"] = len(response_data) if isinstance(response_data, list) else 1
            self._log_success(log_details, message=f"Successfully submitted the {method} Request to: {log_url}")

    @staticmethod
    def _log_success(details: dict, message: str) -> None:
        """Log the REST API Success Message.

        Args:
            details (dict): API Details to be included in the log message.
            message (str): Success message to be logged.

        """
        API_LOGGER.debug(message, extra=details)

    @staticmethod
    def _log_error(response_data: dict, details: dict, message: str) -> None:
        """Log the REST API Error Message.

        Args:
            response_data (dict): REST API Response Message.
            details (dict): API Details to be included in the log message.
            message (str): Error message to be logged.

        """
        if isinstance(response_data, dict):
            error_code = response_data.get('code', None)
            error_title = response_data.get('title', None)
            error_detail = response_data.get('detail', None)
            error_errors = response_data.get('errors', None)

            if error_code:
                details['Error Code'] = error_code
                message = f'{message}\nERROR CODE: {error_code}'

            if error_title:
                details['Error Title'] = error_title
                message = f'{message}\nERROR TITLE: {error_title}'

            if error_detail:
                details['Error Details'] = error_detail
                message = f'{message}\nERROR DETAIL: {error_detail}'

            if error_errors:
                details['More Error info'] = error_errors
                # since every API endpoint quite likely has their own nested structure
                # we just simply dump the output here
                message = f'{message}\nERRORS: {json.dumps(error_errors)}'

            if all(var is None for var in (error_code, error_title, error_detail)):
                details['Error'] = response_data
                message = f'{message}\nERROR: {response_data}'

            API_LOGGER.error(f'ERROR MESSAGE: {message}', extra=details)

        else:
            API_LOGGER.error(f'ERROR MESSAGE: {message}\nERROR: {response_data}', extra=details)

    @staticmethod
    def _format_log_url(api_response_url: str) -> str:
        """Format the API URL to be logged.

        Args:
            api_response_url (str): API Response URL.

        Returns:
            str: Log URL

        """
        parsed_url = urlparse(api_response_url)
        url = parsed_url.path

        if parsed_url.query:
            url += f'?{parsed_url.query}'

        return url


    @staticmethod
    def _map_request_error_to_job_details(response_data:Any) -> dict:

        if isinstance(response_data, dict):
            msg = response_data.get("title", None)
        else:
            msg = ""

        error_data = dict(
            status = "failed"
            , msg = msg
            , result = response_data
        )

        return error_data

    @staticmethod
    def _map_request_success_to_job_details(
        response_data: object = None,
        *,
        msg: str | None = "",
    ) -> dict[str, object]:
        """Map a successful API response to the JobDetails structure.

        Args:
            response_data (object): API response payload stored in result. Defaults
                to None for endpoints that return no response content. May be
                passed positionally or by keyword for backward compatibility.
            msg (str | None): Optional success message, supplied by keyword.
                Defaults to an empty string; explicit None values are preserved.

        Returns:
            dict[str, object]: Successful status, message, and original payload.
        """
        API_LOGGER.debug("Mapping successful API response to job details.")
        return {"status": "successful", "msg": msg, "result": response_data}
