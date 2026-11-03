"""
Example of the CDE (Critical Data Manager) token exchange failing because of an
invalid Alation API token.

The CDM / CDE service uses a dedicated authentication flow: you exchange your Alation
API token for a short-lived CDE token. If the Alation token is invalid, the exchange
endpoint (`POST /cde-service/integration/auth/`) returns a non-success status code and
`create_cde_token` raises a `requests.HTTPError`.

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

# MAKE IT FAIL: Use an invalid Alation API token to exchange for a CDE token
INVALID_ALATION_TOKEN = "invalid_alation_token"

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

# ================================
# Create session with your Alation instance
# ================================

# We only need an object to reach the CDM authentication methods; token exchange
# is done explicitly below, so authentication at init is disabled.
alation = allie.Alation(
    host=ALATION_BASE_URL
    , user_id=ALATION_USER_ID
    , disable_authentication=True
)

# ================================
# Attempt the CDE token exchange with an invalid Alation token
# ================================

try:
    cde_token = alation.cdm_authentication.create_cde_token(
        alation_token=INVALID_ALATION_TOKEN
    )
    print(f"CDE token created: {cde_token.token[:20]}...")
except requests.exceptions.HTTPError as error:
    print("Failed to exchange the Alation token for a CDE token!")
    print(f"HTTP status code: {error.response.status_code}")
    print("What to do next: Provide a valid Alation API token (refresh or access token).")

"""
expected response:

A requests.exceptions.HTTPError is raised (e.g. status code 401).


expected log message:

... - ERROR - ERROR MESSAGE: Error exchanging the Alation token for a CDE token at: /cde-service/integration/auth/
...

"""
