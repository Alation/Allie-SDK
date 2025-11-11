"""FastMCP server exposing every Allie SDK method as an MCP tool."""

from __future__ import annotations

import dataclasses
import inspect
import logging
import os
from collections.abc import Callable
from functools import wraps
from typing import Any, Dict

from fastmcp import FastMCP
try:
    from fastmcp.exceptions import AuthenticationError
except Exception:  # pragma: no cover - FastMCP provides the real exception
    class AuthenticationError(RuntimeError):
        """Fallback when FastMCP's dedicated exception cannot be imported."""


from allie_sdk.alation import Alation
from allie_sdk.methods import (
    AlationAuthentication,
    AlationBusinessPolicy,
    AlationConnector,
    AlationCustomField,
    AlationCustomTemplate,
    AlationDataDictionary,
    AlationDataQuality,
    AlationDatasource,
    AlationDataflow,
    AlationDocument,
    AlationDocumentHubFolder,
    AlationDomain,
    AlationGlossaryTerm,
    AlationGroup,
    AlationOtype,
    AlationPolicyGroup,
    AlationQuery,
    AlationRDBMS,
    AlationTrustChecks,
    AlationUser,
    AlationVirtualDataSource,
    AlationVirtualFileSystem,
    AlationVisualConfig,
)

LOGGER = logging.getLogger("allie_sdk_logger")


def _ensure_expected_refresh_token() -> str:
    """Return the expected refresh token configured on the server."""

    expected_refresh_token = os.environ.get("ALLIE_SDK_EXPECTED_REFRESH_TOKEN")
    if not expected_refresh_token:
        raise AuthenticationError(
            "Missing ALLIE_SDK_EXPECTED_REFRESH_TOKEN environment variable."
        )
    return expected_refresh_token


