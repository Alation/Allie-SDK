"""
Example of creating a custom field

Prerequisites:

- You adjusted the "config_examples.ini" file with your settings.
- In the "Set Global Variables" sectio below define the *unique* name of the custom text field that will be created.

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
config.read("config_examples.ini")

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

create_result = alation.custom_field.post_custom_fields(
    custom_fields = [
        allie.CustomFieldItem(
            field_type = "RICH_TEXT"
            , name_singular = CUSTOM_RICH_TEXT_FIELD_NAME
        )
    ]
)

if create_result:
    if create_result[0].status == "successful":
        for r in create_result[0].result:
            if r.data.field_ids:
                field_id = r.data.field_ids[0]
                logging.info(f"Created custom field with id: {field_id}")


# ================================
# GET CUSTOM FIELD BY ID
# ================================

get_field_result = alation.custom_field.get_a_custom_field(
    field_id = field_id
)

if get_field_result:
    logging.info(f"Managed to fetch custom field '{CUSTOM_RICH_TEXT_FIELD_NAME}' by ID.")

# ================================
# GET CUSTOM FIELD BY NAME
# ================================


my_custom_fields = alation.custom_field.get_custom_fields(
    allie.CustomFieldParams(
        name_singular = CUSTOM_RICH_TEXT_FIELD_NAME
    )
)

if my_custom_fields:
    logging.info(f"Managed to fetch custom field '{CUSTOM_RICH_TEXT_FIELD_NAME}' by name.")

# ================================
# GET A BUILD-IN CUSTOM FIELD
# ================================

builtin_custom_field = alation.custom_field.get_a_builtin_custom_field(
    field_name = "description"
)

if builtin_custom_field:
    logging.info("Managed to fetch builtin custom field 'description'.")