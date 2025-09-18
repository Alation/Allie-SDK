"""Minimal stub implementation of the requests-mock interface used in tests."""

from __future__ import annotations

import json
from collections import deque
from functools import wraps
from typing import Any, Callable, Optional
from urllib.parse import urlparse

import requests
from requests import Response
from requests.structures import CaseInsensitiveDict


class _MockResponse(Response):
    """Lightweight response object that mimics ``requests.Response``."""

    def __init__(
        self,
        *,
        status_code: int,
        url: str,
        json_data: Any,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__()
        self.status_code = status_code
        self.url = url
        self.headers = CaseInsensitiveDict(headers or {})
        self.reason = requests.status_codes._codes.get(status_code, [''])[0].upper()

        if json_data is not None:
            self._json_data = json_data
            self.headers.setdefault('Content-Type', 'application/json')
            self._content = json.dumps(json_data).encode('utf-8')
        else:
            self._json_data = None
            self._content = b''

        self.encoding = 'utf-8'
        self._content_consumed = True

    def json(self, **kwargs: Any) -> Any:  # noqa: D401 - match requests interface
        """Return the mocked JSON payload."""
        if self._json_data is None:
            raise ValueError('No JSON data available')
        return self._json_data


class Mocker:
    """A very small subset of the ``requests_mock.Mocker`` API."""

    def __init__(self, real_http: bool = False) -> None:
        self._registrations: deque[dict[str, Any]] = deque()
        self._real_http = real_http
        self._original_request: Optional[Callable[..., Response]] = None

    def __call__(self, func: Optional[Callable] = None) -> Callable:
        if func is None:
            return self

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with self:
                return func(*args, self, **kwargs)

        return wrapper

    def __enter__(self) -> "Mocker":
        self._original_request = requests.sessions.Session.request

        def _mock_request(session: requests.Session, method: str, url: str, **kwargs: Any) -> Response:
            method_upper = method.upper()
            parsed = urlparse(url)
            path = parsed.path

            for registration in reversed(self._registrations):
                if registration['method'] != method_upper:
                    continue
                if path != registration['path']:
                    continue

                return _MockResponse(
                    status_code=registration['status_code'],
                    url=url,
                    json_data=registration['json'],
                    headers=registration['headers'],
                )

            if self._real_http and self._original_request is not None:
                return self._original_request(session, method, url, **kwargs)

            raise RuntimeError(f'No mock registered for {method_upper} {url}')

        requests.sessions.Session.request = _mock_request
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        if self._original_request is not None:
            requests.sessions.Session.request = self._original_request
        self._registrations.clear()
        self._original_request = None

    def register_uri(
        self,
        method: str,
        url: str,
        *,
        json: Any = None,
        status_code: int = 200,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        parsed = urlparse(url if '://' in url else f'https://mockserver{url}')
        self._registrations.append(
            {
                'method': method.upper(),
                'path': parsed.path,
                'json': json,
                'status_code': status_code,
                'headers': headers or {},
            }
        )
