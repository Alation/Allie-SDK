"""
Example of reading a Critical Data Element (CDM / CDE) failing because the requested
Critical Data Element ID does not exist.

`get_critical_data_element` calls `GET /cde-service/integration/cde/{id}/`. If the ID is
not found, the CDE service returns a non-success status code and the SDK raises a
`requests.HTTPError`.

See: https://developer.alation.com/dev/reference/cde-api-overview

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser
import requests

# ================================
# Set Global Variables
# ================================

# MAKE IT FAIL: Use a Critical Data Element ID that does not exist.
INVALID_CDE_ID = 999999999

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
    level=logging.INFO
    , stream=sys.stdout
    , format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================
# Source Global Config
# ================================

config = configparser.ConfigParser()
config.read("./../config.ini")

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# ================================
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL
    , user_id=ALATION_USER_ID
    , refresh_token=ALATION_API_REFRESH_TOKEN
)

# ================================
# Attempt to read a Critical Data Element that does not exist
# ================================

try:
    cde = alation.cdm_critical_data_element.get_critical_data_element(INVALID_CDE_ID)
    print(f"Critical Data Element found: {cde.name!r}")
except requests.exceptions.HTTPError as error:
    print("Failed to read the Critical Data Element!")
    print(f"HTTP status code: {error.response.status_code}")
    print("What to do next: Provide the ID of an existing Critical Data Element.")

"""
expected response:

Failed to read the Critical Data Element!
HTTP status code: 404
What to do next: Provide the ID of an existing Critical Data Element.

expected log message:

... - ERROR - ERROR MESSAGE: Error submitting the CDE GET Request to: /cde-service/integration/cde/999999999/ ...
"""
