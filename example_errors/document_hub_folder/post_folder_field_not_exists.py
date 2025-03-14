"""
Example of the folder post request failing because of custom field does not exist

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
# CREATE DOCUMENT HUB FOLDERS
# ================================

"""
MAKE IT FAIL:

- Use a field id that doesn't exist
"""

create_folder_result = alation.document_hub_folder.create_document_hub_folders(
    [
        allie.DocumentHubFolderPostItem(
            title = 'Test Document Hub Folder'
            , description = 'Test Document Hub Folder'
            , document_hub_id = DOCUMENT_HUB_ID
            , custom_fields = [
                allie.CustomFieldValueItem(
                    field_id = 999999999999999 # <= this id should not exist
                    , value = allie.CustomFieldStringValueItem(
                        value = 'Production'
                    )
                )
            ]
        )
    ]
)

if create_folder_result[0].status == "failed":
    print(f"The request failed: {create_folder_result[0].result}")

"""
Expected response:
[JobDetailsDocumentHubFolderPost(status='failed', msg=None, result={'job_id': None, 'invalid_folders': [{'index': 0, 'errors': [[{'field_id': ['The field_id 999999999999999 is not present on the chosen template.']}]], 'folder': {'title': 'Test Document Hub Folder', 'description': 'Test Document Hub Folder', 'document_hub_id': 2, 'custom_fields': [{'field_id': 999999999999999, 'value': 'Production'}], 'template_id': 43}}]})]

Expected log message:
ERROR MESSAGE: Error submitting the POST Request to: //integration/v2/folder/
ERROR: {'job_id': None, 'invalid_folders': [{'index': 0, 'errors': [[{'field_id': ['The field_id 999999999999999 is not present on the chosen template.']}]], 'folder': {'title': 'Test Document Hub Folder', 'description': 'Test Document Hub Folder', 'document_hub_id': 2, 'custom_fields': [{'field_id': 999999999999999, 'value': 'Production'}], 'template_id': 43}}]}
2024-12-23 15:34:01,434 - ERROR - ERROR MESSAGE: Error submitting the POST Request to: //integration/v2/folder/

"""
