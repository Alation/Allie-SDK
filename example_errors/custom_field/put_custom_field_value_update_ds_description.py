"""
Example of the put request failing because of an attempt to update the description of a data source

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import allie_sdk as allie
import logging
import sys
import configparser
import datetime

# ================================
# Set Global Variables
# ================================


# ================================
# Define Logging Config
# ================================

logging.basicConfig(
  level=logging.INFO
  , stream = sys.stdout
  , format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================
# Source Global Config
# ================================

config = configparser.ConfigParser()
config.read("./../config.ini")

ALATION_USER_ID = config.get(section = "api", option = "ALATION_USER_ID")
ALATION_BASE_URL = config.get(section = "api", option = "ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section = "api", option = "ALATION_API_REFRESH_TOKEN")

# ================================
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host = ALATION_BASE_URL
    , user_id = ALATION_USER_ID
    , refresh_token = ALATION_API_REFRESH_TOKEN
)

# ================================
# Create Custom Field: Make it fail on updating the description for a data source
# ================================

# This job will fail because we are trying to update the description field of a data source object

my_custom_fields = alation.custom_field.get_custom_fields(
    allie.CustomFieldParams(
        name_singular = 'Description'
    )
)

populate_custom_field_result = alation.custom_field.put_custom_field_values(
    [
        allie.CustomFieldValueItem(
            field_id = my_custom_fields[0].id
            , otype = "data"
            , oid = 1
            , value = allie.CustomFieldStringValueItem(
                value = "Just some test value ..."
            )
        )
    ]
)

if populate_custom_field_result[0].status == "failed":
    logging.error("We received an error ...")

"""
expected response:

[JobDetails(status='failed', msg='Invalid Payload', result={'title': 'Invalid Payload', 'detail': 'Please check the API documentation for more details on the spec.', 'errors': [{'non_field_errors': ['No support for updating `description` field for `data`.']}], 'code': '400000'})]

expected log message:

ERROR - ERROR MESSAGE: Error submitting the PUT Request to: //integration/v2/custom_field_value/async/
ERROR CODE: 400000
ERROR TITLE: Invalid Payload
ERROR DETAIL: Please check the API documentation for more details on the spec.
ERRORS: [{"non_field_errors": ["No support for updating `description` field for `data`."]}]
"""