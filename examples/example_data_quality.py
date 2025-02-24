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

# define the name of the data quality rule
DQ_RULE_NAME = "sdk-test-1"
# specify the key of the table
TABLE_KEY = "2.camera_club.lenses" # <data-source-id>.<schema-name>.<table-name>

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


if result_0 is None:
    logging.error("Tried to create Data quality field, but somehow received no response!")
    sys.exit(1)
elif isinstance(result_0, list):
    for r in result_0:
        if r.status == "successful":
            # Checking for success here is not enough - we need to analyse the content of the returned
            # message to understand whether the fields got created
            if r.result.fields.created.count > 0:
                logging.info("Data quality rule created successfully.")
            else:
                logging.error("Data quality rule request status successful but nothing was created.")
                sys.exit(1)
        else:
            logging.error(f"Data quality rule creation failed: {r.result}")
            sys.exit(1)
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

if result_1 is None:
    logging.error("Tried to create Data quality value, but somehow received no response!")
    sys.exit(1)
elif isinstance(result_1, list):
    for r in result_1:
        if r.status == "successful":
            # Checking for success here is not enough - we need to analyse the content of the returned
            # message to understand whether the values got created
            if r.result.values.created.count > 0:
                logging.info("Data quality value created successfully.")
            else:
                logging.error("Data quality value request status successful but nothing was created.")
                sys.exit(1)
        else:
            logging.error(f"Data quality value creation failed: {r.result}")
            sys.exit(1)
else:
    logging.error("Data quality value creation failed.")
    sys.exit(1)

# ================================
# Get the data quality rule and values
# ================================

dq_fields = alation.data_quality.get_data_quality_fields(
    allie.DataQualityFieldParams(
        key = DQ_RULE_NAME
    )
)

if dq_fields is None:
    logging.warning("No data quality rules/fields found.")
elif isinstance(dq_fields, list):
    logging.info("Following data quality rules/fields found:")
    for f in dq_fields:
        logging.info(f"Name: {f.name}, Key: {f.key}")
else:
    logging.error("Unexpected result when fetching data quality fields.")
    sys.exit(1)


dq_values = alation.data_quality.get_data_quality_values(
    allie.DataQualityValueParams(
        field_key = DQ_RULE_NAME
    )
)

if dq_values is None:
    logging.warning("No data quality values found.")
elif isinstance(dq_values, list):
    logging.info(f"{len(dq_values)} data quality values found.")
else:
    logging.error("Unexpected result when fetching data quality values.")
    sys.exit(1)

# ================================
# Delete a data health rule and child values
# ================================

result_2 = alation.data_quality.delete_data_quality_values(
    dq_values
)


if result_2 is None:
    logging.error("Tried to delete Data quality value, but somehow received no response!")
elif isinstance(result_2, list):
    for r in result_2:
        if r.status == "successful":
            # Checking for success here is not enough - we need to analyse the content of the returned
            # message to understand whether the fields got created
            if r.result.values.deleted.count > 0:
                logging.info("Data quality value deleted successfully.")
            else:
                logging.error("Data quality value request status successful but nothing was deleted.")
                sys.exit(1)
        else:
            logging.error(f"Failed to delete data quality value: {r.result}")
            sys.exit(1)
else:
    logging.error("Unexpected result when deleting data quality value.")
    sys.exit(1)

result_3 = alation.data_quality.delete_data_quality_fields(
    dq_fields
)

if result_3 is None:
    logging.error("Tried to delete Data quality fields, but somehow received no response!")
elif isinstance(result_3, list):
    for r in result_3:
        if r.status == "successful":
            # Checking for success here is not enough - we need to analyse the content of the returned
            # message to understand whether the fields got created
            if r.result.fields.deleted.count > 0:
                logging.info("Data quality fields deleted successfully.")
            else:
                logging.error("Data quality fields request status successful but nothing was deleted.")
                sys.exit(1)
        else:
            logging.error(f"Failed to delete data quality fields: {r.result}")
            sys.exit(1)
else:
    logging.error("Unexpected result when deleting data quality fields.")
    sys.exit(1)