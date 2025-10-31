"""Route all Alation API Calls through the same core request functions."""

import json
import logging
import requests

from urllib.parse import urlparse
from requests.adapters import HTTPAdapter, Retry
from ..models.job_model import *

API_LOGGER = logging.getLogger("allie_sdk_logger")
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]
SUCCESS_CODES = [200, 201, 202, 204]


class RequestHandler(object):
    """Route all Alation API Calls through same core request functions."""

    def __init__(self, session: requests.Session, host: str, access_token: str = None,
                 page_size: int = 1000):
        """Creates an instance of the RequestHandler object.

        Args:
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
            access_token (str): Alation REST API Access Token.
            page_size (int): Page size of REST API Get Calls.

        """
        self.s = session
        self.host = host.rstrip('/')
        self.page_size = page_size

        retries = Retry(total=5, backoff_factor=0.2, status_forcelist=RETRY_STATUS_CODES)
        self.s.mount('http://', HTTPAdapter(max_retries=retries))
        self.s.mount('https://', HTTPAdapter(max_retries=retries))

        self.headers = {"Content-Type": "application/json; charset=utf-8"}
        if access_token:
            self.access_token = access_token
            self.headers['Token'] = access_token

    def delete(
        self,
        url: str,
        body: any = None,
        query_params: dict = None,
        is_async: bool = False

    ) -> dict | list:
        """API Delete Request.

        Args:
            url (str): DELETE API Call URL.
            body (any): DELETE API Body.
            is_async (bool): If True, return raw response for async handling.
            query_params (dict): DELETE API Call Query Parameters.


        Returns:
            dict | list: API Response Body.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        if query_params is None:
            query_params = {}

        if isinstance(body, dict) or isinstance(body, list):
            body = json.dumps(body, default=str)

        api_response = self.s.delete(
            self.host + url, data=body, params=query_params, headers=self.headers
        )

        try:
            response_data = api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                response_data = api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                response_data = api_response.content

        log_url = self._format_log_url(api_response.url)
        log_details = {
            'Method': 'DELETE'
            , 'URL': api_response.url
            , 'Response': api_response.status_code
        }

        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data
                , log_details
                , message = f'Error submitting the DELETE Request to: {log_url}'
            )
            
            # Raise HTTP error instead of returning error details
            api_response.raise_for_status()

        self._log_success(
            log_details
            , message = f'Succesfully submitted the DELETE Request to: {log_url}'
        )

        if is_async:
            # return response data as is since we still need to extract the job id in async_handler.py
            return response_data
        else:
            # make sure result conforms to JobDetails structure
            mapped_response_data = self._map_request_success_to_job_details(response_data)
            return mapped_response_data

    def get(
            self,
            url: str,
            query_params: dict = None,
            pagination: bool = True,
            body: any = None,
    ) -> any:
        """API Get Request.

        Args:
            url (str): GET API Call URL.
            query_params (dict): GET API Call Query Parameters.
            pagination (bool): Fetch all API results that meet the Query Parameters.
            body (any): Optional GET Request Body.

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
            self.host + url, params=query_params, body=body
        )
        # Check status and raise error if needed
        if api_response.status_code not in SUCCESS_CODES:
            api_response.raise_for_status()
            
        try:
            returned_items = api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                return api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                return api_response.content

        if pagination:
            while 'X-Next-Page' in api_response.headers:
                next_url = api_response.headers.get('X-Next-Page')
                api_response = self._api_single_get(self.host + next_url)
                
                # Check status of paginated request and raise error if needed
                if api_response.status_code not in SUCCESS_CODES:
                    api_response.raise_for_status()
                
                response_data = api_response.json()
                returned_items.extend(response_data)

        return returned_items

    def patch(self, url: str, body: any, query_params: dict = None, headers: dict = None) -> dict:
        """API Patch Request.

        Args:
            url (str): PATCH API Call URL.
            body (any): PATCH API Body.
            query_params (dict): PATCH API Call Query Parameters.
            headers (dict): POST API Call Headers.

        Returns:
            dict: API Response Body in JSON.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        if query_params is None:
            query_params = {}

        if headers:
            headers['Token'] = self.access_token
        else:
            headers = self.headers

        if isinstance(body, dict) or isinstance(body, list):
            body = json.dumps(body, default=str)

        api_response = self.s.patch(self.host + url, data=body, params=query_params, headers=headers)

        try:
            response_data = api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                response_data = api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                response_data = api_response.content

        log_url = self._format_log_url(api_response.url)
        log_details = {
            'Method': 'PATCH'
            , 'URL': api_response.url
            , 'Response': api_response.status_code
        }

        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data
                , log_details
                , message = f'Error submitting the PATCH Request to: {log_url}'
            )
            
            # Raise HTTP error instead of returning error details
            api_response.raise_for_status()

        self._log_success(
            log_details
            , message = f'Successfully submitted the PATCH Request to: {log_url}')

        return response_data

    def post(self, url: str, body: any, query_params: dict = None, headers: dict = None,
             files: dict = None) -> dict | list:
        """API Post Request.

        Args:
            url (str): POST API Call URL.
            body (any): POST API Body.
            query_params (dict): POST API Call Query Parameters.
            headers (dict): POST API Call Headers.
            files: (dict) POST API Call upload files

        Returns:
            dict | list: API Response Body.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        if query_params is None:
            query_params = {}

        if headers:
            headers['Token'] = self.access_token
        else:
            headers = self.headers

        if isinstance(body, dict) or isinstance(body, list):
            body = json.dumps(body, default=str)

        api_response = self.s.post(self.host + url, data=body, params=query_params, headers=headers, files=files)

        try:
            response_data = api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                response_data = api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                response_data = api_response.content

        log_url = self._format_log_url(api_response.url)
        log_details = {
            'Method': 'POST'
            , 'URL': api_response.url
            , 'Response': api_response.status_code
        }

        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data
                , log_details
                , message = f'Error submitting the POST Request to: {log_url}'
            )
            
            # Raise HTTP error instead of returning error details
            api_response.raise_for_status()

        self._log_success(
            log_details
            , message = f'Successfully submitted the POST Request to: {log_url}'
        )

        return response_data

    def put(
        self,
        url: str,
        body: any,
        query_params: dict = None,
        headers: dict = None,
        files: dict = None,
    ) -> dict | list:
        """API Put Request.

        Args:
            url (str): PUT API Call URL.
            body (any): PUT API Body.
            query_params (dict): PUT API Call Query Parameters.

        Returns:
            dict | list: API Response Body.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        if query_params is None:
            query_params = {}

        if headers:
            headers['Token'] = self.access_token
        else:
            headers = self.headers.copy()

        if files:
            # Requests will determine the correct boundary and content type when not provided explicitly
            headers = {
                key: value for key, value in headers.items() if key.lower() != 'content-type'
            }
            request_body = body
        else:
            if isinstance(body, dict) or isinstance(body, list):
                request_body = json.dumps(body, default=str)
            else:
                request_body = body

        api_response = self.s.put(
            self.host + url,
            data=request_body,
            params=query_params,
            headers=headers,
            files=files,
        )

        try:
            response_data = api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                response_data = api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                response_data = api_response.content

        log_url = self._format_log_url(api_response.url)
        log_details = {
            'Method': 'PUT'
            , 'URL': api_response.url
            , 'Response': api_response.status_code
        }

        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data
                , log_details
                , message = f'Error submitting the PUT Request to: {log_url}'
            )
            
            # Raise HTTP error instead of returning error details
            api_response.raise_for_status()

        self._log_success(
            log_details
            , message = f'Successfully submitted the PUT Request to: {log_url}'
        )

        return response_data

    def _api_single_get(
            self, url: str, params: dict = None, body: any = None
    ) -> requests.Response:
        """Run a Single REST API Get Call. Helper function for paginated results.

        Args:
            url (str): GET API Call URL.
            params (dict): GET API Call Query Parameters.
            body (any): Optional GET Request Body.

        Returns:
            requests.Response: API GET Response.

        Note:
            This is a helper method that doesn't raise exceptions directly.
            The calling method is responsible for checking status codes and raising exceptions.
        """
        if body is not None:
            body = json.dumps(body, default=str)

            # Always call GET; requests can handle None for params/body
        api_response = self.s.get(
            url,
            params=params,
            headers=self.headers,
            data=body
        )

        try:
            response_data = api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                response_data = api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                response_data = api_response.content

        log_url = self._format_log_url(api_response.url)
        log_details = {
            'Method': 'GET'
            , 'URL': api_response.url
            , 'Response': api_response.status_code
        }

        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data
                , log_details
                , message = f'Error submitting the GET Request to: {log_url}'
            )
        else:
            response_objects = len(response_data) if isinstance(response_data, list) else 1
            log_details['Objects Returned'] = response_objects
            self._log_success(
                log_details
                , message = f'Successfully submitted the GET Request to: {log_url}'
            )

        return api_response

    @staticmethod
    def _log_success(details: dict, message: str):
        """Log the REST API Success Message.

        Args:
            details (dict): API Details to be included in the log message.
            message (str): Success message to be logged.

        """
        API_LOGGER.debug(message, extra=details)

    @staticmethod
    def _log_error(response_data: dict, details: dict, message: str):
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
    def _map_request_error_to_job_details(response_data) -> dict:

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
    def _map_request_success_to_job_details(response_data=None) -> dict:
        # some API endpoints don't return any response content (e.g. for business policies)
        # hence we made the reponse_data argument optional here
        success_data = dict(
            status = "successful"
            , msg = ""
            , result = response_data
        )

        return success_data
