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
# CREATE VIRTUAL DATA SOURCE OBJECTS WITHIN EXISTING DATA SOURCE
# ================================

"""
MAKE IT FAIL

- use invalid data source id
"""

# Note this is for uploading the technical metadata
# You have to create the Alation virtual data source beforehand
ds_id = DATA_SOURCE_ID

# Add/Update Objects
ds_schema = "test"

# create the schema first and then submit the payload, otherwise the parser throws and error
s1 = allie.VirtualDataSourceSchema()
s1.key = f'{ds_id}.{ds_schema}'
s1.description = "New Schema for API testing"

vds_objects = [s1]

params = allie.VirtualDataSourceParams()
params.set_title_descs = "true"
params.remove_not_seen = "false"

vds_response = alation.virtual_datasource.post_metadata(
    ds_id=ds_id
    , vds_objects=vds_objects
    , query_params=params
)

print()

"""
expected response:

[JobDetailsVirtualDatasourcePost(status='failed', msg=None, result={'error': 'Cannot find Datasource'})]

expected logging message:

2025-01-02 11:21:19,389 - ERROR - ERROR MESSAGE: Error submitting the POST Request to: //api/v1/bulk_metadata/extraction/0?set_title_descs=true&remove_not_seen=false
ERROR: {'error': 'Cannot find Datasource'}
"""