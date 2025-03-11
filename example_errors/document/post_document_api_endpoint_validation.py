"""
Example of the post request failing because of invalid payload caught by the api endpoint validation process

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

DOCUMENT_HUB_ID = 2
# define the name of the document template
DOCUMENT_TEMPLATE_NAME = "DS Test 6"
# define the singular name of the multi picker custom field
# (that is assigned to the document template above)
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

my_template = alation.custom_template.get_custom_templates(
        allie.CustomTemplateParams(
            title = DOCUMENT_TEMPLATE_NAME
        )
    )
if my_template:
    my_template_id = my_template[0].id
else:
    logging.error("No custom template found")
    sys.exit(1)

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


# get random folder
folders = alation.document_hub_folder.get_document_hub_folders(
    allie.DocumentHubFolderParams(
        document_hub_id = DOCUMENT_HUB_ID
    )
)

if folders:
    random_folder_id = folders[0].id
else:
    sys.exit("No folders found")

# ================================
# CREATE DOCUMENTS
# ================================


"""

MAKE IT FAIL

- use id of non-existing folder
- use picker value that doesn't exist

"""

create_document_result = alation.document.create_documents(
    [
        allie.DocumentPostItem(
            title = "My KPI 1x1"
            , description = "This is the description for KPI 1"
            , template_id = my_template_id
            , parent_folder_id = 999999999999999 # <= this value should make the process fail
            , nav_link_folder_ids = []
            , document_hub_id = DOCUMENT_HUB_ID
            , custom_fields = [
                # multi-picker
                allie.CustomFieldValueItem(
                    field_id = my_mp_custom_field_id
                    , value = [
                        allie.CustomFieldStringValueItem(
                            value = "reddddddd" # <= this value should make the process fail
                        )
                    ]
                )
            ]
        )
    ]
)

if create_document_result[0].status == "failed":
    print(f"The request failed: {create_document_result[0].result}")

"""
expected response:

[JobDetailsDocumentPost(status='failed', msg=None, result={'job_id': None, 'invalid_documents': [{'index': 0, 'errors': [{'folder_ids': ['The following Folders don’t exist or are deleted (folder_ids: [999999999999999])']}, [{'non_field_errors': ["The value `['reddddddd']` is not allowed for field `Data Categorization` with field_id `10009`."]}]], 'document': {'title': 'My KPI 1x1', 'description': 'This is the description for KPI 1', 'template_id': 49, 'folder_ids': [999999999999999], 'document_hub_id': 2, 'custom_fields': [{'field_id': 10009, 'value': ['reddddddd']}]}}]})]

expected log message:

ERROR MESSAGE: Error submitting the POST Request to: //integration/v2/document/
ERROR: {'job_id': None, 'invalid_documents': [{'index': 0, 'errors': [{'folder_ids': ['The following Folders don’t exist or are deleted (folder_ids: [999999999999999])']}, [{'non_field_errors': ["The value `['reddddddd']` is not allowed for field `Data Categorization` with field_id `10009`."]}]], 'document': {'title': 'My KPI 1x1', 'description': 'This is the description for KPI 1', 'template_id': 49, 'folder_ids': [999999999999999], 'document_hub_id': 2, 'custom_fields': [{'field_id': 10009, 'value': ['reddddddd']}]}}]}
2024-12-23 16:48:19,765 - ERROR - ERROR MESSAGE: Error submitting the POST Request to: //integration/v2/document/
ERROR: {'job_id': None, 'invalid_documents': [{'index': 0, 'errors': [{'folder_ids': ['The following Folders don’t exist or are deleted (folder_ids: [999999999999999])']}, [{'non_field_errors': ["The value `['reddddddd']` is not allowed for field `Data Categorization` with field_id `10009`."]}]], 'document': {'title': 'My KPI 1x1', 'description': 'This is the description for KPI 1', 'template_id': 49, 'folder_ids': [999999999999999], 'document_hub_id': 2, 'custom_fields': [{'field_id': 10009, 'value': ['reddddddd']}]}}]}

"""