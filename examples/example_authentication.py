"""
Example for using the authentication methods.

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import allie_sdk as allie
import logging
import sys
import configparser

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
config.read("config.ini")

ALATION_USER_ID = config.get(section = "api", option = "ALATION_USER_ID")
ALATION_BASE_URL = config.get(section = "api", option = "ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section = "api", option = "ALATION_API_REFRESH_TOKEN")

# ================================
# BASIC AUTHENTICATION
# ================================

alation = allie.Alation(
    host = ALATION_BASE_URL
    , user_id = ALATION_USER_ID
    , refresh_token = ALATION_API_REFRESH_TOKEN
)

# ================================
# INITIALIZE ALATION WITHOUT AUTH TOKENS
# ================================

# Note: Only use this approach for validating tokens and nothing else.

alation = allie.Alation(
    host = ALATION_BASE_URL
    , user_id = ALATION_USER_ID
    , disable_authentication = True
)

val_access_token_res = alation.authentication.validate_access_token(access_token = "xawe9q8")
print(val_access_token_res)

val_ref_token_res = alation.authentication.validate_refresh_token(refresh_token = "asdad9we")
print(val_ref_token_res)