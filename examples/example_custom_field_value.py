"""
Example of creating a populating a custom field and retrieving a custom field value.

Prerequisites:

- You adjusted the "config_examples.ini" file with your settings.
- In the "Set Global Variables" define the object and field that you want to update.
  The custom field and object have to exist already.
  The custom field has to be assigned to the object's custom template.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# Define the object type and id of the object that you want to update
OBJECT_TYPE = "glossary_term"
OBJECT_OID = 17
# Define the name of the custom text field that you want to update
CUSTOM_RICH_TEXT_FIELD_NAME = "Source(s)"
# Define the value that you want to set the custom field to
CUSTOM_RICH_TEXT_FIELD_VALUE = "Test Value"


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
# LOOKUP ANY REQUIRED DATA
# ================================

my_custom_fields = alation.custom_field.get_custom_fields(
    allie.CustomFieldParams(
        name_singular = CUSTOM_RICH_TEXT_FIELD_NAME
    )
)

if my_custom_fields:
    logging.info(f"Managed to fetch custom field '{CUSTOM_RICH_TEXT_FIELD_NAME}' by name.")
    if len(my_custom_fields) > 1:
        logging.warning(f"More than one custom field found with name: '{CUSTOM_RICH_TEXT_FIELD_NAME}'.")
        sys.exit(1)
    else:
        field_id = my_custom_fields[0].id
        logging.info(f"The field id is: {field_id}.")

# ================================
# SET CUSTOM FIELD VALUE
# ================================

populate_custom_field_result = alation.custom_field.put_custom_field_values(
    [
        allie.CustomFieldValueItem(
            field_id = field_id
            , otype = OBJECT_TYPE
            , oid = OBJECT_OID
            , value = allie.CustomFieldStringValueItem(
                value = CUSTOM_RICH_TEXT_FIELD_VALUE
            )
        )
    ]
)

if populate_custom_field_result[0].result == "successful":
    logging.info(f"Custom field '{CUSTOM_RICH_TEXT_FIELD_NAME}' successfully populated.")
elif populate_custom_field_result[0].result == "failed":
    logging.error(f"Execution failed: {populate_custom_field_result[0].msg}")
    logging.error(populate_custom_field_result[0].result.errors)
    sys.exit(1)

# ================================
# GET CUSTOM FIELD VALUE
# ================================


params = allie.CustomFieldValueParams(
    otype = OBJECT_TYPE
    , oid = OBJECT_OID
    , field_id = field_id
)

get_field_values_result = alation.custom_field.get_custom_field_values(
    params
)

if get_field_values_result:
    logging.info("Managed to fetch custom field value.")