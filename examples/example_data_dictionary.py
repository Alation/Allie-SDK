"""
Example of uploading a data dictionary file via the Allie SDK

Prerequisites: UPDATE ++++

- You adjusted the "config.ini" file with your settings.
- Download the data dictionary from one Alation data source (that you can use for testing)
- Make some adjustments to the data dictionary (e.g. change a description)
- Adjust some variables in the code below (e.g. filename)

"""

import configparser
import logging
import sys
from pathlib import Path

import allie_sdk as allie


# ================================
# Set Global Variables
# ================================

# Update these variables for your environment
TARGET_OBJECT_TYPE = "data"  # see SUPPORTED_OBJECT_TYPES for the full list
TARGET_OBJECT_ID = 1
DATA_DICTIONARY_PATH = Path("./sample_data_dictionary.csv")

if not DATA_DICTIONARY_PATH.exists():
    logging.error("Create a sample data dictionary file before running this example.")
    sys.exit(1)
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

CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

ALATION_USER_ID = CONFIG.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = CONFIG.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = CONFIG.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# ================================
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL,
    user_id=ALATION_USER_ID,
    refresh_token=ALATION_API_REFRESH_TOKEN,
)

# ================================
# DATA DICTIONARY UPLOAD
# ================================

payload = allie.DataDictionaryItem(
    overwrite_values=True,
    allow_reset=False,
    file=DATA_DICTIONARY_PATH,
)

result = alation.data_dictionary.upload_data_dictionary(
    TARGET_OBJECT_TYPE,
    TARGET_OBJECT_ID,
    payload,
)

logging.info(f"Uploaded data dictionary file {DATA_DICTIONARY_PATH}")
logging.info(f"Status: {result.status}")
logging.info(f"Message: {result.msg}")
