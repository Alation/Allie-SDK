# Plan: Add OAuth Authentication Support

Support OAuth 2.0 client credentials flow for machine-to-machine authorization, allowing JWT token generation using client ID and client secret credentials.

**Steps**
1. **Create OAuth model classes** - Add `OAuthToken` dataclass for JWT and `OAuthCredentials` for client credentials in `authentication_model.py`
2. **Extend authentication methods** - Add OAuth methods to `AlationAuthentication` class for token generation and validation
3. **Update main Alation class** - Add OAuth initialization support with client credentials parameters
4. **Update request handler** - Ensure OAuth JWT tokens work with existing Token header mechanism
5. **Add configuration examples** - Update example files to demonstrate OAuth usage
6. **Add comprehensive tests** - Create tests for OAuth token flow, validation, and error handling
7. **Update documentation** - Add OAuth examples and error handling demonstrations

**Relevant files**
- `allie_sdk/models/authentication_model.py` — Add `OAuthToken` and `OAuthCredentials` dataclasses
- `allie_sdk/methods/authentication.py` — Add `create_oauth_token`, `validate_oauth_token` methods
- `allie_sdk/alation.py` — Add OAuth initialization support with client_id/client_secret parameters
- `allie_sdk/core/request_handler.py` — Ensure Token header works with JWT (no changes expected)
- `examples/example_authentication.py` — Add OAuth usage examples
- `example_errors/authentication/` — Add OAuth error handling examples
- `tests/models/test_authentication_model.py` — Add OAuth model tests
- `tests/methods/test_authentication.py` — Add OAuth method tests
- `docs/pages/reference/Authentication.md` — Update documentation

**Verification**
1. Run unit tests for OAuth models and methods
2. Test OAuth token generation with valid client credentials
3. Test OAuth token validation functionality
4. Test error handling for invalid credentials
5. Verify JWT tokens work with existing API endpoints
6. Test examples against live Alation instance with OAuth configured
7. Validate documentation examples

**Decisions**
- **Scope**: Limited to obtaining JWT tokens (no token introspection or JWT web keys)
- **Authentication**: Support both Basic auth header and request body credentials
- **Integration**: Reuse existing Token header mechanism in RequestHandler
- **Pattern**: Follow existing authentication patterns (dataclasses, error handling, logging)
- **Backwards compatibility**: No changes to existing refresh token authentication