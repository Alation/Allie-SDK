---
title: Authenticate
nav_order: 2
---

# Authenticate
{:.no_toc}

To use the Allie SDK, you must first authenticate with your Alation instance. To do this, you need to initialize the Alation class and pass in an active Refresh Token associated with an active Alation user. For help with Refresh Tokens, see [Generate Tokens for the Alation API](https://developer.alation.com/dev/docs/authentication-into-alation-apis). When you intialize the Alation class with a valid Refresh Token, the Allie SDK will automatically generate an Access Token for you and then authenticate you with your Alation instance.

```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')
```

## Alation Role Permissions

Alation's REST APIs can only be used by Alation user roles who have permission to that API. Your permissions will be determined by the role of the Alation user whose Refresh Token you are using. See the [APIs by Roles](https://developer.alation.com/dev/docs/alation-apis-by-roles) table for more information on which Alation roles can use which APIs.

## Initialize Alation Without Auth Tokens

```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    disable_authentication=True)

val_access_token_res = alation.authentication.validate_access_token(access_token='<ACCESS TOKEN TO VALIDATE>')
print(val_access_token_res)

val_ref_token_res = alation.authentication.validate_refresh_token(refresh_token='<REFRESH TOKEN TO VALIDATE>')
print(val_ref_token_res)
```

Argument `disable_authentication=True` can be passed into the `Alation` class to initialize it without authenticating first into the Alation instance. This feature is specifically for two endpoints `validate_access_token` and `validate_refresh_token` since these two endpoints do not require an API Access Token to be passed in the header when making the API requests to validate the API tokens.

> **NOTE**: When passing in `disable_authentication=True` into the `Alation` instance, only use that instance for validating tokens and nothing else. To use the rest of the Allie SDK endpoints, you will have to instantiate a new `Alation` instance and pass in a refresh token or access token when initializing `Alation`. 