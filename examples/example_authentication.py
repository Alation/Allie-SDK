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

val_access_token_res = alation.authentication.validate_access_token(access_token = "qsdasc")

if val_access_token_res:
    # a JobDetails object will only be returned if something went wrong, e.g. token is not valid
    if isinstance(val_access_token_res, allie.JobDetails):
        if val_access_token_res.status == "failed":
            error_reason = val_access_token_res.result["detail"]
            logging.warning(error_reason)
            if error_reason == "API Access Token provided is invalid.":
                # you could go ahead here and get a new API access token
                pass
    elif isinstance(val_access_token_res, allie.AccessToken):
        logging.info("Access Token is valid.")
    else:
        logging.info("Unexpected result.")



val_ref_token_res = alation.authentication.validate_refresh_token(refresh_token = "hasdafx")
if val_ref_token_res:
    # a JobDetails object will only be returned if something went wrong, e.g. token is not valid
    if isinstance(val_ref_token_res, allie.JobDetails):
        if val_ref_token_res.status == "failed":
            error_reason = val_ref_token_res.result["detail"]
            logging.warning(error_reason)
            if error_reason == "Refresh token provided is invalid.":
                # you could go ahead here and get a new API access token
                pass
    elif isinstance(val_ref_token_res, allie.RefreshToken):
        logging.info("Refresh Token is valid.")
    else:
        logging.info("Unexpected result.")