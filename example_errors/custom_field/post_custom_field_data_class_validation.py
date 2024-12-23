"""
Example of the post request failing because of invalid payload caught by data class validation

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
# Create Custom Field: Make it fail on the data class validation
# ================================


# input (payload)

"""
Note: Instead of `RICH_TEXT` we specify `RICH_TEXTS`.
The validation in the data model should throw an error.
"""


payload = [
    allie.CustomFieldItem(
       field_type = 'RICH_TEXTS'
       , name_singular = 'Testing'
    )
]

create_result = alation.custom_field.post_custom_fields(
    custom_fields = payload
)

"""
Expected response: None

Error printed to log:

allie_sdk.core.custom_exceptions.InvalidPostBody: The field type 'RICH_TEXTS' is not supported
"""