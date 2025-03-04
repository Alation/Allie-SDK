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
get_authenticated_user() -> User:
```

Query the currently authenticated user and return their details

Args:
Returns:
* User: The python User object of the authenticated user

### get_users

```
get_users(query_params:UserParams = None) -> list[User]:
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
post_remove_dup_users_accts(csv_file: str) -> JobDetails
```

Remove duplicate users using the 'SUSPEND/RETAIN' user list in a CSV file
Args:
* csv_file: CSV List of users to be suspended (removed) or retained.
  
Returns:
* job details

## Examples

See `/examples/example_user.py`.