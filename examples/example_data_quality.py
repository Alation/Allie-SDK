"""
Example of creating, listing, updating and deleting data quality rules.

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
TABLE_KEY = "1.public.parts" # <data-source-id>.<schema-name>.<table-name>

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
    object_type = 'TABLE',
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

# ================================
# Get the data quality rule and values
# ================================

dq_fields = alation.data_quality.get_data_quality_fields(
    allie.DataQualityFieldParams(
        key = DQ_RULE_NAME
    )
)


dq_values = alation.data_quality.get_data_quality_values(
    allie.DataQualityValueParams(
        field_key = DQ_RULE_NAME
    )
)

# ================================
# Delete a data health rule and child values
# ================================

result_2 = alation.data_quality.delete_data_quality_values(
    dq_values
)

if result_2[0].status == "successful":
    logging.info("Data quality value deleted successfully.")
else:
    logging.error("Failed to delete data quality value.")
    sys.exit(1)

result_3 = alation.data_quality.delete_data_quality_fields(
    dq_fields
)

if result_3[0].status == "successful":
    logging.info("Data quality rule deleted successfully.")
else:
    logging.error("Failed to delete data quality rule.")
    sys.exit(1)