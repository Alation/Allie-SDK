---
title: Get Started
nav_order: 1
---

# Get Started
{:.no_toc}

The Allie SDK is a Python library that Alation customers and partners can use to increase productivity when interacting with Alation's [REST APIs](https://developer.alation.com/dev/reference/createtoken). Using the Allie SDK library, you can manage and change many Alation resources programmatically. You can use this library to create your own custom applications.

* TOC
{:toc}

## Prerequisites

Before installing the Allie SDK, you must have:

* Python. The Allie SDK support python versions 3.10+.
* Git. Git is required to clone the Allie SDK repository.

## Install Allie SDK

Copy the folder `allie_sdk` to the root of any Python project. Once copied to the root, import the library:

```python
import allie_sdk as allie
```

## Write your first program

Run the following code to get a list of all the data health rules in an Alation environment.

```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Authentication automatically occurs on Alation init
print(alation.access_token)

# Get the data health rules
dq_fields = alation.data_quality.get_data_quality_rules()
for dq_field in dq_fields:
    dq_field: allie.DataQualityField
    print(f'{dq_field.name}\n\tkey: {dq_field.key}\n\tdescription: {dq_field.description}')
```

