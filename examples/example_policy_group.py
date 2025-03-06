"""
Example of listing domains and assigning object to a given domain.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created at least one policy group. Set the POLICY_GROUP_NAME within the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

POLICY_GROUP_NAME = "GDPR Policies"

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
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host = ALATION_BASE_URL
    , user_id = ALATION_USER_ID
    , refresh_token = ALATION_API_REFRESH_TOKEN
)


# ================================
# FETCH POLICY GROUPS
# ================================

policy_groups = alation.policy_group.get_policy_groups(
    allie.PolicyGroupParams(
        search = POLICY_GROUP_NAME
    )
)

if policy_groups:
    policy_group_id = policy_groups[0].id
    print(f"The policy group id for the '{POLICY_GROUP_NAME}' policy group is {policy_group_id}")
