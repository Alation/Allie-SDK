"""
Example of listing domains failing due to misspelled parameter name.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created at least one domain via the UI.

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
# CREATE DOMAIN
# ================================

# Currently not supported by Allie-SDK

# ================================
# FETCH DOMAINS
# ================================

domains = alation.domain.get_domains(
    allie.DomainParams(
        parent_idd = 1 # <= typo in parameter name
    )
)

"""
Expected behaviour: Fail

TypeError: DomainParams.__init__() got an unexpected keyword argument 'parent_idd'

Process finished with exit code 1
"""

