"""
Example of the folder delete request failing because the folder id does not exist.

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
# DELETE DOCUMENT HUB FOLDERS
# ================================

"""
MAKE IT FAIL:

- Folder ID that doesn't exist

"""

delete_folder_result = alation.document_hub_folder.delete_document_hub_folders(
    document_hub_folders = [
        allie.DocumentHubFolder(
            id = 99999999999999999
        )
    ]
)

"""
Expected behaviour: Actually this will not fail. The API endpoint doesn't seem to throw an error if the
folder id doesn't exist.
"""