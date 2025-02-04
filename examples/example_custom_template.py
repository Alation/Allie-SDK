"""
Example of listing custom templates.

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

CUSTOM_TEMPLATE_NAME = "DS Document"

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
# GET SPECIFIC CUSTOM TEMPLATE
# ================================

templates = alation.custom_template.get_custom_templates(
        allie.CustomTemplateParams(
            title = CUSTOM_TEMPLATE_NAME
        )
    )


if templates is None:
    logging.warning(f"No custom template with the name '{CUSTOM_TEMPLATE_NAME}' found.")
elif len(templates) > 1:
    logging.error(f"More than one document template with the name {CUSTOM_TEMPLATE_NAME} found.")
    logging.error("How to resolve: Make sure the template name is unique!")
    sys.exit(1)
else:
    my_template_id = templates[0].id
    logging.info(f"Template ID: {my_template_id}")


# ================================
# GET ALL CUSTOM TEMPLATES
# ================================

all_templates = alation.custom_template.get_custom_templates(
)

if all_templates is None:
    logging.warning("No custom templates found.")
    sys.exit(1)
elif isinstance(all_templates, list):
    logging.info(f"Found {len(all_templates)} custom templates.")
else:
    logging.error("Unexpected result.")
    sys.exit(1)