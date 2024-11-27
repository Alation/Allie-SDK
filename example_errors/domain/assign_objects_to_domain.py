"""
Example of a failing assignment of objects to domain

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
# ASSIGN OBJECTS TO DOMAINS
# ================================


result = alation.domain.assign_objects_to_domain(
    allie.DomainMembership(
        id = 999999999999999999 # <= id does not exist
        , oid = [999999999999999999] # <= id does not exist
        , otype = 'table'
    )
)

print(result)

"""
Expected result:

ERROR CODE: 400000
ERROR DETAIL: Cannot add object to domain 999999999999999999.  The domain has been deleted.
[JobDetails(status='failed', msg=None, result={'detail': 'Cannot add object to domain 999999999999999999.  The domain has been deleted.', 'code': '400000'})]
"""