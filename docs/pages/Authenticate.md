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