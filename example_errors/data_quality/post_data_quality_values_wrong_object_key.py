"""
Example of DQ value creating failing because of wrong object key

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

"""
Expected behaviour:

The DQ endpoint returns status code 202. 
The job details will include: 'failure_count': 1

Full result:
{'fields': {'created': {'count': 0, 'sample': []}, 'updated': {'count': 0, 'sample': []}}, 'values': {'created': {'count': 0, 'sample': []}, 'updated': {'count': 0, 'sample': []}}, 'created_object_attribution': {'success_count': 0, 'failure_count': 1, 'success_sample': [], 'failure_sample': [{'field_key': 'sdk-test-1', 'object_key': '1.public.parts.banana'}]}, 'flag_counts': {'GOOD': 0, 'WARNING': 0, 'ALERT': 0}, 'total_duration': 0.027975329001492355}

=> So overall the request doesn't fail. It's the responsibility of the developer to extract the details
of the job details and check for failure_count.

"""