"""
Example of the authentication failing because of invalid refresh token

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser
import datetime

# ================================
# Set Global Variables
# ================================

# MAKE IT FAIL: Use invalid refresh token
INVALID_REFRESH_TOKEN = "invalid_refresh_token"

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
    , refresh_token = INVALID_REFRESH_TOKEN
)

if not alation.access_token:
    print("No valid refresh token!")
    print("What to do next: Get a new refresh token.")

"""
Best practice:

Use `alation.authentication.validate_refresh_token()` first to make sure the refresh token is valid.

"""

"""
expected response:

alation.acess_token is None.


expected log message:

2025-01-02 11:46:49,885 - ERROR - ERROR MESSAGE: Error submitting the POST Request to: /integration/v1/validateRefreshToken/
ERROR CODE: 401000
ERROR DETAIL: Refresh token provided is invalid.
Refresh token provided is invalid.
2025-01-02 11:46:49,887 - ERROR - Refresh token provided is invalid.

"""
