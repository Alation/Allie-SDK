"""Route all Alation API Calls through the same core request functions."""

import json
import logging
import requests

from urllib.parse import urlparse, urljoin
from requests.adapters import HTTPAdapter, Retry

API_LOGGER = logging.getLogger("allie_sdk_logger")
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]


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

    def delete(self, url: str, body: any = None) -> dict | list:
        """API Delete Request.

        Args:
            url (str): DELETE API Call URL.
            body (any): DELETE API Body.

        Returns:
            dict | list: API Response Body.

        """
        response = self._request('DELETE', url, body)
        data = self._process_response(response)

        return data if data else True

    def get(self, url: str, query_params: dict = None, pagination: bool = True) -> any:
        """API Get Request.

        Args:
            url (str): GET API Call URL.
            query_params (dict): GET API Call Query Parameters.
            pagination (bool): Fetch all API results that meet the Query Parameters.

        Returns:
            any: API Response Body in JSON.

        """
        query_params = query_params or {}

        if pagination:
            query_params['limit'] = self.page_size

        response = self._request('GET', url, query_params=query_params)
        data = self._process_response(response)

        if pagination:
            while 'X-Next-Page' in response.headers:
                next_url = response.headers.get('X-Next-Page')
                response = self._request('GET', next_url, query_params=query_params)
                data.extend(self._process_response(response))


        return data

    def patch(self, url: str, body: any, query_params: dict = None, headers: dict = None) -> dict:
        """API Patch Request.

        Args:
            url (str): PATCH API Call URL.
            body (any): PATCH API Body.
            query_params (dict): PATCH API Call Query Parameters.
            headers (dict): POST API Call Headers.

        Returns:
            dict: API Response Body in JSON.

        """
        headers = headers or {}
        query_params = query_params or {}

        response = self._request('PATCH', url, body, query_params=query_params, headers=headers)

        return self._process_response(response)

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

        """
        headers = headers or {}
        query_params = query_params or {}
        files = files or {}

        response = self._request('POST', url, body, query_params=query_params, headers=headers, files=files)

        return self._process_response(response)

    def put(self, url: str, body: any, query_params: dict = None) -> dict | list:
        """API Put Request.

        Args:
            url (str): PUT API Call URL.
            body (any): PUT API Body.
            query_params (dict): PUT API Call Query Parameters.

        Returns:
            dict | list: API Response Body.

        """
        query_params = query_params or {}
        
        response = self._request('PUT', url, body, query_params=query_params)

        return self._process_response(response)

    def _request(
            self,
            method: str,
            url: str,
            body: any = None,
            query_params: dict = {},
            headers: dict = {},
            files: dict = {}
    ) -> any:
        """Decode the API Response.

        Args:
            method (str): API Request Method.
            url (str): API Request URL, without the base URL.
            body (any): API Request Body.
            query_params (dict): API Request Query Parameters.
            headers (dict): API Request Headers.
            files (dict): API Request Files.

        Returns:
            any: API Response Body.

        """
        headers.update(self.headers)

        if isinstance(body, dict) or isinstance(body, list):
            body = json.dumps(body, default=str)

        response = self.s.request(
            method,
            urljoin(self.host, url),
            data=body,
            params=query_params,
            headers=headers,
            files=files
        )

        return response

    def _process_response(self, response):
        method = response.request.method.upper()
        log_url = self._format_log_url(response.url)

        log_details = {
            'Method': method,
            'URL': response.url,
            'Response': response.status_code
        }

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                response_data = response.content.decode("utf-8")
            except UnicodeDecodeError:
                response_data = response.content

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            self._log_error(response_data, log_details, f'Error submitting the {method} Request to: {log_url}')
            raise http_error

        if method == 'GET':
            log_details['Objects Returned'] = len(response_data) if isinstance(response_data, list) else 1
        self._log_success(log_details, f'Successfully submitted the {method} Request to: {log_url}')

        return response_data

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

            if error_code:
                details['Error Code'] = error_code
                message = f'{message}\nERROR CODE: {error_code}'

            if error_title:
                details['Error Title'] = error_title
                message = f'{message}\nERROR TITLE: {error_title}'

            if error_detail:
                details['Error Details'] = error_detail
                message = f'{message}\nERROR DETAIL: {error_detail}'

            if all(var is None for var in (error_code, error_title, error_title)):
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
