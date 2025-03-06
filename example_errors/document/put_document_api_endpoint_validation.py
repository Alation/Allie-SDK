"""
Example of the put request failing because of invalid payload caught by the api endpoint validation process

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

DOCUMENT_ID = 6
# define the singular name of the multi picker custom field
# (that is assigned to the document above)
MULTI_PICKER_NAME_SINGULAR = "Data Categorization"

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
# LOOKUP ANY REQUIRED DATA
# ================================

my_mp_custom_fields = alation.custom_field.get_custom_fields(
    allie.CustomFieldParams(
        name_singular = MULTI_PICKER_NAME_SINGULAR
    )
)

if len(my_mp_custom_fields) == 1:
    my_mp_custom_field_id = my_mp_custom_fields[0].id
elif len(my_mp_custom_fields) > 1:
    logging.error("Multiple custom fields found")
    sys.exit(1)
else:
    logging.error("No custom field found")
    sys.exit(1)

# ================================
# CREATE DOCUMENTS
# ================================


"""

MAKE IT FAIL

- use id of non-existing folder
- use picker value that doesn't exist

"""

updated_doc_result = alation.document.update_documents(
    [
        allie.DocumentPutItem(
            id = DOCUMENT_ID
            , description = "This is another description for KPI 1"
            , custom_fields = [
                # multi-picker
                allie.CustomFieldValueItem(
                    field_id=my_mp_custom_field_id
                    , value=[
                        allie.CustomFieldStringValueItem(
                            value="reddddddd"  # <= this value should make the process fail
                        )
                    ]
                )
            ]
        )
    ]
)


if updated_doc_result[0].status == "failed":
    print(f"The request failed: {updated_doc_result[0].result}")

"""
expected response:

[JobDetailsDocumentPut(status='failed', msg=None, result={'job_id': None, 'invalid_documents': [{'index': 0, 'errors': [{'custom_fields': ['Custom field values were included, but no template was specified.']}], 'document': {'id': 6, 'description': 'This is another description for KPI 1', 'custom_fields': [{'field_id': 10009, 'value': ['reddddddd']}], 'document_hub_id': 2}}]})]

expected log message:

ERROR MESSAGE: Error submitting the PUT Request to: //integration/v2/document/
ERROR: {'job_id': None, 'invalid_documents': [{'index': 0, 'errors': [{'custom_fields': ['Custom field values were included, but no template was specified.']}], 'document': {'id': 6, 'description': 'This is another description for KPI 1', 'custom_fields': [{'field_id': 10009, 'value': ['reddddddd']}], 'document_hub_id': 2}}]}
2024-12-23 16:56:15,469 - ERROR - ERROR MESSAGE: Error submitting the PUT Request to: //integration/v2/document/
ERROR: {'job_id': None, 'invalid_documents': [{'index': 0, 'errors': [{'custom_fields': ['Custom field values were included, but no template was specified.']}], 'document': {'id': 6, 'description': 'This is another description for KPI 1', 'custom_fields': [{'field_id': 10009, 'value': ['reddddddd']}], 'document_hub_id': 2}}]}
The request failed: {'job_id': None, 'invalid_documents': [{'index': 0, 'errors': [{'custom_fields': ['Custom field values were included, but no template was specified.']}], 'document': {'id': 6, 'description': 'This is another description for KPI 1', 'custom_fields': [{'field_id': 10009, 'value': ['reddddddd']}], 'document_hub_id': 2}}]}

"""