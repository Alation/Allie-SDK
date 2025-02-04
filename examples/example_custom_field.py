"""
Example of creating a custom field

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- In the "Set Global Variables" section below define the *unique* name of the custom text field that will be created.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# Define the *unique* name of the custom text field that will be created
CUSTOM_RICH_TEXT_FIELD_NAME = "Rich Text Test 10"
# Define the name of one built-in field
BUILT_IN_FIELD_NAME = "description"

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
# CREATE CUSTOM FIELD
# ================================

response = alation.custom_field.post_custom_fields(
    custom_fields = [
        allie.CustomFieldItem(
            field_type = "RICH_TEXT"
            , name_singular = CUSTOM_RICH_TEXT_FIELD_NAME
        )
    ]
)

if response:
    for r in response:
        if r.status == "successful":
            for rslt in r.result:
                if rslt.data.field_ids:
                    field_id = rslt.data.field_ids[0]
                    logging.info(f"Created custom field with id: {field_id}")
        elif r.status == "failed":
            logging.error(f"Failed to create custom field: {r.result}")
            sys.exit(1)
        else:
            logging.error(f"Unexpected result. I don't know how to handle this ...")
            sys.exit(1)



# ================================
# GET CUSTOM FIELD BY ID
# ================================

custom_field = alation.custom_field.get_a_custom_field(
    field_id = field_id
)

if custom_field is None:
    logging.warning(f"Custom field with id {field_id} could not be found!")
    sys.exit(1)
else:
    logging.info(f"Managed to fetch custom field {custom_field.name_singular} by ID.")

# ================================
# GET CUSTOM FIELD BY NAME
# ================================


my_custom_fields = alation.custom_field.get_custom_fields(
    allie.CustomFieldParams(
        name_singular = CUSTOM_RICH_TEXT_FIELD_NAME
    )
)

if my_custom_fields is None:
    logging.warning(f"Custom field with name '{CUSTOM_RICH_TEXT_FIELD_NAME}' could not be found!")
elif isinstance(my_custom_fields, list):
    no_fields_found = len(my_custom_fields)
    logging.info(f"Managed to fetch {no_fields_found} custom field(s) with the name '{CUSTOM_RICH_TEXT_FIELD_NAME}'.")
    logging.info("The ID of the custom field(s):")
    for cf in my_custom_fields:
        logging.info(f" Custom field id: {cf.id}")
else:
    logging.error("Unexpected result. I don't know how to handle this ...")
    sys.exit(1)

# ================================
# GET A BUILD-IN CUSTOM FIELD
# ================================

builtin_custom_field = alation.custom_field.get_a_builtin_custom_field(
    field_name = BUILT_IN_FIELD_NAME
)

if builtin_custom_field is None:
    logging.warning(f"No built-in field by name of '{BUILT_IN_FIELD_NAME}' found!")
elif isinstance(builtin_custom_field, allie.CustomField):
    logging.info(f"Managed to fetch builtin custom field 'BUILT_IN_FIELD_NAME'.")
    logging.info(f"The ID of the builtin field: {builtin_custom_field.id}")
else:
    logging.error("Unexpected result. I don't know how to handle this ...")
    sys.exit(1)


