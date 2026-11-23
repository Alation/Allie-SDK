# Breaking Changes

List of breaking changes that potentially impact any code you are running that utilises Allie-SDK method.

- Removed `RequestHandler.post_oauth`. Use `post` with a `urlencode`-encoded body,
  `Content-Type: application/x-www-form-urlencoded`, and optional `auth` instead. (`145-streamline-authentication-header-creation`)

- `AuthHeaderType` is now a string-valued enum with `TOKEN` and `BEARER` members.
  Existing `"Token"` and `"Authorization"` arguments remain supported. Invalid modes
  now raise `ValueError` even when no access token is supplied.
