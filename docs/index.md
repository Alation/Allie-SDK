---
title: Get Started
nav_order: 1
---

# Get Started
{:.no_toc}

Allie SDK is a Python library that Alation customers and partners can use to increase productivity when interacting with Alation's [REST APIs](https://developer.alation.com/dev/reference/createtoken). Using the Allie SDK library, you can manage and update many Alation resources programmatically. You can use this library to create your own custom applications.

* TOC
{:toc}

## Prerequisites

Before installing the Allie SDK, you must have:

* Python. The Allie SDK supports python versions 3.10+.
* Git: Git is required to clone the Allie SDK repository and to contribute to it.

## Install Allie SDK

Allie SDK exists as a package on the [Python Package Index (PyPI)](https://pypi.org/project/allie-sdk/) and can be installed via pip with `pip3 install allie-sdk`. Alternatively, the codebase can also be cloned directly from the official [Allie SDK GitHub Repository](https://github.com/Alation/Allie-SDK).

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
dq_fields = alation.data_quality.get_data_quality_fields()
for dq_field in dq_fields:
    dq_field: allie.DataQualityField
    print(f'{dq_field.name}\n\tkey: {dq_field.key}\n\tdescription: {dq_field.description}')
```

