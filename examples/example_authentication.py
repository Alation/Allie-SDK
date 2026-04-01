"""
Example for using the authentication methods.

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import pathlib

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
config_path = pathlib.Path(__file__).parent / "config.ini"
config = configparser.ConfigParser()
with open(config_path, 'r') as f:
    config.read_file(f)

ALATION_USER_ID = config.get(section = "api", option = "ALATION_USER_ID")
ALATION_BASE_URL = config.get(section = "api", option = "ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section = "api", option = "ALATION_API_REFRESH_TOKEN")

# OAuth credentials (optional - only if using OAuth authentication)
ALATION_OAUTH_CLIENT_ID = config.get(section = "api", option = "ALATION_OAUTH_CLIENT_ID", fallback=None)
ALATION_OAUTH_CLIENT_SECRET = config.get(section = "api", option = "ALATION_OAUTH_CLIENT_SECRET", fallback=None)

# ================================
# REFRESH TOKEN AUTHENTICATION
# ================================

alation = allie.Alation(
    host = ALATION_BASE_URL
    , user_id = ALATION_USER_ID
    , refresh_token = ALATION_API_REFRESH_TOKEN
)

# ================================
# OAUTH AUTHENTICATION (Client Credentials)
# ================================

if ALATION_OAUTH_CLIENT_ID and ALATION_OAUTH_CLIENT_SECRET:
    logging.info("Using OAuth client_credentials authentication")
    # JWT is created when the Alation object is instantiated, so we can just create the object with the client credentials and it will generate the token automatically
    oauth_alation = allie.Alation(
        host = ALATION_BASE_URL
        , client_id = ALATION_OAUTH_CLIENT_ID
        , client_secret = ALATION_OAUTH_CLIENT_SECRET,
    )
    
    # You can also create OAuth tokens directly using the authentication methods
    oauth_token = oauth_alation.authentication.create_oauth_token()
    logging.info(f"OAuth token created successfully: {oauth_token.access_token[:20]}...")

    # You can also use basic auth scheme to create OAuth tokens directly using the authentication methods
    oauth_token = oauth_alation.authentication.create_oauth_token(use_basic_auth=True)
    logging.info(f"OAuth token created successfully: {oauth_token.access_token[:20]}...")
    
    # You can also use an existing JWT access token
    oauth_with_token = allie.Alation(
        host = ALATION_BASE_URL
        , access_token = oauth_token.access_token  # Use the JWT token directly
        , client_id = ALATION_OAUTH_CLIENT_ID
        , client_secret = ALATION_OAUTH_CLIENT_SECRET
    )
    
else:
    logging.info("OAuth credentials not configured - skipping OAuth examples")

# ================================
# AUTHENTICATION WITHOUT AUTOMATIC TOKEN CREATION
# ================================

# You can also instantiate without automatic authentication for token-only operations
auth_only = allie.Alation(
    host = ALATION_BASE_URL
    , disable_authentication = True
    , user_id = ALATION_USER_ID
    , refresh_token = ALATION_API_REFRESH_TOKEN
    , client_id = ALATION_OAUTH_CLIENT_ID
    , client_secret = ALATION_OAUTH_CLIENT_SECRET
)

# Then manually create tokens as needed
if ALATION_OAUTH_CLIENT_ID and ALATION_OAUTH_CLIENT_SECRET:
    manual_oauth_token = auth_only.authentication.create_oauth_token()
    logging.info(f"Manually created OAuth token: {manual_oauth_token.access_token[:20]}...")

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