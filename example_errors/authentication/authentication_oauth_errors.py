"""
Example for demonstrating OAuth authentication errors.

This example shows what happens when OAuth client credentials are invalid.

Prerequisites:

- You adjusted the "config.ini" file with invalid OAuth credentials.
- Your Alation instance has OAuth configured.

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

ALATION_BASE_URL = config.get(section = "api", option = "ALATION_BASE_URL")

# Use invalid OAuth credentials to trigger error
INVALID_CLIENT_ID = "invalid_client_id"
INVALID_CLIENT_SECRET = "invalid_client_secret"

# ================================
# OAUTH AUTHENTICATION ERROR DEMO  
# ================================

try:
    logging.info("Attempting OAuth authentication with invalid credentials...")
    
    oauth_alation = allie.Alation(
        host = ALATION_BASE_URL
        , client_id = INVALID_CLIENT_ID
        , client_secret = INVALID_CLIENT_SECRET
    )
    
    logging.info("OAuth authentication should have failed!")
    
except Exception as error:
    logging.error(f"Expected OAuth authentication error: {error}")

# ================================
# OAUTH TOKEN CREATION ERROR DEMO
# ================================

try:
    logging.info("Attempting manual OAuth token creation with invalid credentials...")
    
    # Create authentication instance without automatic token creation
    auth_only = allie.Alation(
        host = ALATION_BASE_URL
        , disable_authentication = True
        , client_id = INVALID_CLIENT_ID  
        , client_secret = INVALID_CLIENT_SECRET
    )
    
    # Manually try to create OAuth token - this should fail
    oauth_token = auth_only.authentication.create_oauth_token()
    
    logging.info("OAuth token creation should have failed!")
    
except Exception as error:
    logging.error(f"Expected OAuth token creation error: {error}")

# ================================
# MISSING OAUTH CREDENTIALS ERROR DEMO
# ================================

try:
    logging.info("Attempting OAuth authentication without credentials...")
    
    oauth_alation_no_creds = allie.Alation(
        host = ALATION_BASE_URL
        # No client_id or client_secret provided
    )
    
    logging.info("OAuth authentication should have failed due to missing credentials!")
    
except Exception as error:
    logging.error(f"Expected missing credentials error: {error}")

"""
Expected Error Output: Invalid client credentials

{
    "error": "invalid_client",
    "error_description": "Client credentials are incorrect",
    "code": "401"
}

Expected error output: invalid/expired token
{
    "detail": "Authentication failed: invalid bearer token."
}

Expected error output: missing grant_type
{
    "error": "unsupported_grant_type",
    "error_description": "The requested grant is not supported or grant is not passed"
}
"""