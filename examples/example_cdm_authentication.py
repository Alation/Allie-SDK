"""
Example for using the Critical Data Manager (CDM / CDE) authentication methods.

The Critical Data Manager (a.k.a. CDE) uses a dedicated authentication flow: you
exchange your Alation API token for a short-lived CDE token, which is then used
(via the `CDEToken` header) for all subsequent CDE API calls.

See: https://developer.alation.com/dev/reference/cde-api-overview

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import pathlib

import allie_sdk as allie
import logging
import sys
import configparser

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
config_path = pathlib.Path(__file__).parent / "config.ini"
config = configparser.ConfigParser()
with open(config_path, 'r') as f:
    config.read_file(f)

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# ================================
# Authenticate with Alation
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL
    , user_id=ALATION_USER_ID
    , refresh_token=ALATION_API_REFRESH_TOKEN
)

# ================================
# Exchange the Alation token for a CDE token
# ================================

# By default the CDE token is created by exchanging the Alation access token that
# the Alation object authenticated with.
cde_token = alation.cdm_authentication.create_cde_token()

# The CDE token is a plain string, passed in the `CDEToken` header for CDE API calls.
# It is valid for 24 hours from creation; exchange again to obtain a fresh one.
logging.info(f"CDE token created successfully: {cde_token.token[:20]}...")

# ================================
# Exchange a specific Alation token for a CDE token
# ================================

# You can also exchange an explicit Alation API token instead of the one the Alation
# object was created with. Use a valid Alation *access* token here: while the CDE docs
# mention refresh or access tokens, some cde-service deployments reject refresh tokens
# with "403 Access denied: Invalid Alation API token".
cde_token_explicit = alation.cdm_authentication.create_cde_token(
    alation_token=alation.access_token
)

logging.info(f"CDE token (explicit) created successfully: {cde_token_explicit.token[:20]}...")
