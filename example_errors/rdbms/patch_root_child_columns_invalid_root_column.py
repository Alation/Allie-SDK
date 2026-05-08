"""
Example of the bulk patch request failing because of invalid root column id

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser

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
# PATCH ROOT CHILD COLUMNS
# ================================

"""
MAKE IT FAIL:

- Use invalid root column id
"""

patch_root_child_columns_response = alation.rdbms.patch_root_child_columns(
    ds_id = 1
    , children = [
        allie.RootColumnChildrenPatchItem(
            parent_key = "1.schema.table.root_col"
            , key = "root_col.address.city"
            , title = "City"
            , description = "Bulk updated description"
        )
    ]
)

print(patch_root_child_columns_response)