def _serialize_response(value: Any) -> Any:
    """Convert objects returned from the SDK into JSON serialisable values."""

    if dataclasses.is_dataclass(value):
        return dataclasses.asdict(value)
    if isinstance(value, list):
        return [_serialize_response(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize_response(item) for key, item in value.items()}
    return value


class AllieSessionManager:
    """Create and cache :class:`Alation` clients per tool invocation."""

    def __init__(self) -> None:
        self._cache: Dict[tuple[str, int, str, bool], Alation] = {}

    def get_client(
        self,
        *,
        host: str,
        user_id: int,
        refresh_token: str,
        validate_ssl: bool = True,
        access_token: str | None = None,
        private_ssl_cert: str | None = None,
    ) -> Alation:
        """Return a cached :class:`Alation` instance or create a new one."""

        cache_key = (host, user_id, refresh_token, validate_ssl)
        if cache_key not in self._cache:
            LOGGER.info("Creating a new Allie SDK session for host=%s user_id=%s", host, user_id)
            self._cache[cache_key] = Alation(
                host=host,
                refresh_token=refresh_token,
                user_id=user_id,
                access_token=access_token,
                validate_ssl=validate_ssl,
                private_ssl_cert=private_ssl_cert,
            )
        return self._cache[cache_key]


class RefreshTokenAuthenticator:
    """Authenticate MCP sessions using the Alation refresh token."""

    scheme = "refresh_token"

    async def __call__(self, refresh_token: str) -> dict[str, Any]:
        expected = _ensure_expected_refresh_token()
        if refresh_token != expected:
            LOGGER.warning("Rejected connection with invalid refresh token.")
            raise AuthenticationError("Invalid refresh token supplied.")
        LOGGER.info("Refresh token validated successfully.")
        return {"refresh_token": refresh_token}


def _method_should_be_exposed(owner: type, method: Callable[..., Any]) -> bool:
    """Return True when the callable represents an SDK method we want to expose."""

    if method.__name__.startswith("_"):
        return False
    qualname = method.__qualname__.split(".")[0]
    return qualname == owner.__name__


def _register_allie_tools(server: FastMCP, session_manager: AllieSessionManager) -> None:
    """Dynamically register a FastMCP tool for every Allie SDK method."""

    method_owners: dict[str, type] = {
        "authentication": AlationAuthentication,
        "business_policy": AlationBusinessPolicy,
        "connector": AlationConnector,
        "custom_field": AlationCustomField,
        "custom_template": AlationCustomTemplate,
        "data_dictionary": AlationDataDictionary,
        "data_quality": AlationDataQuality,
        "datasource": AlationDatasource,
        "dataflow": AlationDataflow,
        "document": AlationDocument,
        "document_hub_folder": AlationDocumentHubFolder,
        "domain": AlationDomain,
        "glossary_term": AlationGlossaryTerm,
        "group": AlationGroup,
        "otype": AlationOtype,
        "policy_group": AlationPolicyGroup,
        "query": AlationQuery,
        "rdbms": AlationRDBMS,
        "trust_checks": AlationTrustChecks,
        "user": AlationUser,
        "virtual_datasource": AlationVirtualDataSource,
        "virtual_filesystem": AlationVirtualFileSystem,
        "visual_config": AlationVisualConfig,
    }

    register_tool = getattr(server, "register_tool", None)
    tool_decorator = getattr(server, "tool", None)

    if register_tool is None:
        if tool_decorator is None:
            raise AttributeError(
                "FastMCP server instance must expose either 'register_tool' or 'tool'."
            )

        def register_tool(**kwargs: Any) -> None:
            decorated = tool_decorator(
                name=kwargs["name"], description=kwargs["description"]
            )
            decorated(kwargs["callable"])

    for attribute_name, owner in method_owners.items():
        for method_name, method in inspect.getmembers(owner, predicate=inspect.isfunction):
            if not _method_should_be_exposed(owner, method):
                continue

            tool_name = f"{attribute_name}.{method_name}"
            description = inspect.getdoc(method) or "Allie SDK method"

            @wraps(method)
            def _tool_function(
                *,
                _attribute=attribute_name,
                _method=method_name,
                _tool_name=tool_name,
                **kwargs: Any,
            ) -> Any:
                """Invoke the wrapped Allie SDK method."""

                host = kwargs.pop("host")
                user_id = kwargs.pop("user_id")
                refresh_token = kwargs.pop("refresh_token")
                access_token = kwargs.pop("access_token", None)
                validate_ssl = kwargs.pop("validate_ssl", True)
                private_ssl_cert = kwargs.pop("private_ssl_cert", None)

                client = session_manager.get_client(
                    host=host,
                    user_id=user_id,
                    refresh_token=refresh_token,
                    access_token=access_token,
                    validate_ssl=validate_ssl,
                    private_ssl_cert=private_ssl_cert,
                )

                owner_instance = getattr(client, _attribute)
                owner_method = getattr(owner_instance, _method)
                LOGGER.debug("Invoking Allie SDK tool %s", _tool_name)
                response = owner_method(**kwargs)
                return _serialize_response(response)

            register_tool(
                name=tool_name,
                description=description,
                callable=_tool_function,
            )


def _register_authenticator(server: FastMCP, authenticator: RefreshTokenAuthenticator) -> None:
    """Attach the authenticator to the FastMCP server instance."""

    if hasattr(server, "register_authenticator"):
        server.register_authenticator(authenticator)
        return
    if hasattr(server, "add_authenticator"):
        server.add_authenticator(authenticator)
        return
    auth_attr = getattr(server, "auth", None)
    if isinstance(auth_attr, list):
        auth_attr.append(authenticator)
        return
    raise AttributeError(
        "FastMCP server instance does not provide an authentication registration API."
    )


def build_app() -> FastMCP:
    """Create the FastMCP application and register every Allie SDK tool."""

    session_manager = AllieSessionManager()
    app = FastMCP(
        name="allie-sdk-mcp",
        description=(
            "Expose the entire Allie SDK surface as Model Context Protocol tools."
        ),
        version="0.1.0",
    )
    _register_authenticator(app, RefreshTokenAuthenticator())
    _register_allie_tools(app, session_manager)
    return app


def main() -> None:
    """Entry point to launch the FastMCP server."""

    logging.basicConfig(level=logging.INFO)
    app = build_app()
    app.run()


if __name__ == "__main__":
    main()
