---
title: Trust Check Flags
parent: SDK Reference
---

# Trust Check Flags
{:.no_toc}

* TOC
{:toc}

## Models

### TrustCheckFlag
Individual list item returned in the response of the function `get_trust_checks`.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | The API ID of the trust check flag.                                                      |
| flag_type   | str                   | Type of trust check flag. Response is either `ENDORSEMENT`, `DEPRECATION`, or `WARNING`. |
| flag_reason | str                   | The reason for why the DEPRECATION or WARNING trust check flag was set.                  |
| ts_created  | datetime              | ISO 8601 formatted date time string indicating when the trust check flag was created.    |
| subject     | TrustCheckFlagSubject | Alation catalog object the trust check flag was set for.                                 |
| user        | User                  | Alation user who set the trust check flag.                                               |

### TrustCheckFlagItem
Python object used to create a TrustCheckFlag in Alation and passed in the parameter `trust_check` in the function `post_trust_check`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| flag_type    |   TRUE   | str                   | `ENDORSEMENT`, `DEPRECATION`, or `WARNING`.                  |
| flag_reason  |  FALSE   | str                   | Can only be set if flag_type is `DEPRECATION` or `WARNING`.  |
| flag_subject |   TRUE   | TrustCheckFlagSubject | Alation catalog object the trust check flag will be set for. | 

### TrustCheckFlagSubject
Sub-model used in the parent Models of TrustCheckFlag and TrustCheck Item.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| id    | int   | The applied object's ID. An oid is used in conjunction with its otype is used to uniquely identify an object in Alation.   |
| otype | str   | The applied object's object type. An otype is used in conjunction with its oid to uniquely identify an object in Alation.  |
| url   | str   | Relative URL of the applied object's catalog web page.                                                                     |

### TrustCheckFlagParams
Optional item used to filter the response of the returned data from the function `get_trust_checks`.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| oid   | set   | The applied object's ID. An oid is used in conjunction with its otype is used to uniquely identify an object in Alation.   |
| otype | set   | The applied object's object type. An otype is used in conjunction with its oid to uniquely identify an object in Alation.  |

## Methods
### get_trust_checks

```
get_trust_checks(query_params: TrustCheckFlagParams = None) -> list
```

Query multiple Alation trust check flags

Args:
* query_params (TrustCheckParams): REST API Get Filter Values

Returns:
* list: Alation Trust Check Flags with each item represented as a `TrustCheckFlag` object

### post_trust_check_flag

```
post_trust_check_flag(trust_check: TrustCheckFlagItem) -> TrustCheckFlag
```

Post (Create) an Alation trust check flag.

Args:
* trust_check (TrustCheckFlagItem): Alation Trust Check Flag to be created.

Returns:
* TrustCheckFlag: Alation Trust Check Flag.

### put_trust_check

```
put_trust_check(trust_check: TrustCheckFlag) -> TrustCheckFlag
```

Put (Update) an Alation trust check flag reason only if the flag_type is DEPRECATION or WARNING.

Args:
* trust_check (TrustCheckFlag): Alation Trust Check Flag to be updated.

Returns:
* TrustCheckFlag: Alation Trust Check Flag.

### delete_trust_check

```
delete_trust_check(trust_check: TrustCheckFlag) -> bool
```

Delete an Alation trust check flag.

Args:
* trust_check (TrustCheckFlag): Alation trust check flag to be deleted.
  
Returns:
* bool: Success of the API DELETE call.

## Examples
### Create a trust check flag
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Create a Trust Check Flag
trust_check_item = allie.TrustCheckFlagItem(
    flag_type='WARNING',
    flag_reason='The nightly ETL Job Failed. Data Engineering team looking to resolve',
    subject=allie.TrustCheckFlagSubject(id=6, otype='table')
)
alation.trust_checks.post_trust_check(trust_check_item)
```

### Delete all trust check flags set by a certain user
```python
import allie_dq_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Get all the Trust Check Flags
trust_check_flags = alation.trust_checks.get_trust_checks()

# Loop through the list and delete if Author ID = 1
for flag in trust_check_flags:
    flag: allie.TrustCheckFlag
    if flag.user.id == 1:
        alation.trust_checks.delete_trust_check(flag)
```