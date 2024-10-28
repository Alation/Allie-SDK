"""
Example of DQ value creating failing because of missing property

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
DQ_RULE_NAME = "sdk-test-1"
TABLE_KEY = "1.public.parts.banana" # <= no existing object key => SHOULD FAIL!

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
# Create the data quality field
# ================================

dq_fields = []
field_item = allie.DataQualityFieldItem(
    field_key= DQ_RULE_NAME,
    name='Testing the SDK',
    type='STRING',
    description='Example test code'
)
dq_fields.append(field_item)

result_0 = alation.data_quality.post_data_quality_fields(
    dq_fields
)

if result_0[0].status == "successful":
    logging.info("Data quality rule created successfully.")
else:
    logging.error("Data quality rule creation failed.")
    sys.exit(1)

# ================================
# Create the data quality value
# ================================

dq_values = []
value_item = allie.DataQualityValueItem(
    field_key = DQ_RULE_NAME,
    object_key = TABLE_KEY,
    # object_type = 'TABLE', <= SHOULD FAIL WITHOUT IT!
    status = 'WARNING',
    value = 'DQ Check Passed at 87%'
)
dq_values.append(value_item)
result_1 = alation.data_quality.post_data_quality_values(dq_values)

if result_1[0].status == "successful":
    logging.info("Data quality value submitted successfully.")
else:
    logging.error("Data quality value submission failed.")
    sys.exit(1)

"""
Expected behaviour:

execution gets aborted with following error:

raise InvalidPostBody(
allie_sdk.core.custom_exceptions.InvalidPostBody: 'field_key', 'object_key', 'object_type', 'status', and 'value' are all required fields for the API POST Call



"""