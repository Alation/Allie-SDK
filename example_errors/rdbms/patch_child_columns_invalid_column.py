"""
Example of the patch request failing because of invalid parent column id

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# MAKE IT FAIL: Use invalid column id
STRUCT_COLUMN_ID = 0
DATA_SOURCE_ID = 1

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
  level=logging.INFO
  , stream = sys.stdout
  , format="%(asctime)s - %(levelname)s - %(message)s"
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
# PATCH CHILD COLUMNS
# ================================

"""
MAKE IT FAIL:

- Use invalid column id
"""

patch_child_columns_response = alation.rdbms.patch_child_columns(
    ds_id = DATA_SOURCE_ID
    , column_id = STRUCT_COLUMN_ID
    , children = [
        allie.ChildColumnPatchItem(
            key = "address.city"
            , title = "City"
            , description = "Updated description"
        )
    ]
)

print(patch_child_columns_response)
