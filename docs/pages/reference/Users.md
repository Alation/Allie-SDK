---
title: Users
parent: SDK Reference
---

# Users
{:.no_toc}

* TOC
{:toc}

## Models

### User
The Python object representing an Alation user. 

Attributes:


| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | The API ID of a user.                                                      |
| display_name   | str                   | The user's display name. |
| username | str                   | The user's username, which is used as user's unique identifier                |
| email | str                   | The user's email address.                |
| first_name  | str              | The user's first name.   |
| last_name  | str              | The user's last name.   |
| title     | str | The job title of the user.                                 |
| url        | str                  | The Alation url of the user.                                              |
| last_login  | datetime             | The last login datetime.   |
| ts_created     | datetime | The date of the user creation.                        |
| profile_id        | int                  | The Alation API profile ID of the user.                                              |


### UserParams
Optional item used to filter the response of the returned data from the function `get_users`.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| id   | set   | Filter by User ID.   |
| profile_id   | set   | Filter by Users profile ID.   |
| display_name | set   | Filter by display name.  |
| display_name__contains | set   | Filter by a case-sensitive substring on display_name.  |
| display_name__icontains | set   | Filter by a case-insensitive substring on display_name.  |
| email | set   | Filter by an exact match on email.  |
| email__contains | set   | Filter by a case-sensitive substring on email.  |
| email__icontains | set   | Filter by a case-insensitive substring on email.  |


## Methods
### get_authenticated_user

```
get_authenticated_user() -> list:
```

Query the currently authenticated user and return their details

Args:
Returns:
* User: The python User object of the authenticated user

### get_users

```
get_users(query_params:UserParams = None) -> list:
```

Query multiple Alation Users and return their details

Args:
* query_params (UserParams): REST API User Query Parameters for user searches.
Returns:
* list: Alation Users with each item being represented as a `User` object

### get_a_user

```
get_a_user(user_id: int) -> User
```

Retrieve a User by their ID.

Args:
* user_id: The id of a user to retrieve

Returns:
* User: The User object if found.

### get_generate_dup_users_accts_csv

```
get_generate_dup_users_accts_csv() -> str
```

Retrieve a list of duplicate users as a csv string

Args:

Returns:
* str: CSV list of duplicate users

### post_remove_dup_users_accts

```
post_remove_dup_users_accts(csv_file: str) -> bool
```

Remove duplicate users using the 'SUSPEND/RETAIN' user list in a CSV file
Args:
* csv_file: CSV List of users to be suspended (removed) or retained.
  
Returns:
* bool: Success of the API call.

## Examples
### get_authenticated_user
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

get_auth_user_result = alation.user.get_authenticated_user()

```
### get_users
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Get all users
get_all_users_result = alation.user.get_users()

# Get a users matching the display_name
query_params = allie.UserParams(display_name="API User")
get_users_result = alation.user.get_users(query_params=query_params)

```
### get_a_user
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Get a user by user ID
get_a_user_result = alation.user.get_a_user(user_id=5)
```
### get_generate_dup_users_accts_csv
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Generate a list of duplicate users. If no duplicates found a success is returned
get_csv_result = alation.user.get_generate_dup_users_accts_csv()

# Sample output: 
# "SN,Username,email,Action,Group\r\n" \
# "1,APIUser1,apiuser@alation.com,RETAIN/SUSPEND,1\r\n" \
# "2,APIUSER1,apiuser1@alation.com,RETAIN/SUSPEND,1\r\n"

if get_csv_result:
    if isinstance(get_csv_result, dict):
        print(get_csv_result.get("Success"))
    else:
        # write get_csv_result CSV into a file
        with open('/tmp/dup_users.csv', 'w') as csv_file:
          csv_file.write(get_csv_result)


```
### post_remove_dup_users_accts
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Sample input in a file: 
# "SN,Username,email,Action,Group\r\n" \
# "1,APIUser1,apiuser@alation.com,RETAIN,1\r\n" \
# "2,APIUSER1,apiuser1@alation.com,SUSPEND,1\r\n"

# Modify the duplicate user csv file and decide which users should be kept or suspended.  
get_generate_dup_users_accts_csv_result = alation.user.post_remove_dup_users_accts("/tmp/dup_users.csv")

```