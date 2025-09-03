"""Alation REST API OAuth 2.0 Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass


@dataclass
class ErrorResponse(BaseClass):
    """Properties of an error response returned by the OAuth 2.0 API."""

    error: str = field(default=None)
    error_description: str = field(default=None)
    code: str = field(default=None)


@dataclass
class TokenResponse(BaseClass):
    """Token response containing the access token and metadata."""

    access_token: str = field(default=None)
    token_type: str = field(default=None)
    expires_in: int = field(default=None)


@dataclass
class ActiveIntrospectTokenResponse(BaseClass):
    """Response returned when a JWT is active."""

    active: bool = field(default=None)
    client_id: str = field(default=None)
    exp: int = field(default=None)
    iat: int = field(default=None)
    iss: str = field(default=None)
    jti: str = field(default=None)
    nbf: int = field(default=None)
    sub: str = field(default=None)
    unique_id: str = field(default=None)


@dataclass
class InactiveIntrospectTokenResponse(BaseClass):
    """Response returned when a JWT is inactive."""

    active: bool = field(default=None)


@dataclass
class JWKResponse(BaseClass):
    """JSON Web Key representation."""

    e: str = field(default=None)
    kid: str = field(default=None)
    kty: str = field(default=None)
    n: str = field(default=None)
    use: str = field(default=None)


@dataclass
class JWKSetResponse(BaseClass):
    """A set of JSON Web Keys."""

    keys: list[JWKResponse] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.keys, list):
            self.keys = [
                key if isinstance(key, JWKResponse) else JWKResponse.from_api_response(key)
                for key in self.keys
            ]


@dataclass
class ClientCredentialsGrantRequestPayload(BaseClass):
    """Payload for requesting a token using the client credentials grant type."""

    grant_type: str = field(default=None)
    client_id: str = field(default=None)
    client_secret: str = field(default=None)


@dataclass
class TokenIntrospectRequestPayload(BaseClass):
    """Payload for introspecting a token."""

    token: str = field(default=None)
    token_type_hint: str = field(default=None)
    client_id: str = field(default=None)
    client_secret: str = field(default=None)
