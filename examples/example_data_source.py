"""
Example of listing OCF and native Alation data sources.

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
# Get a list of OCF data sources configured in Alation
# ================================

ocf_datasources = alation.datasource.get_ocf_datasources(
    allie.OCFDatasourceParams(
        include_hidden = False
    )
)

if ocf_datasources is None:
    logging.warning("No OCF datasources found.")
elif isinstance(ocf_datasources, list):
    logging.info("Successfully retrieved list of OCF datasources:")
    for od in ocf_datasources:
        logging.info(od.title)
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)


# ================================
# Get a list of native data sources configured in Alation
# ================================

native_datasources = alation.datasource.get_native_datasources()

if native_datasources is None:
    logging.warning("No native datasources found.")
elif isinstance(native_datasources, list):
    logging.info("Successfully retrieved list of native datasources:")
    for nd in native_datasources:
        logging.info(nd.title)
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)
