"""
Example of creating a Critical Data Element (CDM / CDE) failing client-side validation
because the required `name` field is missing.

`create_critical_data_element` (and the bulk variant) validate the payload before any
request is sent: a `CriticalDataElementItem` without a `name` raises `InvalidPostBody`.
This check needs no server connection.

See: https://developer.alation.com/dev/reference/cde-api-overview

"""

import allie_sdk as allie
from allie_sdk.core.custom_exceptions import InvalidPostBody
import logging
import sys

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
    level=logging.INFO
    , stream=sys.stdout
    , format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================
# Attempt to build an invalid create payload
# ================================

# MAKE IT FAIL: no `name` provided.
invalid_item = allie.CriticalDataElementItem(
    description="A Critical Data Element with no name.",
    status="CANDIDATE",
)

try:
    invalid_item.generate_api_post_payload()
    print("Payload generated (unexpected).")
except InvalidPostBody as error:
    print("Failed to build the Critical Data Element payload!")
    print(f"Error: {error}")
    print("What to do next: Provide a 'name' for the Critical Data Element.")

"""
expected response:

Failed to build the Critical Data Element payload!
Error: 'name' is a required field for a Critical Data Element POST payload body
What to do next: Provide a 'name' for the Critical Data Element.
"""
