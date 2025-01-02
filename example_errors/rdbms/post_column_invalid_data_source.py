"""
Example of the post request failing because of invalid data source id

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser
import datetime

# ================================
# Set Global Variables
# ================================

# MAKE IT FAIL: Use invalid data source id
DATA_SOURCE_ID = 0

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
# CREATE COLUMN WITH TECHNICAL AND LOGICAL METADATA
# ================================

"""
MAKE IT FAIL:

- Use invalid data source id
"""

post_column_response = alation.rdbms.post_columns(
    ds_id = DATA_SOURCE_ID
    , columns = [
        allie.ColumnItem(
            key = f"{DATA_SOURCE_ID}.ORDERS.refunds.id"
            , column_type = "INTEGER"
            , title = "ID"
            , description = "This is the id column of the refunds table ..."
        )
    ]
)

print()

"""
Expected response:

[JobDetailsRdbms(status='failed', msg=None, result={'detail': 'Data source with id 0 does not exist', 'code': '404000'})]

Expected log message:

2025-01-02 11:13:18,173 - ERROR - ERROR MESSAGE: Error submitting the POST Request to: //integration/v2/column/?ds_id=0
ERROR CODE: 404000
ERROR DETAIL: Data source with id 0 does not exist

"""